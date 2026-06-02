import os
import json
import csv
import io
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify
from werkzeug.utils import secure_filename

from config import Config
from models import db, Recipe, Collection
from forms import RecipeForm, CollectionForm

app = Flask(__name__)
app.config.from_object(Config)

# Custom Jinja2 filters
@app.template_filter('from_json')
def from_json(value):
    if not value:
        return []
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return []

# Initialize extensions
db.init_app(app)

# Create upload directory
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


# Context processor for template globals
@app.context_processor
def inject_globals():
    return {
        'categories': [
            ('appetizer', 'Appetizer'),
            ('main_course', 'Main Course'),
            ('dessert', 'Dessert'),
            ('breakfast', 'Breakfast'),
            ('lunch', 'Lunch'),
            ('dinner', 'Dinner'),
            ('snack', 'Snack'),
            ('beverage', 'Beverage'),
            ('soup', 'Soup'),
            ('salad', 'Salad'),
            ('side_dish', 'Side Dish'),
            ('baking', 'Baking'),
            ('other', 'Other')
        ]
    }


# ==================== HOME & SEARCH ====================

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    collection_id = request.args.get('collection_id', type=int)
    
    query = Recipe.query
    
    if search:
        query = query.filter(
            db.or_(
                Recipe.title.ilike(f'%{search}%'),
                Recipe.description.ilike(f'%{search}%'),
                Recipe.tags.ilike(f'%{search}%')
            )
        )
    
    if category:
        query = query.filter_by(category=category)
    
    if collection_id:
        query = query.filter_by(collection_id=collection_id)
    
    recipes = query.order_by(Recipe.created_at.desc()).paginate(
        page=page, per_page=12, error_out=False
    )
    
    collections = Collection.query.order_by(Collection.name).all()
    
    return render_template('index.html', recipes=recipes, collections=collections,
                         search=search, category=category, selected_collection=collection_id)


# ==================== RECIPES CRUD ====================

@app.route('/recipe/<int:recipe_id>')
def view_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template('view_recipe.html', recipe=recipe)


@app.route('/recipe/create', methods=['GET', 'POST'])
def create_recipe():
    form = RecipeForm()
    form.collection_id.choices = [(0, 'None')] + [
        (c.id, c.name) for c in Collection.query.order_by(Collection.name).all()
    ]
    
    if form.validate_on_submit():
        ingredients = [line.strip() for line in form.ingredients.data.split('\n') if line.strip()]
        instructions = [line.strip() for line in form.instructions.data.split('\n') if line.strip()]
        tags = [tag.strip() for tag in form.tags.data.split(',') if tag.strip()] if form.tags.data else []
        
        recipe = Recipe(
            title=form.title.data,
            description=form.description.data,
            ingredients=json.dumps(ingredients),
            instructions=json.dumps(instructions),
            prep_time=form.prep_time.data,
            cook_time=form.cook_time.data,
            servings=form.servings.data,
            category=form.category.data,
            tags=json.dumps(tags),
            image_url=form.image_url.data,
            collection_id=form.collection_id.data if form.collection_id.data != 0 else None
        )
        
        db.session.add(recipe)
        db.session.commit()
        
        flash('Recipe created successfully!', 'success')
        return redirect(url_for('view_recipe', recipe_id=recipe.id))
    
    return render_template('create_recipe.html', form=form, title='Create Recipe')


