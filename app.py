import pandas as pd
from fastapi import FastAPI, Depends
from extractor import fetch_latest_launch
from analyzer import calculate_sentiment
import matplotlib.pyplot as plt
import io
from fastapi.responses import StreamingResponse
from database import engine, Base, SessionLocal, LaunchDB
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def interpret_sentiment(score: float) -> str:
        if score > 0.5:
            return "Excellent"
        elif score > 0:
            return "Good"
        elif score == 0:
            return "Neutral"
        elif score > -0.5:
            return "Bad"
        else:
            return "Very Bad"

app = FastAPI()

@app.get("/analyze")
def get_spacex_analysis(db: Session = Depends(get_db)):
    try:
        raw_data = fetch_latest_launch()
        df = pd.DataFrame(raw_data)

        if 'details' not in df.columns:
            return {"error": "Missing 'details' column in API response", "available_columns": list(df.columns)}

        df = df.dropna(subset=['details'])
        df['details'] = df['details'].str.strip()

        df['sentiment'] = df['details'].apply(calculate_sentiment)
        df['sentiment_label'] = df['sentiment'].apply(interpret_sentiment)

        df_final = df[['name', 'details', 'success', 'sentiment', 'sentiment_label']].tail(30)

        for index, row in df_final.iterrows():
            db_launch = LaunchDB(
                name=row['name'],
                details=row['details'],
                success=bool(row['success']),
                sentiment=float(row['sentiment']),
                sentiment_label=str(row['sentiment_label'])
            )
            db.add(db_launch)

        db.commit()
        return df_final.to_dict(orient='records')

    except Exception as e:
        return f"Error: {str(e)}"

@app.get("/stats")
def get_spaces_stats():
    try:
        raw_data = fetch_latest_launch()
        df = pd.DataFrame(raw_data)

        df = df.dropna(subset=['details'])
        df['details'] = df['details'].str.strip()
        df['sentiment'] = df['details'].apply(calculate_sentiment)

        avg_total = df['sentiment'].mean()
        stats_by_success = df.groupby('success')['sentiment'].mean().to_dict()

        df['year'] = pd.to_datetime(df['date_utc']).dt.year
        yearly_stats = df.groupby('year')['sentiment'].mean().to_dict()

        return {
            "average_sentiment_total": round(avg_total, 4),
            "stats_by_success": stats_by_success,
            "mission_count": len(df),
            "yearly_stats": yearly_stats
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/chart")
def get_spaces_chart():
    try:
        raw_data = fetch_latest_launch()
        df = pd.DataFrame(raw_data)

        df = df.dropna(subset=['details'])
        df['details'] = df['details'].str.strip()
        df['sentiment'] = df['details'].apply(calculate_sentiment)

        df['year'] = pd.to_datetime(df['date_utc']).dt.year
        yearly_stats = df.groupby('year')['sentiment'].mean()

        plt.figure(figsize=(10, 5))
        plt.plot(yearly_stats.index, yearly_stats.values, marker='o', color='royalblue', linewidth=2)
        plt.title('Spacex analys per years')
        plt.xlabel('Year')
        plt.ylabel('AVG Sentiment')
        plt.grid(True, linestyle='--', alpha=0.7)

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        return StreamingResponse(buf, media_type='image/png')

    except Exception as e:
        return {"error": str(e)}
