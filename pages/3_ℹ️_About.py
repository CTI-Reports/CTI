import streamlit as st
from core.ml_models import ML_AVAILABLE

st.set_page_config(page_title="About", page_icon="ℹ️", layout="wide")

st.markdown("""
<div style="padding: 30px; background: linear-gradient(145deg, #1a1a1a, #2a2a2a);
            border: 2px solid #ffff00; border-radius: 15px; margin: 20px 0;">
    
    <h2 class="glow-text">ML‑Powered Threat Intelligence Platform</h2>

    <p style="font-size: 16px; line-height: 1.6;">
        This platform delivers enterprise‑grade cybersecurity intelligence with advanced machine learning 
        capabilities for predictive analytics, anomaly detection, and intelligent threat pattern recognition.
        Designed for operational security teams, SOC analysts, and cyber‑threat researchers, it provides 
        a unified view of human‑targeted attacks, geographic exposure, and emerging adversarial behaviors.
    </p>

    <h3 style="color: #ffff00; margin-top: 30px;">Machine Learning Capabilities</h3>
    <ul style="font-size: 14px; line-height: 1.8;">
        <li><strong>KMeans Clustering</strong> — Threat pattern grouping using TF‑IDF vectorization</li>
        <li><strong>Isolation Forest</strong> — Detection of anomalous attack vectors</li>
        <li><strong>Polynomial Regression</strong> — Time‑series forecasting with confidence intervals</li>
        <li><strong>NLP Intelligence Extraction</strong> — Keyword, technique, and pattern mining</li>
        <li><strong>Threat Actor Profiling</strong> — ML‑driven behavioral clustering</li>
        <li><strong>Automated Prioritization</strong> — Multi‑factor scoring (frequency, geo‑spread, recency, sophistication)</li>
        <li><strong>Geographic Risk Forecasting</strong> — Nordic/Baltic threat prediction</li>
        <li><strong>Resource Allocation Optimization</strong> — Budget and focus recommendations</li>
    </ul>

    <h3 style="color: #ffff00; margin-top: 30px;">Risk Assessment Frameworks</h3>
    <ul style="font-size: 14px; line-height: 1.8;">
        <li><strong>ISO 27005</strong> — Threat frequency, geographic spread, and source diversity</li>
        <li><strong>NIST SP 800‑30</strong> — Likelihood, impact, and vulnerability scoring</li>
    </ul>

    <h3 style="color: #ffff00; margin-top: 30px;">Technical Stack</h3>
    <p style="font-size: 14px; line-height: 1.8;">
        <strong>ML Libraries:</strong> scikit‑learn<br>
        <strong>Data Processing:</strong> pandas, numpy<br>
        <strong>Visualization:</strong> plotly, streamlit<br>
        <strong>Geolocation:</strong> MaxMind GeoLite2<br>
        <strong>ML Status:</strong> {status}
    </p>

    <div style="margin-top: 40px; padding: 20px; 
                background: linear-gradient(45deg, #ffff00, #cccc00); 
                border-radius: 10px;">
        <p style="color: #000000; font-weight: bold; text-align: center; margin: 0;">
            Developed by Ricardo Mendes Pinto
        </p>
    </div>

</div>
""".replace(
    "{status}",
    '<span style="color: #44ff44;">Active</span>' if ML_AVAILABLE 
    else '<span style="color: #ff4444;">Unavailable — Install scikit‑learn</span>'
), unsafe_allow_html=True)
