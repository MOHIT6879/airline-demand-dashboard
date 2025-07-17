# ✈️ Airline Booking Market Demand Dashboard

A Streamlit web app that visualizes real-time airline booking market trends using data from the AviationStack API. Includes filters, charts, AI-generated insights, and CSV export.

---

## 📌 Features

- ✅ Fetch live flight data (with caching)
- ✅ Filter by airline and route
- ✅ Display top 10 most popular routes
- ✅ View flight volume trends over time
- ✅ Detailed flight-level data table
- ✅ Export filtered data to CSV
- ✅ AI-generated summary insights (offline/local model)

---

## 📂 Project Structure

airline-demand-app/
│
├── app.py # Streamlit main app
│
├── data/
│ └── processor.py # Data processing and filtering
│
├── insights/
│ └── analyzer.py # AI summarizer logic
│
├── utils/
│ └── download.py # CSV export helper
│
├── flights.json # Cached data from API (optional)
├── requirements.txt # Python dependencies
└── README.md 

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/airline-demand-dashboard.git
cd airline-demand-dashboard

python -m venv venv
# Activate it:
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
streamlit run app.py

🔐 API Key Configuration
✈️ AviationStack API
This app uses the AviationStack API for real-time flight data(100 free api calls per month).

Sign up at https://aviationstack.com

Copy your API key

Replace it in app.py:

API_KEY = "YOUR_API_KEY_HERE"

🧠 AI-Generated Insights (Locally Run)

Uses the facebook/bart-large-cnn model via the Hugging Face transformers library (runs locally)

No Hugging Face token or internet access is required for summarization

Summarizes:

Top 3 most popular routes

Top 3 airlines by frequency

Recent peak flight dates

⚠️ First-time usage downloads the model from Hugging Face once, then cache locally.

💾 Sample Output Screens

✅ **Top Routes Bar Chart**  
![Top Routes](screenshots/top_routes.png)

✅ **Most Frequent Routes**  
![Flight Time Chart](screenshots/bar.png)

✅ **AI-generated Trend Summary and Download CSV**  
![AI Summary](screenshots/ai_summary.png)

✅ **Full Flight Table**  
![Flight Table](screenshots/full_table.png)