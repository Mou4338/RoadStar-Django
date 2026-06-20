# RoadStar Cars Dealership

RoadStar is a full-stack dealership capstone application built with Django, SQLite, and React.
Visitors can browse and filter nationwide dealers, read dealer reviews, create an account,
sign in, and submit a sentiment-tagged review of a dealership.

## Tech stack

- **Backend:** Django 6, SQLite, Django admin
- **Frontend:** Django templates (Dealers, About, Contact, Login, Review) + a React
  registration component (`frontend/src/components/Register/Register.jsx`)
- **APIs:** JSON endpoints under `/djangoapp/...` for dealers, reviews, car makes/models,
  login, logout, registration, and sentiment analysis
- **CI/CD:** GitHub Actions (`.github/workflows/ci.yml`)
- **Deployment:** Docker + Kubernetes manifests, deployable to IBM Cloud Code Engine

## Run locally

```bash
cd server
pip install -r requirements.txt
python manage.py migrate
python seed.py          # creates root/demo users, dealers, and car makes
python manage.py runserver
```

Open http://127.0.0.1:8000

- Demo user: `demo` / `Demo123!`
- Admin/superuser: `root` / `root123` (Django admin at `/admin`)

## Project structure

```
server/
  carsdealership/        Django project settings & urls
  djangoapp/              Models, views, admin, API endpoints
  frontend/
    templates/            Dealers / About / Contact / Login / Register / Review pages
    static/                style.css
    src/components/Register/Register.jsx   React registration component
  seed.py                  Seeds demo data
.github/workflows/ci.yml   CI pipeline
Dockerfile
kubernetes/deployment.yaml
```

## API endpoints

- `GET /djangoapp/get_dealers` / `?state=KS`
- `GET /djangoapp/dealer/<id>`
- `GET /djangoapp/reviews/dealer/<id>`
- `GET /djangoapp/get_cars`
- `GET /djangoapp/analyze/<text>`
- `POST /djangoapp/login`, `/djangoapp/logout`, `/djangoapp/register`
