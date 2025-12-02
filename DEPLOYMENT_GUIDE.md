# How to Deploy Your Medium Search API for Free

This guide shows you how to host your API on **Render.com** (a free cloud hosting platform).

## 1. Prerequisites (You have these ready)

Ensure you have these 4 files in a folder:
1. `app.py` (The API code)
2. `scrapping_results.csv` (Your data)
3. `api_requirements.txt` (List of libraries)
4. `Procfile` (Deployment instruction)

## 2. Upload to GitHub

Render needs your code to be on GitHub first.

1. Create a new repository on [GitHub.com](https://github.com).
2. Name it `medium-api`.
3. Upload the 4 files above to this repository.

## 3. Deploy on Render (Free)

1. Go to [dashboard.render.com](https://dashboard.render.com) and sign up/login.
2. Click **New +** and select **Web Service**.
3. Connect your GitHub account and select your `medium-api` repository.
4. Scroll down to configure:
   - **Name**: `my-medium-api` (or any name)
   - **Region**: Any (e.g., Frankfurt)
   - **Branch**: `main` (or master)
   - **Root Directory**: (Leave blank)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r api_requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: Select **Free**

5. Click **Create Web Service**.

## 4. Wait for Deployment

Render will start building your app. It takes about 2-5 minutes.
Watch the logs. When you see "Your service is live", it's ready!

## 5. Use Your API

Your API URL will be something like: `https://my-medium-api.onrender.com`

**Test it in your browser:**
Search for "python":
`https://my-medium-api.onrender.com/search?query=python`

Search for "data":
`https://my-medium-api.onrender.com/search?query=data`

It will return the top 10 articles sorted by claps!
