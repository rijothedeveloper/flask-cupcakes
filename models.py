from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class Cupcake(db.Model):
    """Models for Cupcake app."""
    
    __tablename__ = "cupcakes"
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    flavor = db.Column(db.String,
                       nullable=False)
    
    size = db.Column(db.String,
                       nullable=False)
    
    rating = db.Column(db.Float,
                       nullable=False)
    
    image = db.Column(db.String,
                       nullable=False,
                       default="https://tinyurl.com/demo-cupcake")