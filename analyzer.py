from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from fpdf import FPDF
from pytrends.request import TrendReq
from serpapi import GoogleSearch
import random
import socket
import requests
import os

# Constants
STRENGTHS = ["innovative", "ai", "automation", "unique", "scalable", "efficient", "intelligent"]
WEAKNESSES = ["expensive", "complex", "slow", "unclear", "unproven", "limited"]
OPPORTUNITIES = ["demand", "growing", "expansion", "trend", "future", "emerging", "opportunity"]
THREATS = ["competition", "privacy", "risk", "regulations", "barrier", "threat"]
DOMAIN_SUFFIXES = ['.com', '.io', '.app', '.co', '.xyz', '.tech']
SERPAPI_KEY = os.getenv("SERPAPI_KEY") or "your_serpapi_key_here"

# Tools
vader = SentimentIntensityAnalyzer()
pytrends = TrendReq()

# Function: Extract Keywords
def extract_keywords(idea):
    blob = TextBlob(idea)
    return list(set(blob.noun_phrases))

# Function: Generate Domain Names
def generate_domain_names(keywords, idea, count=5):
    domains = set()
    base_words = keywords + idea.lower().split()
    base_words = list(set([w for w in base_words if len(w) > 2]))
    while len(domains) < count:
        name_parts = random.sample(base_words, min(2, len(base_words)))
        prefix = random.choice(['get', 'try', 'go', 'my', 'the', 'best', 'top', 'super', 'smart', 'easy'])
        domain = prefix + ''.join(name_parts) + random.choice(DOMAIN_SUFFIXES)
        domains.add(domain)
    return list(domains)

# Function: Check Domain Availability
def check_domain_availability(domain):
    try:
        socket.gethostbyname(domain)
        return False  # Taken
    except socket.gaierror:
        return True  # Available

# Function: Competitor Search via SerpAPI
def find_competitors(idea):
    if not SERPAPI_KEY or SERPAPI_KEY == "b388b8beb57a5263ced570bfcd1141d1e03710003ea788ea1ec6a3b74bfc704b":
        return ["[!] SerpAPI key not configured."]

    try:
        params = {
            "q": idea,
            "api_key": SERPAPI_KEY,
            "engine": "google",
            "num": 5  # num can be int or string, int preferred
        }
        search = GoogleSearch(params)
        results = search.get_dict().get("organic_results", [])
        
        # Extract title and link for each result
        competitors = [f"{r.get('title', 'No Title')} - {r.get('link', 'No Link')}" for r in results if "title" in r]
        
        return competitors if competitors else ["No clear competitors found."]
    except Exception as e:
        return [f"Error: {str(e)}"]


# Function: Fetch Trend Score from Google Trends
def fetch_trend_data(keyword):
    try:
        pytrends.build_payload([keyword], cat=0, timeframe='today 12-m')
        data = pytrends.interest_over_time()
        if not data.empty:
            trend_score = int(data[keyword].mean())
            return trend_score
    except:
        pass
    return 0

# Function: Export PDF Report
def export_pdf_report(result, filename="business_report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "HustleAnalyzer Business Report", ln=True)
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, f"Hustle Score: {result['hustle_score']} / 100", ln=True)
    pdf.cell(0, 10, f"Viral Factor: {result['viral_factor']} / 10", ln=True)
    pdf.cell(0, 10, f"Trend Score: {result['trend_score']}", ln=True)

    pdf.cell(0, 10, "\nSWOT Analysis:", ln=True)
    for k, v in result['swot'].items():
        pdf.multi_cell(0, 10, f"{k}: {', '.join(v)}")

    pdf.cell(0, 10, "\nDomain Suggestions:", ln=True)
    for domain, status in result['domain_suggestions'].items():
        pdf.cell(0, 10, f"- {domain}: {status}", ln=True)

    pdf.cell(0, 10, "\nCompetitors:", ln=True)
    for comp in result['competitors']:
        pdf.multi_cell(0, 10, f"- {comp}")

    pdf.output(filename)
    return filename

# Main Analysis Function
def analyze_business_idea(idea):
    idea_lower = idea.lower()
    keywords = extract_keywords(idea)

    # Sentiment Scores
    tb_score = TextBlob(idea).sentiment.polarity
    vader_score = vader.polarity_scores(idea)["compound"]
    base_score = int(((tb_score + vader_score) / 2 + 1) * 50)

    # SWOT
    strengths = [w for w in STRENGTHS if w in idea_lower]
    weaknesses = [w for w in WEAKNESSES if w in idea_lower]
    opportunities = [w for w in OPPORTUNITIES if w in idea_lower]
    threats = [w for w in THREATS if w in idea_lower]

    score_adjustment = (len(strengths) + len(opportunities)) * 5 - (len(weaknesses) + len(threats)) * 5
    hustle_score = max(0, min(100, base_score + score_adjustment))
    viral_factor = int((vader_score + 1) * 5)

    # Domain + Competitors + Trends
    domain_suggestions = generate_domain_names(keywords, idea)
    domain_status = {
        d: "Available" if check_domain_availability(d) else "Taken"
        for d in domain_suggestions
    }
    competitors = find_competitors(idea)
    trend_score = fetch_trend_data(keywords[0] if keywords else "startup")

    return {
        "swot": {
            "Strengths": strengths or ["Unique approach"],
            "Weaknesses": weaknesses or ["Needs validation"],
            "Opportunities": opportunities or ["Untapped potential"],
            "Threats": threats or ["Market risk"]
        },
        "hustle_score": hustle_score,
        "viral_factor": viral_factor,
        "keywords": keywords,
        "trend_score": trend_score,
        "domain_suggestions": domain_status,
        "competitors": competitors
    }

# Test Run (Optional)
if __name__ == "__main__":
    idea = input("💡 Enter your business idea: ").strip()
    result = analyze_business_idea(idea)

    print(f"\n🔍 SWOT: {result['swot']}")
    print(f"💡 Hustle Score: {result['hustle_score']} / 100")
    print(f"🔥 Viral Factor: {result['viral_factor']} / 10")
    print(f"📊 Google Trend Score: {result['trend_score']}")
    print(f"🔑 Keywords: {result['keywords']}")

    print(f"\n🌐 Domain Suggestions:")
    for domain, status in result['domain_suggestions'].items():
        print(f" - {domain}: {status}")

    print(f"\n🏢 Competitors:")
    for comp in result['competitors']:
        print(f" - {comp}")

    export_pdf_report(result)
    print("\n📄 PDF report generated: business_report.pdf")
