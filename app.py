from flask import Flask, render_template, request, redirect, url_for, session
import os
from ldap3 import Server, Connection, ALL, NTLM

app = Flask(__name__)
app.secret_key = 'aguadesalsicha'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Função para autenticação LDAP
def authenticate_ldap(username, password):
    server = Server('ldap://srvcn07.clubenaval.intra', get_info=ALL)  # Substitua pelo seu servidor LDAP
    try:
        # Cria a conexão com o servidor LDAP
        conn = Connection(server, user=f'clubenaval\\{username}', password=password, authentication=NTLM)
        if conn.bind():  # Tenta fazer o bind com as credenciais
            return True
        else:
            return False
    except Exception as e:
        print(f"Erro na autenticação LDAP: {e}")
        return False

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Validação com Active Directory via LDAP
        if authenticate_ldap(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return "Login falhou!"

    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    return render_template('dashboard.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'files[]' not in request.files:
            return redirect(request.url)
        files = request.files.getlist('files[]')

        for file in files:
            if file and allowed_file(file.filename):
                filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        return redirect(url_for('dashboard'))

    return render_template('upload.html')

@app.route('/delete', methods=['POST'])
def delete_images():
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/slideview')
def slideview():
    images = os.listdir(app.config['UPLOAD_FOLDER'])
    images = [img for img in images if allowed_file(img)]
    return render_template('slideview.html', images=images)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
