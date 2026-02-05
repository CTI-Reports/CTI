import streamlit as st
import pandas as pd

from core.data_loader import load_local_reports, get_ttp_and_country_columns
from core.geo_utils import get_nordic_baltic_countries, country_to_iso3
from core.risk_scoring import calculate_iso_risk_score, calculate_nist_risk_score, get_risk_level
from core.visualization import plot_risk_gauge, plot_heatmap, create_modern_plot_theme
import plotly.graph_objects as go
import pycountry

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

items = load_local_reports()
ttp_columns, country_columns = get_ttp_and_country_columns(items)

st.markdown('<h2 class="glow-text">WEEKLY THREAT INTELLIGENCE OVERVIEW</h2>', unsafe_allow_html=True)

report_dates = sorted(items['report_date'].dt.date.unique(), reverse=True)
selected_date = st.selectbox("Select Intelligence Report Period", report_dates, index=0)
selected_report = items[items['report_date'].dt.date == selected_date]

# Multi-country filter
all_countries = []
if country_columns:
    all_countries = pd.Series(pd.concat([selected_report[col] for col in country_columns], ignore_index=True))
    all_countries = sorted(all_countries.dropna().unique().tolist())

nordic_baltic_countries = get_nordic_baltic_countries()
default_countries = [c for c in nordic_baltic_countries if c in all_countries]

selected_countries = st.multiselect(
    "Geographic Filter",
    options=all_countries,
    default=default_countries
)

# Metrics
if ttp_columns:
    all_ttps = pd.Series(pd.concat([selected_report[col] for col in ttp_columns], ignore_index=True))
    all_ttps_flat = []
    unique_techniques = set()
    for val in all_ttps:
        if isinstance(val, (list, tuple, set)):
            vals = [str(x) for x in val if x not in [None, "None"]]
            all_ttps_flat.extend(vals)
            unique_techniques.update(vals)
        elif pd.notna(val) and str(val) != "None":
            all_ttps_flat.append(str(val))
            unique_techniques.add(str(val))
    unique_ttps_count = len(unique_techniques)
    total_ttp_count = len(all_ttps_flat)
else:
    unique_ttps_count = 0
    total_ttp_count = 0
    unique_techniques = set()

country_count = len([c for c in all_countries if c in selected_countries]) if selected_countries else len(all_countries)
sources_count = selected_report['source'].nunique() if 'source' in selected_report.columns else 0
regional_focus = bool(selected_countries and any(c in nordic_baltic_countries for c in selected_countries))

iso_score = calculate_iso_risk_score(total_ttp_count, country_count, sources_count, regional_focus)
nist_score = calculate_nist_risk_score(total_ttp_count, country_count, unique_techniques, regional_focus)

iso_level, iso_color = get_risk_level(iso_score)
nist_level, nist_color = get_risk_level(nist_score)

