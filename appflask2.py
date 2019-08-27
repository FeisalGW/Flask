from flask import Flask, jsonify, redirect, request, render_template
import mysql.connector

app=Flask(__name__)
db= mysql.connector.connect(
    host='localhost',
    user='feisal',
    passwd='1616',
    database='school'

)

@app.route('/',methods=['GET'])
def beranda():
    return render_template('form_appflask2.html')

@app.route('/students', methods=['GET', 'POST'])
def students():
    if request.method == 'GET':
        used=db.cursor()
        used.execute('describe students')
        hasil=used.fetchall()
        namaKolom=[]

        for i in hasil:
            namaKolom.append(i[0])
        used.execute('select * from students')
        hasil=used.fetchall()
        data=[]
        for i in hasil:
            x={
                namaKolom[0]: i[0],
                namaKolom[1]: i[1],
                namaKolom[2]: i[2],
            }
            data.append(x)
        return jsonify(data)
    elif request.method == 'POST':
        # body = request.json
        body = request.form
        used = db.cursor()
        qry = 'insert into students(nama, usia) values (%s,%s)'
        val = (body['nama'], body['usia'])
        used.execute(qry, val)
        db.commit()
        # return jsonify({'status':'data sudah masuk'})
        return redirect('/students')
    else:
        return jsonify({'status': 'Anda tidak diizinkan, hanya boleh GET & POST'})

##get user by id
@app.route('/students/<string:nis>')
def student(nis):
    if nis.isdigit() and int(nis) >0:
        used=db.cursor()
        used.execute('describe students')
        hasil=used.fetchall()
        namaKolom=[]

        for i in hasil:
            namaKolom.append(i[0])
        qry = 'select * from students where nis = %s'
        nis = (nis,)
        used.execute(qry, nis)
        hasil=used.fetchall()
        data=[]
        for i in hasil:
            x={
                namaKolom[0]: i[0],
                namaKolom[1]: i[1],
                namaKolom[2]: i[2],
            }
            data.append(x)
        return jsonify(data)
    else:
        return jsonify({'status': 'Harap masukkan angka! > 0'})


if __name__ == '__main__':
    app.run(debug=True)

