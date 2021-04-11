from flask import Flask, render_template, request, redirect, jsonify, session
app = Flask(__name__)
app.secret_key = 'cseukcfhussjdgbv'

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


cred = credentials.Certificate("kunci.json")
firebase_admin.initialize_app(cred)
db = firestore.client()



@app.route('/')
def index():
    daftar_mahasiswa = []
    docs = db.collection('mahasiswa').stream()
    for doc in docs :
        mhs = doc.to_dict()
        mhs['id'] = doc.id
        daftar_mahasiswa.append(mhs)
    return render_template("index.html", daftar_mahasiswa=daftar_mahasiswa)

@app.route('/proseslogin', methods=["POST"])
def proseslogin():
    username_form = request.form.get("username")
    password_form = request.form.get("password")

    docs = db.collection('admin').where("username", "==", username_form).stream()
    for doc in docs:
        admin = doc.to_dict()
        print(admin)
        if admin['password'] == password_form:
            print('berhasil login')
        
        else:
            print('gagal')
   
    return render_template("login.html")

@app.route('/login')
def login():
    if 'login' in session:
        return redirect('/')
    return render_template("login.html")

@app.route('/logout')
def logout():
    return render_template("login.html")

@app.route('/detail/<uid>')
def detail(uid):
    mahasiswa = db.collection('mahasiswa').document(uid).get().to_dict()
    return render_template("detail.html", mahasiswa=mahasiswa)

@app.route('/update/<uid>')
def update(uid):
    mhs = db.collection('mahasiswa').document(uid).get()
    mahasiswa = mhs.to_dict()
    mahasiswa['id'] = mhs.id
    return render_template('update.html', mhs=mahasiswa)

@app.route('/updatedata/<uid>')
def updatedata(uid):
    nama = request.form.get("nama")
    nilai = request.form.get("nilai")

@app.route('/delete/<uid>')
def delete(uid):
    db.collection('mahasiswa').document(uid).delete()

    daftar_mahasiswa = []
    docs = db.collection('mahasiswa').stream()
    for doc in docs :
        mhs = doc.to_dict()
        mhs['id'] = doc.id
        daftar_mahasiswa.append(mhs)
    return render_template("index.html", daftar_mahasiswa=daftar_mahasiswa)

@app.route('/add', methods=["POST"])
def add_data():
    nama = request.form.get("nama")
    nilai = request.form.get("nilai")
    email = request.form.get("email")
    alamat = request.form.get("alamat")
    no_hp = request.form.get("no_hp")
    mahasiswa = {
        'alamat' : alamat,
        'email' : email,
        'nama' : nama,
        'nilai' : int(nilai),
        'no_hp' : no_hp
    }
    
    db.collection('mahasiswa').document().set(mahasiswa)

    daftar_mahasiswa = []
    docs = db.collection('mahasiswa').stream()
    for doc in docs :
        mhs = doc.to_dict()
        mhs['id'] = doc.id
        daftar_mahasiswa.append(mhs)
    return render_template("index.html", daftar_mahasiswa=daftar_mahasiswa)

@app.route('/api/mahasiswa')
def api_mahasiswa():
    daftar_mahasiswa = []
    docs = db.collection('mahasiswa').stream()
    for doc in docs :
        mhs = doc.to_dict()
        mhs['id'] = doc.id
        daftar_mahasiswa.append(mhs)
    return jsonify(daftar_mahasiswa)

@app.route('/api/mahasiswa/<uid>')
def api_mahasiswa_detail(uid):
    mahasiswa = db.collection('mahasiswa').document(uid).get().to_dict()
    return jsonify(mahasiswa)

if __name__ == "__main__":
    app.run(debug=True)