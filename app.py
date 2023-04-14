from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:root@localhost/College"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    birthday = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    education = db.Column(db.String(20), nullable=False)
    development_language = db.Column(db.String(30), nullable=False)

    def __repr__(self) -> str:
        return f"{self.id} - {self.first_name}"

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        id = request.form.get('id')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        birthday = request.form.get('birthday')
        email = request.form.get('email')
        gender = request.form.getlist('gender')
        phone = request.form.get('phone')
        education = request.form.get('education')
        development_language = request.form.get('development_language')
        student = Student(first_name=first_name, last_name=last_name, birthday=birthday, email=email,
                          gender=gender, phone=phone, education=education, development_language=development_language)
        db.session.add(student)
        db.session.commit()
    allstudent = Student.query.all()

    return render_template('index.html', allstudent=allstudent)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def Update(id):
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        birthday = request.form.get('birthday')
        email = request.form.get('email')
        gender = request.form.get('gender')
        phone = request.form.get('phone')
        education = request.form.get('education')
        development_language = request.form.get('development_language')
        student = Student.query.filter_by(id=id).first()
        student.first_name = first_name
        student.last_name = last_name
        student.birthday = birthday
        student.email = email
        student.gender = gender
        student.phone = phone
        student.education = education
        student.development_language = development_language
        db.session.add(student)
        db.session.commit()
        return redirect('/')
    student = Student.query.filter_by(id=id).first()
    return render_template('update.html', student=student)


@app.route('/delete/<int:id>')
def Delete(id):
    student = Student.query.filter_by(id=id).first()
    db.session.delete(student)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, port=8000)
