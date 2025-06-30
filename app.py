import streamlit as st
from analyzer import analyze_business_idea, export_pdf_report

st.set_page_config(page_title="TechTide", layout="centered")

st.title("🚀TechTide")
st.write("Analyze your business idea for SWOT, trends, domains, and more!")

# Idea input
idea = st.text_area("💡 Enter your business idea", placeholder="e.g., AI-powered legal document generator")

if st.button("Analyze"):
    if not idea.strip():
        st.warning("Please enter a business idea.")
    else:
        with st.spinner("Analyzing your hustle..."):
            result = analyze_business_idea(idea)

        st.success("Analysis complete!")

        st.subheader("📊 Hustle Score")
        st.progress(result["hustle_score"] / 100)
        st.metric("Score", f"{result['hustle_score']} / 100")
        st.metric("Viral Factor", f"{result['viral_factor']} / 10")
        st.metric("Google Trend Score", result["trend_score"])

        st.subheader("🧠 SWOT Analysis")
        for k, v in result["swot"].items():
            st.markdown(f"**{k}**: {', '.join(v)}")

        st.subheader("🔑 Extracted Keywords")
        st.write(result["keywords"])

        st.subheader("🌐 Domain Suggestions")
        for domain, status in result["domain_suggestions"].items():
            emoji = "✅" if "Available" in status else "❌"
            st.write(f"{emoji} {domain} - {status}")

        st.subheader("🏢 Competitors")
        for c in result["competitors"]:
            st.markdown(f"- {c}")

        # Export PDF
        filename = export_pdf_report(result)
        with open(filename, "rb") as f:
            st.download_button("📄 Download Report (PDF)", f, file_name=filename)
