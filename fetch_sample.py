import requests

url = "https://medium.com/javascript-scene/top-javascript-frameworks-and-topics-to-learn-in-2019-b4142f38df20"
try:
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"})
    response.raise_for_status()
    with open("sample_medium.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    print("Successfully downloaded sample_medium.html")
except Exception as e:
    print(f"Error fetching URL: {e}")
