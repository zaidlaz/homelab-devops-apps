# My Recipes - Flask Recipe Manager

A beautiful, feature-rich Flask web application for managing your recipe collections. Create, organize, search, and share recipes with an intuitive web interface. Designed for both local development and production Kubernetes deployments with HTTPS support.

## Features

- **Recipe Management**: Create, view, edit, and delete recipes with rich metadata (prep time, cook time, servings, category, tags)
- **Collections**: Organize recipes into named collections for easy grouping
- **Search & Filter**: Full-text search by title, description, or tags; filter by category and collection
- **Import/Export**: Import recipes from JSON files and export individual recipes, collections, or your entire library
- **Responsive Design**: Clean, modern UI that works beautifully on desktop, tablet, and mobile
- **Persistent Storage**: SQLite database with persistent volumes for data and file uploads
- **Automated Backups**: Scheduled daily backups of database and uploads via Kubernetes CronJob
- **HTTPS Ready**: Kubernetes Ingress with TLS termination via cert-manager and Traefik

## Technology Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Python 3.12, Flask 3.x, Flask-SQLAlchemy, Flask-WTF, Gunicorn |
| **Database** | SQLite (persistent via PVC in Kubernetes) |
| **Frontend** | Jinja2 templates, custom CSS/JS |
| **Container** | Docker (python:3.12-slim) |
| **Orchestration** | Kubernetes |
| **Ingress / TLS** | Traefik + cert-manager (cluster issuer: `homelab-ca-issuer`) |
| **Storage** | local-path StorageClass (2Gi data, 5Gi uploads, 5Gi backups) |

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

The app will be available at `http://localhost:5000`.

### Docker Compose

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

The app will be available at `http://localhost:5001`.

### Kubernetes Deployment (Production)

All manifests are located in `k8s-apps/my_recipe/`.

```bash
# 1. Apply namespace and secrets
kubectl apply -f k8s-apps/my_recipe/namespace.yaml
kubectl apply -f k8s-apps/my_recipe/secret.yaml

# 2. Apply persistent storage
kubectl apply -f k8s-apps/my_recipe/pvc-data.yaml
kubectl apply -f k8s-apps/my_recipe/pvc-uploads.yaml
kubectl apply -f k8s-apps/my_recipe/backup-pvc.yaml

# 3. Deploy application
kubectl apply -f k8s-apps/my_recipe/deployment.yaml
kubectl apply -f k8s-apps/my_recipe/service.yaml

# 4. Configure HTTPS ingress
kubectl apply -f k8s-apps/my_recipe/ingress.yaml

# 5. Enable automated backups
kubectl apply -f k8s-apps/my_recipe/backup-cronjob.yaml
```

The application will be available at `https://recipe.lab` (TLS secured via cert-manager).

#### Kubernetes Architecture

| Resource | Purpose |
|----------|---------|
| `Namespace` | `my-recipe` — isolates all application resources |
| `Deployment` | Runs the Flask app container (`zaid/my-recipe:<sha>`) |
| `Service` | ClusterIP exposing port 5000 |
| `Ingress` | Traefik ingress with TLS (`recipe-lab-tls`) for `recipe.lab` |
| `Secret` | Stores `SECRET_KEY` for Flask sessions |
| `PVC` (data) | 2Gi persistent SQLite database |
| `PVC` (uploads) | 5Gi persistent file uploads |
| `PVC` (backup) | 5Gi backup storage for CronJob |
| `CronJob` | Daily at 02:00 — backs up `recipes.db` and `/uploads` |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | `dev-secret-key-change-in-production` | Flask secret key (required in production) |
| `DATA_DIR` | `/app/data` | Path to SQLite database directory |
| `UPLOAD_FOLDER` | `/app/uploads` | Path to file uploads directory |
| `DATABASE_URL` | — | Optional full database URI (overrides `DATA_DIR`) |
| `FLASK_ENV` | `production` | Flask environment mode |

## Project Structure

```
my_recipe/
├── app.py                  # Main Flask application (routes, views)
├── config.py               # Configuration settings & environment loader
├── models.py               # SQLAlchemy models (Recipe, Collection)
├── forms.py                # WTForms form definitions
├── requirements.txt        # Python dependencies
├── Dockerfile              # Container image definition
├── docker-compose.yml      # Local Docker Compose stack
├── entrypoint.sh           # Container startup script (init DB + gunicorn)
├── README.md               # This file
├── data/                   # SQLite database (persistent in Docker/K8s)
├── instance/               # Flask instance folder
├── uploads/                # Uploaded files (persistent in Docker/K8s)
├── static/
│   ├── css/style.css       # Application styles
│   └── js/main.js          # Application scripts
└── templates/              # Jinja2 HTML templates
    ├── base.html
    ├── index.html
    ├── view_recipe.html
    ├── create_recipe.html
    ├── edit_recipe.html
    ├── collections.html
    ├── view_collection.html
    ├── create_collection.html
    ├── edit_collection.html
    ├── import.html
    ├── 404.html
    └── 500.html

k8s-apps/my_recipe/         # Kubernetes manifests
├── namespace.yaml
├── secret.yaml
├── pvc-data.yaml
├── pvc-uploads.yaml
├── backup-pvc.yaml
├── deployment.yaml
├── service.yaml
├── ingress.yaml
└── backup-cronjob.yaml
```
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

## Dashboard Preview

![My Recipe Dashboard](my_recipe/docs/screenshots/myrecipe-dashboard.png)

## License

MIT License
