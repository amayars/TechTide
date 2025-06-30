# 🚀 Techtide: Business Idea Analyzer

**Techtide** is an AI-powered business idea analyzer that helps entrepreneurs and innovators validate and explore their startup concepts. It combines sentiment analysis, SWOT insights, domain name suggestions, trend data, and competitor research to generate a detailed PDF report.

---

## 🧠 Features

🔍 **Keyword Extraction**  
Extracts core keywords and noun phrases using `TextBlob`.

💬 **Sentiment Analysis**  
Calculates a Hustle Score and Viral Factor using `TextBlob` and `VADER` sentiment polarity.

📈 **Google Trends Analysis**  
Fetches interest data for your idea using `pytrends` to evaluate long-term relevance.

🧩 **SWOT Analysis**  
Automatically identifies:
- Strengths
- Weaknesses
- Opportunities
- Threats  
based on predefined relevant terms.

🌐 **Domain Name Generator + Availability Check**  
Generates creative domain names using your keywords and checks their availability using Python's `socket`.

🏢 **Competitor Research**  
Uses **[SerpAPI](https://serpapi.com/)** to fetch real-time Google search results to identify competitors.

📄 **PDF Report Generation**  
Generates a complete business analysis report in PDF using `fpdf`.

---

## 🛠️ Tech Stack

- Python 3.x
- TextBlob
- VADER SentimentIntensityAnalyzer
- pytrends
- FPDF
- SerpAPI
- Socket
- Requests

---

## 🗂️ Project Structure