with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 15px; background: linear-gradient(45deg, #ffff00, #cccc00); border-radius: 10px; margin-bottom: 20px;">
        <h3 style="color: #000000; margin: 0;">NAVIGATION</h3>
    </div>
    """, unsafe_allow_html=True)

    st.plotly_chart(plot_risk_gauge(iso_score, "ISO 27005"), use_container_width=True)
    st.markdown(f"""
    <div style="background: linear-gradient(145deg, #2a2a2a, #1a1a1a); padding: 10px; border-radius: 8px; margin-bottom: 15px; border: 1px solid {iso_color};">
        <p style="margin: 0; font-size: 12px;"><strong>Risk Level:</strong> <span style="color: {iso_color};">{iso_level}</span></p>
    </div>
    """, unsafe_allow_html=True)

    st.plotly_chart(plot_risk_gauge(nist_score, "NIST SP 800-30"), use_container_width=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class="metric-container">
        <h3 style="margin: 0; color: #ffff00;">{unique_ttps_count}</h3>
        <p style="margin: 5px 0 0 0; color: #cccccc;">MITRE TTPs</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="metric-container">
        <h3 style="margin: 0; color: #ffff00;">{sources_count}</h3>
        <p style="margin: 5px 0 0 0; color: #cccccc;">Intel Sources</p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="metric-container">
        <h3 style="margin: 0; color: {iso_color};">{iso_score:.0f}</h3>
        <p style="margin: 5px 0 0 0; color: #cccccc;">ISO Risk Score</p>
    </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown(f"""
    <div class="metric-container">
        <h3 style="margin: 0; color: {nist_color};">{nist_score:.0f}</h3>
        <p style="margin: 5px 0 0 0; color: #cccccc;">NIST Risk Score</p>
    </div>
    """, unsafe_allow_html=True)

if country_columns and ttp_columns:
    melted = selected_report.melt(id_vars=country_columns, value_vars=ttp_columns,
                                  var_name="ttp_col", value_name="TTP")
    if any(melted["TTP"].apply(lambda x: isinstance(x, (list, tuple, set)))):
        melted = melted.explode("TTP")
    melted = melted.dropna(subset=["TTP"])
    melted = melted[melted["TTP"] != "None"]
    melted = melted.melt(id_vars=["TTP"], value_vars=country_columns,
                         var_name="country_col", value_name="country")
    melted = melted.dropna(subset=["country"])
    melted = melted[melted["country"] != "None"]

    if selected_countries:
        melted = melted[melted["country"].isin(selected_countries)]

    if not melted.empty:
        col_globe, col_ttp = st.columns([1, 1.5])

        all_countries_series = pd.Series(pd.concat([selected_report[col] for col in country_columns], ignore_index=True))
        all_countries_series = all_countries_series.dropna()[all_countries_series != "None"]
        if selected_countries:
            all_countries_series = all_countries_series[all_countries_series.isin(selected_countries)]
        iso_codes = all_countries_series.map(country_to_iso3).dropna().unique()
        all_iso = [c.alpha_3 for c in pycountry.countries]
        z_values = [1 if code in iso_codes else 0 for code in all_iso]

        fig_globe = go.Figure(go.Choropleth(
            locations=all_iso,
            z=z_values,
            colorscale=[[0, '#1a1a1a'], [1, '#ffff00']],
            showscale=False,
            marker_line_color='#ffff00',
            marker_line_width=1
        ))
        fig_globe.update_geos(
            projection_type="orthographic",
            showcoastlines=True, coastlinecolor="#ffff00",
            showland=True, landcolor="#2a2a2a",
            showocean=True, oceancolor="#0a0a0a",
            showframe=False, bgcolor="#0a0a0a"
        )
        fig_globe.update_layout(
            **create_modern_plot_theme(),
            title={'text': 'Global Threat Distribution', 'y': 0.95, 'x': 0.5, 'xanchor': 'center'},
            height=400
        )
        col_globe.plotly_chart(fig_globe, use_container_width=True)

        ttp_counts = (melted.groupby("TTP").size()
                      .reset_index(name="count")
                      .sort_values("count", ascending=False).head(10))

        fig_ttp = go.Figure(go.Bar(
            x=ttp_counts["count"],
            y=ttp_counts["TTP"],
            orientation="h",
            text=ttp_counts["count"],
            textposition="auto",
            marker=dict(
                color=ttp_counts["count"],
                colorscale=[[0, '#ffaa00'], [1, '#ffff00']],
                line=dict(color='#ffff00', width=1)
            )
        ))
        fig_ttp.update_layout(
            **create_modern_plot_theme(),
            title={'text': 'Top Human-Targeted Techniques', 'y': 0.95, 'x': 0.5, 'xanchor': 'center'},
            height=400,
            yaxis=dict(automargin=True, tickfont=dict(size=10))
        )
        col_ttp.plotly_chart(fig_ttp, use_container_width=True)

        country_counts = (melted.groupby("country").size()
                          .reset_index(name="count")
                          .sort_values("count", ascending=False))

        st.markdown('<h3 class="glow-text">Geographic Threat Distribution</h3>', unsafe_allow_html=True)
        fig_country = go.Figure(go.Bar(
            x=country_counts["country"],
            y=country_counts["count"],
            text=country_counts["count"],
            textposition="auto",
            marker=dict(
                color=country_counts["count"],
                colorscale=[[0, '#ffaa00'], [1, '#ffff00']],
                line=dict(color='#ffff00', width=1)
            )
        ))
        fig_country.update_layout(
            **create_modern_plot_theme(),
            height=400,
            xaxis=dict(tickangle=45, tickfont=dict(size=10)),
            yaxis=dict(title=dict(text="Threat Events", font=dict(color='#ffff00')))
        )
        st.plotly_chart(fig_country, use_container_width=True)

        st.markdown('<h3 class="glow-text">Threat Technique Heatmap</h3>', unsafe_allow_html=True)
        heat_data = melted.groupby(["country", "TTP"]).size().reset_index(name="count")
        plot_heatmap(heat_data, x_col="country", y_col="TTP",
                     title="MITRE Techniques × Geographic Distribution", height=600)
