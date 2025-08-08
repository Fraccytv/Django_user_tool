import base64
from typing import Final

_DATA_URI_PREFIX: Final[str] = 'data:{mime};base64,'


def encode_data_uri(mime: str, payload: bytes) -> str:
    """Returnér data-URI for et binært payload.
    Hvorfor: Nem visning af QR direkte i <img src="..."> uden filer.
    """
    b64 = base64.b64encode(payload).decode('ascii')
    return _DATA_URI_PREFIX.format(mime=mime) + b64