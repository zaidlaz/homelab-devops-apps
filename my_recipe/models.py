from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Recipe(db.Model):
    __tablename__ = 'recipes'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    ingredients = db.Column(db.Text, nullable=False)  # JSON string
    instructions = db.Column(db.Text, nullable=False)  # JSON string
    prep_time = db.Column(db.Integer, nullable=True)  # minutes
    cook_time = db.Column(db.Integer, nullable=True)  # minutes
    servings = db.Column(db.Integer, nullable=True)
    category = db.Column(db.String(100), nullable=True)
    tags = db.Column(db.Text, nullable=True)  # JSON string
    image_url = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign key to collection
    collection_id = db.Column(db.Integer, db.ForeignKey('collections.id'), nullable=True)
    collection = db.relationship('Collection', back_populates='recipes')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'ingredients': json.loads(self.ingredients) if self.ingredients else [],
            'instructions': json.loads(self.instructions) if self.instructions else [],
            'prep_time': self.prep_time,
            'cook_time': self.cook_time,
            'servings': self.servings,
            'category': self.category,
            'tags': json.loads(self.tags) if self.tags else [],
            'image_url': self.image_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'collection_id': self.collection_id
        }
    
    def __repr__(self):
        return f'<Recipe {self.title}>'


class Collection(db.Model):
    __tablename__ = 'collections'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    recipes = db.relationship('Recipe', back_populates='collection', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'recipe_count': len(self.recipes)
        }
    
    def __repr__(self):
        return f'<Collection {self.name}>'
