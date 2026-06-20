# Capturing your evidence — run this yourself

Everything below is real, tested code. Run these commands yourself so the terminal output
and screenshots are genuinely yours — that's what the rubric is checking for.

## 0. Setup (once)

```bash
cd server
pip install -r requirements.txt
python manage.py migrate
python seed.py
```

## 1. Task 2 — django_server.txt

```bash
python manage.py runserver
```

Copy the terminal output (it will show `Django version 6.0.6, using settings 'carsdealership.settings'`
and `Starting development server at http://127.0.0.1:8000/`). Save it as `evidence/django_server.txt`.
Leave this terminal running and open a **second terminal** for the rest.

## 2. Tasks 5 & 6 — loginuser.txt / logoutuser.txt

```bash
curl -i -c cookies.txt -X POST -H "Content-Type: application/json" \
  -d '{"username":"demo","password":"Demo123!"}' \
  http://127.0.0.1:8000/djangoapp/login

curl -i -b cookies.txt http://127.0.0.1:8000/djangoapp/logout
```

Save each command + its output into `evidence/loginuser.txt` and `evidence/logoutuser.txt`.

## 3. Tasks 8–11, 14–16 — dealer/car/sentiment API evidence

```bash
curl http://127.0.0.1:8000/djangoapp/reviews/dealer/1        # getdealerreviews
curl http://127.0.0.1:8000/djangoapp/get_dealers              # getalldealers
curl http://127.0.0.1:8000/djangoapp/dealer/1                 # getdealerbyid
curl "http://127.0.0.1:8000/djangoapp/get_dealers?state=KS"   # getdealersbyState
curl http://127.0.0.1:8000/djangoapp/get_cars                 # getallcarmakes
curl "http://127.0.0.1:8000/djangoapp/analyze/Fantastic%20services"  # analyzereview
```

Save each into its named evidence file.

## 4. Tasks 12 & 13 — admin_login.png / admin_logout.png

1. Open `http://127.0.0.1:8000/admin` in your browser.
2. Log in with `root` / `root123`. Screenshot the Django administration dashboard → `admin_login.png`.
3. Click **Log out** in the admin. Screenshot the admin login screen → `admin_logout.png`.

## 5. Tasks 17–20 — dealer browsing screenshots

1. Visit `http://127.0.0.1:8000/` while logged out → screenshot → `get_dealers.png`.
2. Log in with `demo` / `Demo123!` at `/login`. Visit `/` again — you should see
   "Hi, demo" and a **Review dealer** button → screenshot, with the URL bar visible → `get_dealers_loggedin.png`.
3. Visit `http://127.0.0.1:8000/?state=KS` → screenshot with URL visible → `dealersbystate.png`.
4. Visit `http://127.0.0.1:8000/dealer/1` → screenshot with URL visible → `dealer_id_reviews.png`.

## 6. Tasks 21 & 22 — posting a review

1. From the dealer page, click **Post a review** (`/review/1`). Fill in the form but
   **don't submit yet** → screenshot → `dealership_review_submission.png`.
2. Click **Submit review**. You'll land back on `/dealer/1` with your new review showing
   → screenshot → `added_review.png`.

## 7. Task 23 — CI/CD evidence

1. Create a public GitHub repo and push this project (the workflow file is already at
   `.github/workflows/ci.yml`).
2. Open the **Actions** tab, let it run, and copy the successful run's log into `evidence/CICD.txt`.

## 8. Tasks 24–28 — deployment

1. Build and push the Docker image, then deploy it to IBM Cloud Code Engine:
   ```bash
   docker build -t roadstar .
   ibmcloud ce application create --name roadstar --image <your-registry>/roadstar
   ```
2. Save the public app URL to `evidence/deploymentURL`.
3. Repeat the same four screenshots from steps 5–6 (landing page, logged-in page, dealer
   detail, posted review) but against your **live** Code Engine URL instead of localhost,
   named `deployed_landingpage.png`, `deployed_loggedin.png`, `deployed_dealer_detail.png`,
   `deployed_add_review.png`.
