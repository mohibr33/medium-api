from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

# Load data
CSV_FILE = 'scrapping_results.csv'
df = None

def load_data():
    global df
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)
            # Ensure claps is numeric for sorting
            # Convert "1.5K" to 1500, "50" to 50, etc.
            def parse_claps(val):
                if pd.isna(val): return 0
                val = str(val).upper().replace(',', '')
                if 'K' in val:
                    return float(val.replace('K', '')) * 1000
                try:
                    return float(val)
                except:
                    return 0
            
            df['claps_numeric'] = df['claps'].apply(parse_claps)
            print(f"Loaded {len(df)} records")
        except Exception as e:
            print(f"Error loading CSV: {e}")
            df = pd.DataFrame()
    else:
        print("CSV file not found!")
        df = pd.DataFrame()

load_data()

@app.route('/')
def home():
    return "<h1>Medium Search API</h1><p>Use /search?query=keyword to search articles.</p>"

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').lower()
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    if df is None or df.empty:
        return jsonify({'error': 'No data available'}), 500
    
    # Filter data
    # Search in Title, Text, and Keywords
    mask = (
        df['title'].astype(str).str.lower().str.contains(query) |
        df['text'].astype(str).str.lower().str.contains(query) |
        df['keywords'].astype(str).str.lower().str.contains(query)
    )
    
    results = df[mask].copy()
    
    # Sort by claps (descending)
    results = results.sort_values('claps_numeric', ascending=False)
    
    # Take top 10
    top_10 = results.head(10)
    
    # Format response
    response = []
    for _, row in top_10.iterrows():
        response.append({
            'title': row['title'],
            'url': row['url'],
            'claps': int(row['claps_numeric']) if not pd.isna(row['claps_numeric']) else 0
        })
        
    return jsonify({
        'count': len(response),
        'results': response
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