@app.route('/recipe/<int:recipe_id>/edit', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    form = RecipeForm(obj=recipe)
    form.collection_id.choices = [(0, 'None')] + [
        (c.id, c.name) for c in Collection.query.order_by(Collection.name).all()
    ]
    
    if request.method == 'GET':
        form.ingredients.data = '\n'.join(json.loads(recipe.ingredients)) if recipe.ingredients else ''
        form.instructions.data = '\n'.join(json.loads(recipe.instructions)) if recipe.instructions else ''
        form.tags.data = ', '.join(json.loads(recipe.tags)) if recipe.tags else ''
        form.collection_id.data = recipe.collection_id or 0
    
    if form.validate_on_submit():
        ingredients = [line.strip() for line in form.ingredients.data.split('\n') if line.strip()]
        instructions = [line.strip() for line in form.instructions.data.split('\n') if line.strip()]
        tags = [tag.strip() for tag in form.tags.data.split(',') if tag.strip()] if form.tags.data else []
        
        recipe.title = form.title.data
        recipe.description = form.description.data
        recipe.ingredients = json.dumps(ingredients)
        recipe.instructions = json.dumps(instructions)
        recipe.prep_time = form.prep_time.data
        recipe.cook_time = form.cook_time.data
        recipe.servings = form.servings.data
        recipe.category = form.category.data
        recipe.tags = json.dumps(tags)
        recipe.image_url = form.image_url.data
        recipe.collection_id = form.collection_id.data if form.collection_id.data != 0 else None
        recipe.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        flash('Recipe updated successfully!', 'success')
        return redirect(url_for('view_recipe', recipe_id=recipe.id))
    
    return render_template('edit_recipe.html', form=form, recipe=recipe, title='Edit Recipe')


@app.route('/recipe/<int:recipe_id>/delete', methods=['POST'])
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    flash('Recipe deleted successfully!', 'success')
    return redirect(url_for('index'))


# ==================== COLLECTIONS CRUD ====================

@app.route('/collections')
def list_collections():
    collections = Collection.query.order_by(Collection.name).all()
    return render_template('collections.html', collections=collections)


@app.route('/collection/<int:collection_id>')
def view_collection(collection_id):
    collection = Collection.query.get_or_404(collection_id)
    page = request.args.get('page', 1, type=int)
    recipes = Recipe.query.filter_by(collection_id=collection_id).order_by(
        Recipe.created_at.desc()
    ).paginate(page=page, per_page=12, error_out=False)
    return render_template('view_collection.html', collection=collection, recipes=recipes)


@app.route('/collection/create', methods=['GET', 'POST'])
def create_collection():
    form = CollectionForm()
    
    if form.validate_on_submit():
        collection = Collection(
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(collection)
        db.session.commit()
        
        flash('Collection created successfully!', 'success')
        return redirect(url_for('view_collection', collection_id=collection.id))
    
    return render_template('create_collection.html', form=form)


@app.route('/collection/<int:collection_id>/edit', methods=['GET', 'POST'])
def edit_collection(collection_id):
    collection = Collection.query.get_or_404(collection_id)
    form = CollectionForm(obj=collection)
    
    if form.validate_on_submit():
        collection.name = form.name.data
        collection.description = form.description.data
        collection.updated_at = datetime.utcnow()
        db.session.commit()
        
        flash('Collection updated successfully!', 'success')
        return redirect(url_for('view_collection', collection_id=collection.id))
    
    return render_template('edit_collection.html', form=form, collection=collection)


@app.route('/collection/<int:collection_id>/delete', methods=['POST'])
def delete_collection(collection_id):
    collection = Collection.query.get_or_404(collection_id)
    db.session.delete(collection)
    db.session.commit()
    flash('Collection deleted successfully!', 'success')
    return redirect(url_for('list_collections'))


# ==================== IMPORT / EXPORT ====================

@app.route('/export/recipe/<int:recipe_id>')
def export_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    data = recipe.to_dict()
    
    filename = secure_filename(f"{recipe.title}.json")
    return send_file(
        io.BytesIO(json.dumps(data, indent=2).encode()),
        mimetype='application/json',
        as_attachment=True,
        download_name=filename
    )


@app.route('/export/collection/<int:collection_id>')
def export_collection(collection_id):
    collection = Collection.query.get_or_404(collection_id)
    data = {
        'name': collection.name,
        'description': collection.description,
        'recipes': [r.to_dict() for r in collection.recipes]
    }
    
    filename = secure_filename(f"{collection.name}_collection.json")
    return send_file(
        io.BytesIO(json.dumps(data, indent=2).encode()),
        mimetype='application/json',
        as_attachment=True,
        download_name=filename
    )


@app.route('/export/all')
def export_all():
    recipes = Recipe.query.all()
    data = {
        'export_date': datetime.utcnow().isoformat(),
        'recipe_count': len(recipes),
        'recipes': [r.to_dict() for r in recipes]
    }
    
    return send_file(
        io.BytesIO(json.dumps(data, indent=2).encode()),
        mimetype='application/json',
        as_attachment=True,
        download_name='all_recipes.json'
    )


@app.route('/import', methods=['GET', 'POST'])
def import_recipes():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            try:
                content = file.read().decode('utf-8')
                data = json.loads(content)
                
                imported_count = 0
                
                # Handle single recipe
                if 'title' in data and 'ingredients' in data:
                    recipes_data = [data]
                # Handle collection export
                elif 'recipes' in data:
                    recipes_data = data['recipes']
                # Handle array of recipes
                elif isinstance(data, list):
                    recipes_data = data
                else:
                    flash('Invalid file format', 'error')
                    return redirect(request.url)
                
                for recipe_data in recipes_data:
                    recipe = Recipe(
                        title=recipe_data.get('title', 'Untitled'),
                        description=recipe_data.get('description', ''),
                        ingredients=json.dumps(recipe_data.get('ingredients', [])),
                        instructions=json.dumps(recipe_data.get('instructions', [])),
                        prep_time=recipe_data.get('prep_time'),
                        cook_time=recipe_data.get('cook_time'),
                        servings=recipe_data.get('servings'),
                        category=recipe_data.get('category', ''),
                        tags=json.dumps(recipe_data.get('tags', [])),
                        image_url=recipe_data.get('image_url', '')
                    )
                    db.session.add(recipe)
                    imported_count += 1
                
                db.session.commit()
                flash(f'Successfully imported {imported_count} recipe(s)!', 'success')
                return redirect(url_for('index'))
                
            except Exception as e:
                db.session.rollback()
                flash(f'Error importing file: {str(e)}', 'error')
                return redirect(request.url)
        else:
            flash('Invalid file type. Please upload a JSON file.', 'error')
            return redirect(request.url)
    
    return render_template('import.html')


# ==================== API ENDPOINTS ====================

@app.route('/api/recipes')
def api_recipes():
    recipes = Recipe.query.all()
    return jsonify([r.to_dict() for r in recipes])


@app.route('/api/recipe/<int:recipe_id>')
def api_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return jsonify(recipe.to_dict())


@app.route('/api/collections')
def api_collections():
    collections = Collection.query.all()
    return jsonify([c.to_dict() for c in collections])


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


# ==================== INIT DATABASE ====================

@app.cli.command('init-db')
def init_db():
    with app.app_context():
        db.create_all()
    print('Database initialized!')


# Initialize database tables on startup (for Docker/gunicorn)
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
