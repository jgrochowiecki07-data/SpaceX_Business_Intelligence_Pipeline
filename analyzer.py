from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def calculate_sentiment(text: str):
    try:
        analyzer = SentimentIntensityAnalyzer()
        scores = analyzer.polarity_scores(text)
        return scores['compound']

    except Exception as e:
        print(f"Error: {e}")
        return None