from flask import Blueprint, render_template, request, send_file, redirect, url_for
from cryptography import x509
from cryptography.hazmat.backends import default_backend
import os
import base64
from io import BytesIO

# Utworzenie blueprintu dla certyfikatów
certyfikat_bp = Blueprint('certyfikat', __name__, template_folder='templates')

# Ścieżki do przechowywania certyfikatów
CERT_UPLOAD_FOLDER = 'certs'
os.makedirs(CERT_UPLOAD_FOLDER, exist_ok=True)

def parse_certificate(cert_data):
    """
    Parsuje certyfikat X.509 i zwraca słownik z jego informacjami.
    """
    cert = x509.load_pem_x509_certificate(cert_data, default_backend())
    
    cert_info = {
        'subject': cert.subject.rfc4514_string(),
        'issuer': cert.issuer.rfc4514_string(),
        'serial_number': cert.serial_number,
        'version': cert.version.name,
        'not_valid_before': cert.not_valid_before,
        'not_valid_after': cert.not_valid_after,
        'signature_algorithm': cert.signature_algorithm_oid._name,
        'public_key': cert.public_key().__class__.__name__,
        'extensions': []
    }
    
    for ext in cert.extensions:
        cert_info['extensions'].append({
            'oid': ext.oid.dotted_string,
            'name': ext.oid._name,
            'value': str(ext.value)
        })
    
    return cert_info

def parse_certificate_chain(cert_chain_data):
    """
    Parsuje łańcuch certyfikatów X.509 i zwraca listę słowników z ich informacjami.
    """
    certs = []
    # Zakładamy, że certyfikaty są w formacie PEM i kolejno po sobie
    pem_certs = cert_chain_data.split(b'-----END CERTIFICATE-----')
    for pem_cert in pem_certs:
        pem_cert = pem_cert.strip()
        if pem_cert:
            pem_cert += b'\n-----END CERTIFICATE-----\n'
            cert_info = parse_certificate(pem_cert)
            certs.append(cert_info)
    return certs

@certyfikat_bp.route('/certyfikat', methods=['GET', 'POST'])
def certyfikat():
    cert_info = None
    cert_chain_info = None
    error = None
    
    if request.method == 'POST':
        cert_file = request.files.get('cert_file')
        cert_type = request.form.get('cert_type')  # 'single' or 'chain'
        
        if not cert_file:
            error = "Nie przesłano pliku certyfikatu."
            return render_template('certyfikat.html', error=error)
        
        try:
            cert_data = cert_file.read()
            # Sprawdzenie, czy certyfikat jest w formacie PEM
            if b'-----BEGIN CERTIFICATE-----' not in cert_data:
                error = "Certyfikat musi być w formacie PEM (ASCII z kodowaniem Base64)."
                return render_template('certyfikat.html', error=error)
            
            if cert_type == 'single':
                cert_info = parse_certificate(cert_data)
            elif cert_type == 'chain':
                cert_chain_info = parse_certificate_chain(cert_data)
            else:
                error = "Nieznany typ certyfikatu."
        except Exception as e:
            error = f"Błąd podczas parsowania certyfikatu: {e}"
    
    return render_template('certyfikat.html', cert_info=cert_info, cert_chain_info=cert_chain_info, error=error)
