import streamlit as st


st.set_page_config(page_title="DiagnoCare", layout="centered")
st.markdown(
    """
    <style>
    /* Main styling */
    .main {
        font-family: 'Arial', sans-serif;
        background-color: #4a90e2;
    }

    /* Custom Tabs Styling */
    [data-testid="stTabs"] {
        background-color: #e6f0fa;
        border-radius: 8px;
        padding: 5px;
    }
    [data-testid="stTab"] {
        color: #2d3e50;
        font-weight: bold;
        padding: 8px 20px;
        border-radius: 6px;
    }
    [data-testid="stTab"]:hover {
        background-color: #d6e9f8;
        color: #000000;
    }
    [data-testid="stTab"][aria-selected="true"] {
        background-color: #4a90e2;
        color: white;
    }

    /* Title and sections */
    .title {
        color: #2d3e50;
        font-size: 40px;
        font-weight: bold;
        text-align: center;
    }
    .section-header {
        color: #4a90e2;
        font-size: 28px;
        margin-top: 20px;
    }
    .section-content {
        font-size: 18px;
        color: white;
        text-align: justify;
        line-height: 1.6;
    }

    /* CTA Buttons */
    .cta-button {
        background-color: #2d3e50;
        color: white;
        padding: 10px 30px;
        border-radius: 30px;
        text-align: center;
        font-size: 18px;
        margin-top: 30px;
        display: inline-block;
        text-decoration: none;
    }
    .cta-button:hover {
        background-color: #2d3e50;
        cursor: pointer;
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 20px;
        background-color: #2d3e50;
        color: white;
    }
    .social-icons {
        font-size: 24px;
        margin: 10px;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)


def main():
    
    
    # Title Section
    st.markdown('<h1 class="title">Welcome to DiagnoCare</h1>', unsafe_allow_html=True)
    
    # Platform Overview
    st.markdown('<h2 class="section-header">Platform Overview</h2>', unsafe_allow_html=True)
    st.markdown(
        """
        <p class="section-content">
        DiagnoCare is an advanced healthcare platform that empowers individuals and healthcare professionals with cutting-edge AI tools to diagnose medical conditions, manage health records, and receive personalized recommendations.
        </p>
        """, unsafe_allow_html=True)
    
    # Key Features Section
    st.markdown('<h2 class="section-header">Key Features</h2>', unsafe_allow_html=True)
    st.markdown(
        """
        <p class="section-content">
        -AI-Based Diagnosis : Accurate predictions and suggestions using AI.
        \n-Symptom-Based Predictions : Based on your symptoms, we provide probable diagnoses.
        \n-Personalized Recommendations : Get diet, lifestyle, and medical suggestions based on your health profile.
        \n-Health Record Management : Keep your records secure and easily accessible in one platform.
        </p>
        """, unsafe_allow_html=True)

    # Mission Statement
    st.markdown('<h2 class="section-header">Our Mission</h2>', unsafe_allow_html=True)
    st.markdown(
        """
        <p class="section-content">
        Our mission is to make healthcare more accessible and accurate using artificial intelligence. We aim to provide individuals with the tools they need to understand their health better and make informed decisions.
        </p>
        """, unsafe_allow_html=True)

    # Call to Action Section
    st.markdown('<h2 class="section-header">Get Started with DiagnoCare</h2>', unsafe_allow_html=True)
    st.markdown(
        """
        <p class="section-content">
        Start exploring our platform now! Access diagnosis tools, manage your health records, and receive personalized insights to take charge of your health.
        </p>
        """, unsafe_allow_html=True)
    
    # Call-to-action buttons (using custom CSS)
    st.markdown('<a href="/diagnosis" class="cta-button">Start Diagnosis</a>', unsafe_allow_html=True)

    st.markdown('<a href="/sapp" class="cta-button">Manage Health Records</a>', unsafe_allow_html=True)

    st.markdown('<a href="/Insights" class="cta-button">Get Insights of the disease data</a>', unsafe_allow_html=True)

    st.markdown('<a href="/Utilities" class="cta-button">Get Utilities(Chat, tips, tools)</a>', unsafe_allow_html=True)

    # Social Media and Contact Info
    st.markdown("<div class='footer'><p>Contact Us: support@diagnocare.com</p></div>", unsafe_allow_html=True)

    # Social Icons (you can replace these with actual links to social media)
    st.markdown(
        """
        <div class="footer">
            <a href="#" class="social-icons">🔗</a>
            <a href="#" class="social-icons">🐦</a>
            <a href="#" class="social-icons">📘</a>
            <a href="#" class="social-icons">🔶</a>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
