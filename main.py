from extractor import fetch_latest_launch
from analyzer import calculate_sentiment
from models import LaunchData

def run_pipeline():
    raw_data = fetch_latest_launch()

    if not raw_data:
        return None

    sentiment = calculate_sentiment(raw_data('details', ""))

    try:
        mission = LaunchData(**raw_data, sentiment_score=sentiment)
        print("Success")
        print(mission.model_dump_json(indent=4))
        return mission

    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    run_pipeline()