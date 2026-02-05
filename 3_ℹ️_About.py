import streamlit as st
from core.ml_models import ML_AVAILABLE

st.set_page_config(page_title="About", page_icon="ℹ️", layout="wide")

st.markdown("""
<div style="padding: 30px; background: linear-gradient(145deg, #1a1a1a, #2a2a2a); 
border: 2px solid #ffff00; border-radius: 15px; margin: 20px 0;">
    <h2 class="glow-text">ML-Powered Threat Intelligence Platform</h2>
    <p style="font-size: 16px; line-height: 1.6;">
        This platform delivers enterprise-grade cybersecurity intelligence with advanced machine learning 
        capabilities for predictive analytics, anomaly detection, and intelligent threat pattern recognition.
    </p>

    <h3 style="color: #ffff00; margin-top: 30px;">Machine Learning Features</h3>
    <ul style="font-size: 14px; line-height: 1.8;">
        <li>KMeans clustering for threat pattern grouping</li>
        <li>Isolation Forest anomaly detection</li>
        <li>Polynomial regression forecasting</li>
        <li>TF-IDF NLP intelligence extraction</li>
        <li>Automated threat prioritization</li>
        <li>Geographic risk forecasting</li>
        <li>Resource allocation optimization</li>
    </ul>

    <h3 style="color: #ffff00; margin-top: 30px;">Risk Frameworks</h3>
    <ul style="font-size: 14px; line-height: 1.8;">
        <li><strong>ISO 27005</strong> — Threat frequency, geographic spread, source diversity</li>
        <li><strong>NIST SP 800-30</strong> — Likelihood, impact, vulnerability scoring</li>
    </ul>

    <h3 style="color: #ffff00; margin-top: 30px;">Technical Stack</h3>
    <p style="font-size: 14px; line-height: 1.8;">
        <strong>ML Libraries:</strong> scikit-learn<br>
        <strong>Data Processing:</strong> pandas, numpy<br>
        <strong>Visualization:</strong> plotly, streamlit<br>
        <strong>ML Status:</strong> 
        {status}
    </p>

    <div style="margin-top: 40px; padding: 20px; background: linear-gradient(45deg, #ffff00, #cccc00); border-radius: 10px;">
        <p style="color: #000000; font-weight: bold; text-align: center; margin: 0;">
            Developed by Ricardo Mendes Pinto
        </p>
    </div>
</div>
""".replace("{status}", 
    '<span style="color: #44ff44;">Active</span>' if ML_AVAILABLE 
    else '<span style="color: #ff4444;">Unavailable — Install scikit-learn</span>'
), unsafe_allow_html=True)
