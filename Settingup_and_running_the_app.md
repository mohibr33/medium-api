# Setting Up and Running the App

This guide explains how to set up and run the Medium Search API (`app.py`) locally on your machine.

## 1. Prerequisites

Ensure you have Python installed. You can check by running:
```bash
python --version
```

## 2. Install Dependencies

Open your terminal in the project folder and run:

```bash
pip install -r api_requirements.txt
```
*(This installs Flask, Pandas, and Gunicorn)*

## 3. Run the Application

Start the API server by running:

```bash
python app.py
```

You should see output indicating the server is running, usually on port 5000:
`Running on http://127.0.0.1:5000`

## 4. Test the API

Open your web browser and visit:

*   **Home Page**: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
*   **Search Example**: [http://127.0.0.1:5000/search?query=python](http://127.0.0.1:5000/search?query=python)

## 5. Stop the App

To stop the server, go back to your terminal and press:
`Ctrl + C`
