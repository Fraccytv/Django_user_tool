from django.shortcuts import render
from twofactor.services import get_user_qr
from twofactor.services import verify_token
from twofactor.backup import generate_backup_codes
# Create your views here.

def show_qr(request):
    user = request.user
    tf = user.usertwofactor
    
    qr_code = get_user_qr(user.email, tf.secret_key)
    return render(request, 'twofactor/qr_code.html', {'qr_code': qr_code})

def activate_2fa(request):
    user = request.user
    
    if request.method == 'POST':
        token = request.POST.get('token')
        
        if verify_token(user, token):
            user.usertwofactor.is_enabled = True
            user.usertwofactor.save()
            
            codes = generate_backup_codes(user)
            
            return render(request, "twofactor/show_backup_codes.html", {"codes": codes})
        else:
            return render(request, 'twofactor/enable_failed.html', {'error': 'Invalid token'})
        
    return render(request, 'twofactor/activate_2fa.html')

