from flask import Flask, render_template,request,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Secure Key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/flaskcrud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))

    def __init__(self, name, email, phone):
        self.email = email
        self.name = name
        self.phone = phone


with app.app_context():
    db.create_all()

@app.route('/')
def Index():
    all_data = Employee.query.all()
    return render_template("index.html", employees=all_data)

@app.route('/insert', methods= ['POST'])
def Insert():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        my_data = Employee(name, email, phone)
        db.session.add(my_data)
        db.session.commit()

        flash("Employee has been inserted successfully.")

        return redirect(url_for('Index'))

@app.route('/update', methods=['GET','POST'])
def update():

    if request.method == 'POST':
        my_data = Employee.query.get(request.form.get('id'))
        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']

        db.session.commit()

        flash("Employee Updated Successfully")

        return redirect(url_for('Index'))

@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = Employee.query.get(id)
    db.session.delete(my_data)
    db.session.commit()

    flash("Employe deleted successfully")

    return redirect(url_for('Index'))


if __name__ == "__main__":
    app.run(debug=True)


