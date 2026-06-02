# My Recipes - Flask Recipe Manager

A beautiful, feature-rich Flask web application for managing your recipe collections. Upload, download, update, and delete recipes with an intuitive web interface.

## Features

- **Recipe Management**: Create, view, edit, and delete recipes
- **Collections**: Organize recipes into collections
- **Search & Filter**: Search by title, description, or tags; filter by category and collection
- **Import/Export**: Import recipes from JSON files and export individual recipes, collections, or all recipes
- **Responsive Design**: Works beautifully on desktop, tablet, and mobile
- **Modern UI**: Clean, modern interface with smooth animations

## Quick Start

### Option 1: Docker (Recommended)

The easiest way to run the app is with Docker Compose:

```bash
# Build and start the container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

The app will be available at `http://localhost:5000`

Data is persisted in Docker volumes (`recipe-data` and `recipe-uploads`).

#### Docker Environment Variables

You can customize the container by setting environment variables in `docker-compose.yml` or a `.env` file:

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | `change-me-in-production` | Flask secret key |
| `DATABASE_URL` | `sqlite:///data/recipes.db` | Database connection string |

#### Building the Docker Image

```bash
# Build the image
docker build -t my-recipes .

# Run the container
docker run -d -p 5000:5000 -v recipe-data:/app/data -v recipe-uploads:/app/uploads my-recipes
```

### Option 2: Local Development

#### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 2. Set Up Environment (Optional)

Copy the example environment file and customize:

```bash
cp .env.example .env
```

#### 3. Run the Application

```bash
python app.py
```

The app will be available at `http://localhost:5000`

#### 4. Initialize Database (Optional)

If you want to initialize the database manually:

```bash
flask --app app init-db
```

## Project Structure

```
my_recipe_app/
├── app.py                  # Main Flask application
├── config.py               # Configuration settings
├── models.py               # Database models (Recipe, Collection)
├── forms.py                # WTForms form definitions
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker image definition
├── docker-compose.yml      # Docker Compose configuration
├── entrypoint.sh           # Docker container startup script
├── .env.example            # Example environment variables
├── templates/              # HTML templates
│   ├── base.html           # Base layout
│   ├── index.html          # Home page with recipe grid
│   ├── view_recipe.html    # Recipe detail page
│   ├── create_recipe.html  # Create recipe form
│   ├── edit_recipe.html    # Edit recipe form
│   ├── collections.html    # Collections list
│   ├── view_collection.html # Collection detail
│   ├── create_collection.html
│   ├── edit_collection.html
│   ├── import.html         # Import recipes
│   ├── 404.html            # Not found page
│   └── 500.html            # Server error page
├── static/
│   ├── css/
│   │   └── style.css       # Main stylesheet
│   └── js/
│       └── main.js         # JavaScript utilities
└── uploads/                # Upload directory (created automatically)
```

## Data Model

### Recipe
- `title` - Recipe name
- `description` - Brief description
- `ingredients` - List of ingredients (JSON)
- `instructions` - Step-by-step instructions (JSON)
- `prep_time` - Preparation time in minutes
- `cook_time` - Cooking time in minutes
- `servings` - Number of servings
- `category` - Recipe category
- `tags` - Tags for searching (JSON)
- `image_url` - URL to recipe image
- `collection_id` - Associated collection

### Collection
- `name` - Collection name
- `description` - Collection description
- `recipes` - Associated recipes (relationship)

## Import Format

The app supports importing recipes from JSON files in these formats:

### Single Recipe
```json
{
  "title": "Chocolate Cake",
  "description": "A delicious chocolate cake",
  "ingredients": ["2 cups flour", "1 cup sugar", "3 eggs"],
  "instructions": ["Preheat oven to 350°F", "Mix ingredients", "Bake for 30 minutes"],
  "prep_time": 20,
  "cook_time": 30,
  "servings": 8,
  "category": "dessert",
  "tags": ["baking", "chocolate"],
  "image_url": "https://example.com/cake.jpg"
}
```

### Collection Export
```json
{
  "name": "Desserts",
  "description": "Sweet treats",
  "recipes": [
    { ... recipe object ... },
    { ... recipe object ... }
  ]
}
```

### Array of Recipes
```json
[
  { ... recipe object ... },
  { ... recipe object ... }
]
```

## API Endpoints

The app also provides JSON API endpoints:

- `GET /api/recipes` - List all recipes
- `GET /api/recipe/<id>` - Get a specific recipe
- `GET /api/collections` - List all collections

## Categories

Recipes can be categorized as:
- Appetizer
- Main Course
- Dessert
- Breakfast
- Lunch
- Dinner
- Snack
- Beverage
- Soup
- Salad
- Side Dish
- Baking
- Other

## Development

### Running in Debug Mode

The app runs in debug mode by default when executed directly:

```bash
python app.py
```

### Production Deployment

For production, set `SECRET_KEY` in your environment and disable debug mode:

```bash
export SECRET_KEY="your-secure-secret-key"
export FLASK_ENV=production
```

## License

MIT License
