from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
db = SQLAlchemy(app)


class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(140))

    def __repr__(self):
        return f"{self.name} - {self.description}"


db.create_all()


@app.route('/')
def index():
    return "Welcome to Cafe la Colombia!"


@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()

    if not drinks:
        return {"message": "No drinks yet."}

    output = []
    for drink in drinks:
        output.append({
            'ID': drink.id,
            'name': drink.name,
            'description': drink.description
        })

    return {"drinks": output}


@app.route('/drinks/<id>')
def get_drink_by_id(id):
    drink = Drink.query.get_or_404(id)
    return {"name": drink.name, "description": drink.description}


@app.route('/drinks', methods=['POST'])
def add_drinks():
    drink = Drink(
        name=request.json['name'],
        description=request.json['description']
    )
    db.session.add(drink)
    db.session.commit()
    return {"message": f"Drink {drink.id} added"}
