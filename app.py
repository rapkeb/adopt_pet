from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///adoptPet.db'
app.secret_key = "super secret key"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=False, nullable=False)
    age = db.Column(db.Integer, unique=False, nullable=False)
    animal = db.Column(db.String(10), unique=False, nullable=False)
    photo = db.Column(db.String(100), unique=False, nullable=False)
    description = db.Column(db.String(100), unique=False, nullable=False)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=False, nullable=False)
    password = db.Column(db.String(20), unique=False, nullable=False)


class Opinion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    petId = db.Column(db.Integer, primary_key=False)
    username = db.Column(db.String(20), unique=False, nullable=False)
    opinion = db.Column(db.String(200), unique=False, nullable=False)


@app.route("/")
def homepage():
    pets = Pet.query.all()
    if 'username' not in session:
        return render_template("homepage.html", pets=pets, user_authenticated="")
    else:
        return render_template("homepage.html", pets=pets, user_authenticated=session["username"])


@app.route('/filter_pets', methods=['POST'])
def filter_pets():
    selected_kind = request.form.get('petKind')
    all_pets = Pet.query.all()
    if selected_kind == 'all':
        filtered_pets = all_pets
    else:
        filtered_pets = [pet for pet in all_pets if pet.animal == selected_kind]
    if 'username' not in session:
        return render_template('homepage.html', pets=filtered_pets, user_authenticated="")
    else:
        return render_template("homepage.html", pets=filtered_pets, user_authenticated=session["username"])


@app.route("/show_animal/<int:id>", methods=["POST", "GET"])
def show_animal(id):
    if 'username' not in session:
        pets = Pet.query.all()
        return render_template("homepage.html", pets=pets, user_authenticated="")
    if request.method == "POST":
        opinion = request.form.get("opinion")
        petId = request.form.get("petId")
        value = Opinion.query.filter(Opinion.username == session["username"], Opinion.petId==petId).first()
        if value:
            value.opinion = opinion
            db.session.flush()
            db.session.commit()
        else:
            o = Opinion(username=session["username"], opinion=opinion, petId=petId)
            db.session.add(o)
            db.session.commit()
        return redirect(f"/show_animal/{id}")
    else:
        opinions = Opinion.query.filter(Opinion.petId == id)
        pet = Pet.query.get(id)
        return render_template("show_animal.html", pet=pet, user_authenticated=session["username"], opinions=opinions)


@app.route("/delete_opinion/<int:id>")
def delete_opinion(id):
    opinion = Opinion.query.get(id)
    db.session.delete(opinion)
    db.session.commit()
    return redirect("/")


def delete_pet_and_opinions(id):
    data = Pet.query.get(id)
    opinions = Opinion.query.filter(Opinion.petId == id)
    db.session.delete(data)
    for o in opinions:
        db.session.delete(o)
    db.session.commit()


@app.route("/delete_pet/<int:id>", methods=["POST", "GET"])
def delete_pet(id):
    if 'username' not in session:
        pets = Pet.query.all()
        return render_template("homepage.html", pets=pets, user_authenticated="")
    if request.method == "POST":
        delete_pet_and_opinions(id)
        return redirect("/")
    else:
        pets = Pet.query.all()
        return render_template("delete_pet.html", pets=pets, user_authenticated=session["username"])


@app.route("/add_pet/", methods=["POST", "GET"])
def add_pet():
    if 'username' not in session:
        pets = Pet.query.all()
        return render_template("homepage.html", pets=pets, user_authenticated="")
    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        animal = request.form.get("animal")
        photo = request.form.get("photo")
        description = request.form.get("description")
        p = Pet(name=name, age=age, animal=animal, photo=photo, description=description)
        db.session.add(p)
        db.session.commit()
        return redirect("/")
    else:
        return render_template("addPet.html", user_authenticated=session["username"])


@app.route("/register/", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmPassword = request.form.get("confirmPassword")
        users = User.query.all()
        for user in users:
            if user.username == username:
                return redirect("/register")
        if password == confirmPassword:
            u = User(username=username, email=email, password=password)
            db.session.add(u)
            db.session.commit()
            return redirect("/login")
        else:
            return redirect("/register")
    else:
        return render_template("register.html", user_authenticated="")


@app.route("/login/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        users = User.query.all()
        for user in users:
            if user.username == username and user.password == password:
                session['username'] = username
                return redirect("/")
        return redirect("/login")
    else:
        return render_template("login.html", user_authenticated="")


@app.route("/logout/")
def logout():
    session.pop('username', None)
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)
