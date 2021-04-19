from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
db = SQLAlchemy(app)


class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(140))
    product_type = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"{self.name} - {self.description}"


db.create_all()


@app.route('/')
def index():
    return "Welcome to Cafe la Colombia!"


@app.route('/menu')
def get_menu():
    menu = Menu.query.all()

    if not menu:
        return {"message": "Menu is empty."}

    output = []
    for product in menu:
        output.append({
            'ID': product.id,
            'name': product.name,
            'description': product.description,
            'type': product.product_type
        })

    return {"Menu": output}


@app.route('/menu/drinks')
def get_drinks():
    drinks = Menu.query.all()

    output = []
    for drink in drinks:
        if drink.product_type == "drinks":
            output.append({
                'ID': drink.id,
                'name': drink.name,
                'description': drink.description
            })

    if not output:
        return {"message": "Menu is empty."}
    else:
        return {"drinks": output}


@app.route('/menu/food')
def get_food():
    product = Menu.query.all()

    output = []
    for food in product:
        if food.product_type == "food":
            output.append({
                'ID': food.id,
                'name': food.name,
                'description': food.description
            })

    if not output:
        return {"message": "Menu is empty."}
    else:
        return {"food": output}


@app.route('/menu/<id>')
def get_menu_by_id(id):
    menu = Menu.query.get_or_404(id)
    return {"name": menu.name, "description": menu.description}


@app.route('/menu', methods=['POST'])
def add_menu():
    menu = Menu(
        name=request.json['name'],
        description=request.json['description'],
        product_type=request.json['product_type']
    )
    db.session.add(menu)
    db.session.commit()
    return {"message": f"Menu {menu.id} added"}


@app.route('/menu/<id>', methods=['DELETE'])
def delete_menu(id):
    menu = Menu.query.get(id)

    if menu is None:
        return {"error": f"Menu {id} not found"}

    db.session.delete(menu)
    db.session.commit()

    return {"message": "yeet!"}
