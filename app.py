from flask import Flask, jsonify, request
from flask_debugtoolbar import DebugToolbarExtension
from models import Cupcake, db, connect_db


app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
debug = DebugToolbarExtension(app)

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['JSON_SORT_KEYS'] = False

connect_db(app)

"""Flask app for Cupcakes"""

@app.route("/api/cupcakes")
def get_cupcakes():
    cupcakes = Cupcake.query.all()
    cupcakes = [cupcake.serialise() for cupcake in cupcakes]
    return jsonify(cupcakes=cupcakes)

@app.route("/api/cupcakes/<int:id>")
def get_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialise())

@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json.get("image", "https://tinyurl.com/demo-cupcake")
    
    cupcake = Cupcake(flavor=flavor,
                      size=size,
                      rating=rating,
                      image=image)
    
    db.session.add(cupcake)
    db.session.commit()
    
    json = {"id":cupcake.id,
            "flavor": cupcake.flavor,
            "size": cupcake.size,
            "rating": cupcake.rating,
            "image": cupcake.image }
    
    return (jsonify(cupcake=json), 201)

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def alter_cupcakes(cupcake_id):
    
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    
    cupcake.flavor = request.json.get("flavor", cupcake.flavor)
    cupcake.size = request.json.get("size", cupcake.size)
    cupcake.rating = request.json.get("rating", cupcake.rating)
    cupcake.image = request.json.get("image", cupcake.image)
    
    db.session.commit()
    
    json = {"id":cupcake.id,
            "flavor": cupcake.flavor,
            "size": cupcake.size,
            "rating": cupcake.rating,
            "image": cupcake.image }
    
    return jsonify(cupcake=json)

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    
    Cupcake.query.get_or_404(cupcake_id)
    Cupcake.query.filter(Cupcake.id==cupcake_id).delete()
    db.session.commit()
    return jsonify({"message": "Deleted"})
    