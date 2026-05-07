from transformers import pipeline
# Wdrożenie Systemu AI który mi ocenia na podstawie wrzuconych przez spaceX misji czy misja była dobra czy nie od -1 do 1

classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def calculate_sentiment(text: str):
    if not text or not isinstance(text, str) or text.strip() == "":
        return  0.0


    try:
        result = classifier(text[:512])[0]

        label = result['label']
        score = result['score']

        if label == 'NEGATIVE':
            return -score
        return score

    except Exception as e:
        print(f"Error: {e}")
        return 0.0