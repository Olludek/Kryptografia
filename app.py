from flask import Flask, render_template, request, send_file, session, redirect, url_for
from szyfrowanie_vigenerea import przetworz_pliki_vigenerea, szyfruj_vigenerea, deszyfruj_vigenerea
from szyfrowanie_rail_fence import szyfruj_rail_fence, deszyfruj_rail_fence, przetworz_pliki_rail_fence
from szyfrowanie_DES import szyfruj_des, deszyfruj_des
from szyfrowanie_AES import szyfruj_aes, deszyfruj_aes
from szyfrowanie_diffie_hellman import generuj_klucz_publiczny, generuj_wspolny_klucz
from szyfrowanie_rsa import generuj_klucze, szyfruj_rsa, deszyfruj_rsa
from podpis_cyfrowy import generate_rsa_keys, sign_data, verify_signature, hash_file
from certyfikat import certyfikat_bp  # Import nowego blueprintu


import os
import base64
from werkzeug.utils import secure_filename


# Inicjalizacja aplikacji Flask
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generuje losowy klucz dla sesji

# Ścieżki do przechowywania kluczy
KEY_FOLDER = 'keys'
PRIVATE_KEY_PATH = os.path.join(KEY_FOLDER, 'private_key.pem')
PUBLIC_KEY_PATH = os.path.join(KEY_FOLDER, 'public_key.pem')

# Maksymalny rozmiar przesyłanego pliku (np. 5MB)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

# Dozwolone rozszerzenia plików certyfikatów
ALLOWED_EXTENSIONS_CERT = {'pem', 'der', 'crt', 'cer'}

