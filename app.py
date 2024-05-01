"""Flask app for Cupcakes"""
from flask import Flask, request, render_template, jsonify
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'

connect_db(app)

@app.route('/')
def homepage():
    '''homepage'''
    return render_template('index.html')

@app.route('/api/cupcakes')
def list_cupcakes():
    '''return all cupcakes'''
    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes = cupcakes)

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    '''add a cupcake and return data about new cupcake'''
    data = request.json
    cupcake = Cupcake(
        flavor = data['flavor'],
        size = data['size'],
        rating = data['rating'],
        image = data['image'] or None)

    db.session.add(cupcake)
    db.session.commit()

    return (jsonify(cupcake = cupcake.serialize()), 201)


@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    '''return data on specific cupcake'''
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake = cupcake.serialize())


@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def update_cupcake(id):
    '''update cupcake from data in request. return updated data'''
    data = request.json
    cupcake = Cupcake.query.get_or_404(id)

    cupcake.flavor = data['flavor']
    cupcake.size = data['size']
    cupcake.rating = data['rating']
    cupcake.image = data['image']

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake = cupcake.serialize())


@app.route('/api/cupcakes/<int:id>', methods=['DELETE'])
def delete_cupcake(id):
    '''delete cupcake and return confirmation message'''
    cupcake = Cupcake.query.get_or_404(id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message = 'Deleted')