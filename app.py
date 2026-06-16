import streamlit as st
import google.generativeai as genai
from fpdf import FPDF

# 🔑 API KEY
genai.configure(api_key="YOUR_REAL_API_KEY")

# 🤖 MODEL
model = genai.GenerativeModel("gemini-2.5-flash")

# 🖥️ UI
st.title("LinkedIn Profile Analyzer")

headline = st.text_input("Headline")
about = st.text_area("About")
skills = st.text_area("Skills")
experience = st.text_area("Experience")

# 📄 PDF FUNCTION
def generate_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for line in text.split("\n"):
        pdf.multi_cell(0, 10, line)

    pdf.output("LinkedIn_Report.pdf")


# 🚀 MAIN BUTTON
if st.button("Analyze"):

    # validation
    if not headline or not about or not skills or not experience:
        st.error("Please fill all fields before analyzing")
    else:

        # prompt
        prompt = f"""
Analyze this LinkedIn profile:

Headline: {headline}
About: {about}
Skills: {skills}
Experience: {experience}

Give:
- Headline Score
- About Score
- Skills Score
- Experience Score
- Suggestions
- Overall Score
"""

        # Gemini response
        response = model.generate_content(prompt)
        report = response.text

        st.write(report)

        # create PDF
        generate_pdf(report)

        st.success("PDF Created Successfully!")

        # download button
        with open("LinkedIn_Report.pdf", "rb") as file:
            st.download_button(
                label="Download PDF Report",
                data=file,
                file_name="LinkedIn_Report.pdf",
                mime="application/pdf"
            )
            