import secrets
from .models import BackupCode

def generate_backup_codes(user, amount=10):
    codes = []
    
    for _ in range(amount):
        code = secrets.token_hex(4)
        BackupCode.objects.create(user=user, code=code)
        codes.append(code)
    return codes

def verify_backup_code(user, input_code):
    try:
        backup = BackupCode.objects.get(user=user, code=input_code, used=False)
        backup.used = True
        backup.save()
        return True
    except BackupCode.DoesNotExist:
        return False
    