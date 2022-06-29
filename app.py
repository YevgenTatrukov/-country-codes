from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///phone.db'
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class PhoneTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(20), nullable=False)
    part_of_the_world = db.Column(db.String(20), nullable=False)
    code = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<PhoneTable %r>' % self.id


@app.route('/')
def index():
    phone_table = PhoneTable.query.order_by(PhoneTable.country).all()
    return render_template("index.html", phone_table=phone_table)


@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == "POST":
        country = request.form['country']
        part_of_the_world = request.form['part_of_the_world']
        code = request.form['code']

        try:
            code = int(code)
        except:
            return render_template("try.html")

        phone_table = PhoneTable(country=country, part_of_the_world=part_of_the_world, code=code)
        try:
            db.session.add(phone_table)
            db.session.commit()
            return redirect('/')
        except:
            return "При додаванні виникла помилка"

    else:
        return render_template("add.html")


@app.route('/<int:id>')
def phone_detail(id):
    phone_table = PhoneTable.query.get(id)
    return render_template("phone_detail.html", phone_table=phone_table)


@app.route('/<int:id>/update', methods=['POST', 'GET'])
def phone_update(id):
    phone_table = PhoneTable.query.get(id)
    if request.method == "POST":
        phone_table.country = request.form['country']
        phone_table.part_of_the_world = request.form['part_of_the_world']
        phone_table.code = request.form['code']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "При редагуванні виникла помилка"
    else:
        return render_template("update.html", phone_table=phone_table)


@app.route('/<int:id>/del')
def phone_del(id):
    phone_table = PhoneTable.query.get_or_404(id)

    try:
        db.session.delete(phone_table)
        db.session.commit()
        return redirect('/')
    except:
        return "При видаленні виникла похибка"


@app.route('/country_search', methods=['POST', 'GET'])
def country_search():
    phone_table = PhoneTable.query.order_by(PhoneTable.country)
    if request.method == "POST":
        phone_table.country = request.form['country']
        phone_table = phone_table.country
        return render_template("country.html", phone_table=phone_table)
    else:
        return render_template("country_search.html", phone_table=phone_table)




@app.route('/code_search')
def code_search():
    phone_table = PhoneTable.query.order_by(PhoneTable.code).all()

    return render_template("code_search.html", phone_table=phone_table)



if __name__ == "__main__":
    app.run(debug=True)
