import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from .risk_scoring import get_risk_level

def create_modern_plot_theme():
    return {
        'paper_bgcolor': '#050505',
        'plot_bgcolor': '#101010',
        'font': {'color': '#ffffff', 'family': 'Courier New'},
        'colorway': ['#ffff00', '#ffaa00', '#ff4444', '#44ff44', '#00aaff', '#aa44ff'],
        'margin': {'l': 0, 'r': 0, 't': 40, 'b': 20}
    }

def plot_risk_gauge(score, framework):
    level, color = get_risk_level(score)
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"{framework} Risk Score", 'font': {'color': '#ffff00', 'size': 16}},
        delta={'reference': 50, 'increasing': {'color': "#ff4444"}, 'decreasing': {'color': "#44ff44"}},
        gauge={
            'axis': {'range': [None, 100], 'tickcolor': '#ffff00'},
            'bar': {'color': color, 'thickness': 0.8},
            'bgcolor': '#2a2a2a',
            'borderwidth': 2,
            'bordercolor': '#ffff00',
            'steps': [
                {'range': [0, 50], 'color': 'rgba(68, 255, 68, 0.2)'},
                {'range': [50, 75], 'color': 'rgba(255, 170, 0, 0.2)'},
                {'range': [75, 100], 'color': 'rgba(255, 68, 68, 0.2)'}
            ],
            'threshold': {
                'line': {'color': "#ffffff", 'width': 4},
                'thickness': 0.75,
                'value': score
            }
        }
    ))
    theme = create_modern_plot_theme()
    theme['font'] = {'color': '#ffffff', 'size': 12, 'family': 'Courier New'}
    theme['height'] = 300
    fig.update_layout(**theme)
    return fig

def plot_heatmap(df, x_col, y_col, title, x_order=None, y_order=None, height=500):
    if df.empty:
        st.info("No data available to display heatmap.")
        return

    pivot = df.pivot(index=y_col, columns=x_col, values="count").fillna(0)
    if y_order:
        pivot = pivot.reindex(index=y_order, fill_value=0)
    if x_order:
        pivot = pivot.reindex(columns=x_order, fill_value=0)

    z_values = pivot.values
    text_values = np.where(z_values > 0, z_values.astype(int), "")

    fig = go.Figure(go.Heatmap(
        z=z_values,
        x=list(pivot.columns),
        y=list(pivot.index),
        colorscale=[[0, '#1a1a1a'], [0.5, '#ffaa00'], [1, '#ffff00']],
        text=text_values,
        texttemplate="%{text}",
        textfont={"size": 10, "color": "#ffffff"},
        hovertemplate=f"{x_col}: %{{x}}<br>{y_col}: %{{y}}<br>Count: %{{z}}<extra></extra>",
        showscale=True,
        xgap=2,
        ygap=2
    ))

    fig.update_layout(
        **create_modern_plot_theme(),
        title={'text': title, 'y': 0.95, 'x': 0.5, 'xanchor': 'center'},
        height=height,
        xaxis={'showgrid': False, 'tickangle': 45},
        yaxis={'showgrid': False}
    )
    st.plotly_chart(fig, use_container_width=True)