def allowed_file_cert(filename):
    """
    Sprawdza, czy plik ma dozwolone rozszerzenie certyfikatu.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_CERT

# Sprawdzenie i tworzenie katalogów do zapisu plików
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Definicja głównej strony aplikacji
@app.route('/')
def home():
    return render_template('index.html')

# ----------------------------------------------------------------------------------------------------------------------------------------

# Strona szyfrowania Vigenère'a
@app.route('/szyfrowanie_vigenerea', methods=['GET', 'POST'])
def szyfrowanie_vigenerea():
    result = None
    text, key, operation = "", "", "szyfruj"

    if request.method == 'POST':
        # Pobieranie danych z formularza
        text = request.form.get('text', '')
        key = request.form.get('key', '')
        operation = request.form.get('operation', 'szyfruj')
        
        # Wykonywanie operacji szyfrowania lub deszyfrowania
        if operation == 'szyfruj':
            result = szyfruj_vigenerea(text, key)
        elif operation == 'deszyfruj':
            result = deszyfruj_vigenerea(text, key)

    return render_template('szyfrowanie_vigenerea.html', result=result, text=text, key=key, operation=operation)

# Strona do przesyłania pliku tekstowego do szyfrowania/deszyfrowania
@app.route('/szyfrowanie_vigenerea_file', methods=['POST'])
def szyfrowanie_vigenerea_file():
    result = None
    file_result = None
    key_file, operation_file = "", "szyfruj"

    if request.method == 'POST':
        # Pobieranie pliku i klucza z formularza
        uploaded_file = request.files.get('file')
        key_file = request.form.get('key_file', '')
        operation_file = request.form.get('operation_file', 'szyfruj')

        if uploaded_file:
            # Zapisanie pliku na serwerze
            file_path = f"./uploads/{uploaded_file.filename}"
            uploaded_file.save(file_path)

            # Wykonanie operacji szyfrowania/deszyfrowania
            file_result = przetworz_pliki_vigenerea(file_path, key_file, szyfruj_vigenerea if operation_file == 'szyfruj' else deszyfruj_vigenerea, operation_file)

    return render_template('szyfrowanie_vigenerea.html', result=result, file_result=file_result, key_file=key_file, operation_file=operation_file)

# ----------------------------------------------------------------------------------------------------------------------------------------

# Strona szyfrowania Rail Fence - ręczne wprowadzanie
@app.route('/szyfrowanie_rail_fence', methods=['GET', 'POST'])
def szyfrowanie_rail_fence():
    result, visualization = None, None
    text, key, operation = "", "", "szyfruj"

    if request.method == 'POST':
        # Pobieranie danych z formularza
        text = request.form.get('text', '')
        key = request.form.get('key', '')
        operation = request.form.get('operation', 'szyfruj')

        # Wykonywanie operacji szyfrowania lub deszyfrowania wraz z wizualizacją
        if operation == 'szyfruj':
            result, visualization = szyfruj_rail_fence(text, int(key))
        elif operation == 'deszyfruj':
            result, visualization = deszyfruj_rail_fence(text, int(key))

    return render_template('szyfrowanie_rail_fence.html', result=result, visualization=visualization, text=text, key=key, operation=operation)

# Strona szyfrowania Rail Fence - obsługuje pliki
@app.route('/szyfrowanie_rail_fence_file', methods=['POST'])
def szyfrowanie_rail_fence_file():
    result = None
    processed_file_path = None
    key_file = ""
    operation_file = "szyfruj"  # Domyślnie ustawione na szyfrowanie

    if request.method == 'POST':
        # Pobieranie pliku i pozostałych danych z formularza
        file = request.files.get('file')
        key_file = request.form.get('key_file', '')
        operation_file = request.form.get('operation_file', 'szyfruj')

        if file:
            # Zapisywanie pliku na serwerze (do folderu uploads)
            filename = secure_filename(file.filename)  # Bezpieczne nazwy plików
            file_path = os.path.join(UPLOAD_FOLDER, filename)  # Ścieżka do pliku
            file.save(file_path)  # Zapisanie pliku na serwerze

            # Przetwarzanie pliku (szyfrowanie lub deszyfrowanie)
            if operation_file == 'szyfruj':
                processed_file_path = przetworz_pliki_rail_fence(file_path, int(key_file), szyfruj_rail_fence)
            elif operation_file == 'deszyfruj':
                processed_file_path = przetworz_pliki_rail_fence(file_path, int(key_file), deszyfruj_rail_fence)

    return render_template('szyfrowanie_rail_fence.html', result=result, key_file=key_file, operation_file=operation_file)


# ----------------------------------------------------------------------------------------------------------------------------------------

# Strona szyfrowania DES - ręczne wprowadzanie
@app.route('/szyfrowanie_des', methods=['GET', 'POST'])
def szyfrowanie_des():
    result = None
    text, key, mode, iv, operation = "", "", "ECB", "", "szyfruj"

    if request.method == 'POST':
        # Pobieranie danych z formularza
        text = request.form.get('text', '')
        key = request.form.get('key', '')
        mode = request.form.get('mode', 'ECB')
        iv = request.form.get('iv', '')
        operation = request.form.get('operation', 'szyfruj')

        # Wykonywanie operacji szyfrowania lub deszyfrowania
        if operation == 'szyfruj':
            result = szyfruj_des(text, key, mode, iv)
        elif operation == 'deszyfruj':
            result = deszyfruj_des(text, key, mode, iv)

    return render_template('szyfrowanie_DES.html', result=result, text=text, key=key, mode=mode, iv=iv, operation=operation)

# ----------------------------------------------------------------------------------------------------------------------------------------

# Szyfrowanie plików DES z kodowaniem base64
@app.route('/szyfrowanie_base64_des', methods=['POST'])
def szyfrowanie_base64_des():
    file = request.files.get('file_base64')
    key = request.form['key_base64']
    mode = request.form['mode_base64']
    iv = request.form.get('iv_base64', None)
    operation = request.form['operation_base64']
    output_format = request.form.get('output_format', 'txt')  # Domyślny format .txt

    if operation == 'szyfruj' and file:
        # Zapisywanie przesłanego pliku
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Kodowanie zawartości pliku do base64
        with open(file_path, 'rb') as f:
            base64_content = base64.b64encode(f.read()).decode('utf-8')

        # Szyfrowanie zawartości base64
        encrypted_content = szyfruj_des(base64_content, key, mode, iv)

        # Zapisywanie zaszyfrowanej zawartości do pliku tekstowego
        encrypted_file_path = f"{file_path}_encrypted.txt"
        with open(encrypted_file_path, 'w', encoding='utf-8') as f:
            f.write(encrypted_content)

        # Wysyłanie zaszyfrowanego pliku do użytkownika
        return send_file(encrypted_file_path, as_attachment=True)

    elif operation == 'deszyfruj' and file:
        # Zapisywanie przesłanego pliku
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Odczytywanie zaszyfrowanej zawartości
        with open(file_path, 'r', encoding='utf-8') as f:
            encrypted_content = f.read()

        # Deszyfrowanie zawartości
        decrypted_content = deszyfruj_des(encrypted_content, key, mode, iv)

        # Dekodowanie z base64 do oryginalnego formatu
        original_file_path = f"{file_path}_decrypted.{output_format}"
        with open(original_file_path, 'wb') as f:
            f.write(base64.b64decode(decrypted_content))

        # Wysyłanie odszyfrowanego pliku do użytkownika
        return send_file(original_file_path, as_attachment=True)

# ----------------------------------------------------------------------------------------------------------------------------------------

# Strona szyfrowania AES - ręczne wprowadzanie
@app.route('/szyfrowanie_aes', methods=['GET', 'POST'])
def szyfrowanie_aes():
    result = None
    text = request.form.get('text', '')
    key = request.form.get('key', '')
    mode = request.form.get('mode', 'ECB')
    iv = request.form.get('iv', '')
    operation = request.form.get('operation', 'szyfruj')

    if request.method == 'POST':
        # Wykonywanie operacji szyfrowania lub deszyfrowania
        if operation == 'szyfruj':
            result = szyfruj_aes(text, key, mode, iv)
        elif operation == 'deszyfruj':
            result = deszyfruj_aes(text, key, mode, iv)

    return render_template(
        'szyfrowanie_AES.html', 
        result=result, 
        text=text, 
        key=key, 
        iv=iv, 
        mode=mode, 
        operation=operation
    )

# Szyfrowanie plików AES z kodowaniem base64
@app.route('/szyfrowanie_base64_aes', methods=['POST'])
def szyfrowanie_base64_aes():
    file = request.files.get('file_base64')
    key = request.form['key_base64']
    mode = request.form['mode_base64']
    iv = request.form.get('iv_base64', None)
    operation = request.form['operation_base64']
    output_format = request.form.get('output_format', 'txt')  # Domyślny format .txt

    if operation == 'szyfruj' and file:
        # Zapisywanie przesłanego pliku
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Kodowanie zawartości pliku do base64
        with open(file_path, 'rb') as f:
            base64_content = base64.b64encode(f.read()).decode('utf-8')

        # Szyfrowanie zawartości base64
        encrypted_content = szyfruj_aes(base64_content, key, mode, iv)

        # Zapisywanie zaszyfrowanej zawartości do pliku tekstowego
        encrypted_file_path = f"{file_path}_encrypted.txt"
        with open(encrypted_file_path, 'w', encoding='utf-8') as f:
            f.write(encrypted_content)

        # Wysyłanie zaszyfrowanego pliku do użytkownika
        return send_file(encrypted_file_path, as_attachment=True)

    elif operation == 'deszyfruj' and file:
        # Zapisywanie przesłanego pliku
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Odczytywanie zaszyfrowanej zawartości
        with open(file_path, 'r', encoding='utf-8') as f:
            encrypted_content = f.read()

        # Deszyfrowanie zawartości
        decrypted_content = deszyfruj_aes(encrypted_content, key, mode, iv)

        # Dekodowanie z base64 do oryginalnego formatu
        original_file_path = f"{file_path}_decrypted.{output_format}"
        with open(original_file_path, 'wb') as f:
            f.write(base64.b64decode(decrypted_content))

        # Wysyłanie odszyfrowanego pliku do użytkownika
        return send_file(original_file_path, as_attachment=True)

    # Renderowanie strony z aktualnymi danymi formularza
    return render_template(
        'szyfrowanie_AES.html',
        key_base64=key,
        mode_base64=mode,
        iv_base64=iv,
        operation_base64=operation,
        output_format=output_format
    )

# ----------------------------------------------------------------------------------------------------------------------------------------

# Strona szyfrowania Diffie-Hellmana
@app.route('/szyfrowanie_diffie_hellman', methods=['GET', 'POST'])
def szyfrowanie_diffie_hellman():
    shared_key = None
    if request.method == 'POST':
        try:
            # Pobieranie danych z formularza i konwersja na liczby całkowite
            private_key = int(request.form['private_key'])
            public_key_other = int(request.form['public_key_other'])
            g_value = int(request.form['g_value'])
            p_value = int(request.form['p_value'])

            # Generowanie klucza publicznego użytkownika
            public_key = generuj_klucz_publiczny(private_key, g_value, p_value)
            
            # Generowanie wspólnego klucza
            shared_key = generuj_wspolny_klucz(public_key_other, private_key, p_value)
        except KeyError as e:
            # Obsługa błędów w przypadku brakujących danych
            print(f"Missing key in form: {e}")

    return render_template('szyfrowanie_diffie_hellman.html', shared_key=shared_key)

# ----------------------------------------------------------------------------------------------------------------------------------------

# Generowanie kluczy RSA i zapisanie ich w sesji
@app.route('/generuj_klucze_rsa', methods=['GET'])
def generuj_klucze_rsa():
    private_key, public_key = generuj_klucze()
    session['private_key'] = private_key
    session['public_key'] = public_key
    return render_template('szyfrowanie_rsa.html', private_key=private_key, public_key=public_key)

# Szyfrowanie i deszyfrowanie RSA ręczne
@app.route('/szyfrowanie_rsa', methods=['GET', 'POST'])
def szyfrowanie_rsa():
    result = None
    text = request.form.get('text', '')
    operation = request.form.get('operation', 'szyfruj')

    # Pobieranie kluczy z sesji
    private_key = session.get('private_key')
    public_key = session.get('public_key')

    if request.method == 'POST':
        # Wykonywanie operacji szyfrowania lub deszyfrowania
        if operation == 'szyfruj' and public_key:
            result = szyfruj_rsa(text, public_key)
        elif operation == 'deszyfruj' and private_key:
            result = deszyfruj_rsa(request.form.get('result', ''), private_key)
        else:
            result = "Brak wymaganego klucza lub nieprawidłowa operacja."

    return render_template(
        'szyfrowanie_rsa.html', 
        result=result, 
        text=text, 
        operation=operation, 
        private_key=private_key, 
        public_key=public_key
    )

# Szyfrowanie i deszyfrowanie plików tekstowych za pomocą RSA
@app.route('/szyfrowanie_rsa_file', methods=['POST'])
def szyfrowanie_rsa_file():
    file = request.files.get('file')
    operation = request.form.get('operation', 'szyfruj')
    private_key = session.get('private_key')
    public_key = session.get('public_key')

    if file and operation:
        # Zapisywanie przesłanego pliku
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        if operation == 'szyfruj' and public_key:
            # Odczytywanie danych z pliku
            with open(file_path, 'r', encoding='utf-8') as f:
                data = f.read()
            # Szyfrowanie danych
            encrypted_data = szyfruj_rsa(data, public_key)

            # Zapisywanie zaszyfrowanych danych do pliku
            encrypted_file_path = f"{file_path}_encrypted.txt"
            with open(encrypted_file_path, 'w', encoding='utf-8') as f:
                f.write(encrypted_data)
            # Wysyłanie zaszyfrowanego pliku do użytkownika
            return send_file(encrypted_file_path, as_attachment=True)

        elif operation == 'deszyfruj' and private_key:
            # Odczytywanie zaszyfrowanych danych z pliku
            with open(file_path, 'r', encoding='utf-8') as f:
                encrypted_data = f.read()
            # Deszyfrowanie danych
            decrypted_data = deszyfruj_rsa(encrypted_data, private_key)

            # Zapisywanie odszyfrowanych danych do pliku
            decrypted_file_path = f"{file_path}_decrypted.txt"
            with open(decrypted_file_path, 'w', encoding='utf-8') as f:
                f.write(decrypted_data)
            # Wysyłanie odszyfrowanego pliku do użytkownika
            return send_file(decrypted_file_path, as_attachment=True)

    # Przekierowanie do strony szyfrowania RSA w przypadku błędu
    return redirect(url_for('szyfrowanie_rsa'))

# ------------------------------------------------------------------------------------------------------------------------------------------

# Strona podpisu cyfrowego - generowanie i weryfikacja
@app.route('/podpis_cyfrowy', methods=['GET'])
def podpis_cyfrowy():
    return render_template('podpis_cyfrowy.html')

# Generowanie podpisu cyfrowego
@app.route('/podpis_cyfrowy/generuj', methods=['POST'])
def generuj_podpis():
    file = request.files.get('file')
    if not file:
        return render_template('podpis_cyfrowy.html', podpis="Nie przesłano pliku.")
    
    # Generowanie kluczy RSA, jeśli nie istnieją
    if not os.path.exists(PRIVATE_KEY_PATH) or not os.path.exists(PUBLIC_KEY_PATH):
        generate_rsa_keys()
    
    # Zapisywanie przesłanego pliku
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    # Obliczanie hash pliku
    file_hash = hash_file(file_path)
    
    # Generowanie podpisu cyfrowego
    podpis = sign_data(file_hash)
    
    return render_template('podpis_cyfrowy.html', podpis=podpis)

# Pobieranie podpisu cyfrowego jako plik
@app.route('/podpis_cyfrowy/pobierz_podpis', methods=['POST'])
def pobierz_podpis():
    podpis = request.form.get('podpis')
    if not podpis:
        return redirect(url_for('podpis_cyfrowy'))
    
    # Zapisywanie podpisu do pliku tekstowego
    podpis_bytes = podpis.encode('utf-8')
    podpis_path = os.path.join(OUTPUT_FOLDER, 'podpis.txt')
    with open(podpis_path, 'w') as f:
        f.write(podpis)
    
    # Wysyłanie pliku z podpisem do użytkownika
    return send_file(podpis_path, as_attachment=True)

# Weryfikacja podpisu cyfrowego
@app.route('/podpis_cyfrowy/weryfikuj', methods=['POST'])
def weryfikuj_podpis():
    file = request.files.get('file_verify')
    podpis = request.form.get('podpis_verify')
    
    if not file or not podpis:
        return render_template('podpis_cyfrowy.html', weryfikacja="Nie przesłano pliku lub podpisu.")
    
    # Zapisywanie przesłanego pliku
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    # Obliczanie hash pliku
    file_hash = hash_file(file_path)
    
    # Weryfikacja podpisu cyfrowego
    jest_prawidlowy = verify_signature(file_hash, podpis)
    
    # Przygotowanie wyniku weryfikacji
    if jest_prawidlowy:
        wynik = "Podpis jest prawidłowy."
    else:
        wynik = "Podpis jest nieprawidłowy lub plik został zmieniony."
    
    return render_template('podpis_cyfrowy.html', weryfikacja=wynik)

# ------------------------------------------------------------------------------------------------------------------------------------------

# Rejestracja blueprintu dla certyfikatów
app.register_blueprint(certyfikat_bp)

# Uruchomienie aplikacji w trybie debugowania
if __name__ == '__main__':
    app.run(debug=True)
