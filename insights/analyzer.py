from transformers import pipeline
import pandas as pd


summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text: str) -> str:
    try:
        if len(text.strip()) < 20:
            return "Not enough text to summarize."
        result = summarizer(text, max_length=100, min_length=25, do_sample=False)
        return result[0]["summary_text"]
    except Exception as e:
        return f"Error generating summary: {e}"

def prepare_summary_text(df: pd.DataFrame) -> str:
    if df.empty:
        return "No data to summarize."

    top_routes = df.groupby(['from', 'to']).size().sort_values(ascending=False).head(3)
    top_airlines = df['airline'].value_counts().head(3)
    flights_over_time = df['departure_time'].dt.date.value_counts().sort_index().tail(3)

    summary = f"""
    Top Routes: {top_routes.to_dict()}
    Top Airlines: {top_airlines.to_dict()}
    Peak Dates: {flights_over_time.to_dict()}
    """
    return summary
