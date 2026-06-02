from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectField, FieldList, FormField
from wtforms.validators import DataRequired, Optional, Length, NumberRange


class IngredientForm(FlaskForm):
    name = StringField('Ingredient', validators=[DataRequired(), Length(max=200)])
    amount = StringField('Amount', validators=[Optional(), Length(max=100)])
    unit = StringField('Unit', validators=[Optional(), Length(max=50)])


class InstructionForm(FlaskForm):
    step = TextAreaField('Step', validators=[DataRequired()])


class RecipeForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[Optional()])
    ingredients = TextAreaField('Ingredients (one per line)', validators=[DataRequired()])
    instructions = TextAreaField('Instructions (one step per line)', validators=[DataRequired()])
    prep_time = IntegerField('Prep Time (minutes)', validators=[Optional(), NumberRange(min=0)])
    cook_time = IntegerField('Cook Time (minutes)', validators=[Optional(), NumberRange(min=0)])
    servings = IntegerField('Servings', validators=[Optional(), NumberRange(min=1)])
    category = SelectField('Category', choices=[
        ('', 'Select Category'),
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
    ], validators=[Optional()])
    tags = StringField('Tags (comma separated)', validators=[Optional(), Length(max=500)])
    image_url = StringField('Image URL', validators=[Optional(), Length(max=500)])
    collection_id = SelectField('Collection', coerce=int, validators=[Optional()])


class CollectionForm(FlaskForm):
    name = StringField('Collection Name', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[Optional()])
