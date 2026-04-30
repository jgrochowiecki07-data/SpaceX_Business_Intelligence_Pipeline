import requests

def get_url():
    try:
        url = "https://api.spacexdata.com/v5/launches/past"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()

        print(f"Error Connection {response.status_code}")
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []

def fetch_latest_launch():
    try:
        data = get_url()

        if not data:
            return []

        return data
    except Exception as e:
        print(f"Error: {e}")
        return None