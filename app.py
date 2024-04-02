from flask_migrate import Migrate
from flask import Flask, request, jsonify
from models import db, Baby
from flask_cors import CORS


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///babies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})  # Initialize CORS


db.init_app(app)
migrate = Migrate(app, db)

@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello, world!'

@app.route('/babies', methods=['GET'])
def get_babies():
    babies = Baby.query.all()
    baby_list = []
    for baby in babies:
        baby_data = {
            'id': baby.id,
            'name': baby.name,
            'age': baby.age,
            'weight': baby.weight
        }
        baby_list.append(baby_data)
    return jsonify(baby_list)

@app.route('/babies/<int:id>', methods=['GET'])
def get_baby(id):
    baby = Baby.query.filter_by(id=id).first()
    baby_data = {
        'id': baby.id,
        'name': baby.name,
        'age': baby.age,
        'weight': baby.weight
    }
    return jsonify(baby_data)      



@app.route('/babies', methods=['POST'])
def create_baby():
    data = request.json
    name = data.get('name')
    age = data.get('age')
    weight = data.get('weight')

    if not name or not age or not weight:
        return jsonify({'error': 'Missing required fields'}), 400

    new_baby = Baby(name=name, age=age, weight=weight)
    db.session.add(new_baby)
    db.session.commit()

    return jsonify({'message': 'Baby created successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)
