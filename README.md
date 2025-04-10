# Smart Shopping Recommender

This is a simple AI-powered shopping recommendation system built for your Hackathon.

## How it works:
- Reads customer browsing history from SQLite database
- Uses Ollama (Llama2) model to generate personalized product category suggestions
- Simple and clean Streamlit Web UI

## Setup

1. Install dependencies:
```
pip install -r requirements.txt
```

2. Run the application:
```
streamlit run streamlit_app.py
```

3. Open `http://localhost:8501` in your browser

## Files:
- `db.sqlite` → Contains customer and product data
- `streamlit_app.py` → Streamlit Web UI
- `recommender_core.py` → Core Python logic