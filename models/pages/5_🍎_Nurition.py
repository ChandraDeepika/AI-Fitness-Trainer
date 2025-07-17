import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from streamlit_extras.no_default_selectbox import selectbox
import matplotlib.pyplot as plt
from streamlit_lottie import st_lottie
import requests
from datetime import datetime

# Page config
st.set_page_config(page_title='Nutrition Calorie Tracker', layout='wide')

# Custom CSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .header {
        background: linear-gradient(135deg, #025246 0%, #013a32 100%);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .header h2 {
        color: white;
        text-align: center;
        margin: 0;
        font-size: 2.5em;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }
    .nutrition-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    .nutrition-card:hover {
        transform: translateY(-5px);
    }
    .nutrition-card h3 {
        color: #025246;
        font-size: 1.5em;
        margin-bottom: 15px;
    }
    .nutrition-card p {
        color: #333333;
        font-size: 1.1em;
        line-height: 1.6;
    }
    .summary-card {
        background: linear-gradient(135deg, #025246 0%, #013a32 100%);
        color: #ffffff !important;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .summary-card h4,
    .summary-card p {
        color: #ffffff !important;
    }
    .chart-container {
        background: linear-gradient(135deg, #FF9800 0%, #F57C00 100%);
        color: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .chart-container h3 {
        color: white !important;
        text-align: center;
        margin-bottom: 15px;
    }
    .stNumberInput > div > div > input {
        color: #333333;
        border-radius: 10px;
        border: 2px solid #025246;
    }
    .stSelectbox > div > div > select {
        color: #333333;
    }
    .daily-goal {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .nutrition-tip {
        background: linear-gradient(135deg, #FF9800 0%, #F57C00 100%);
        color: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .progress-container {
        background: linear-gradient(135deg, #d4edda 0%, #a8e063 100%);
        color: #025246;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .progress-container h3, .progress-container h4, .progress-container p {
        color: #025246 !important;
        font-weight: 600;
    }
    .breakdown-header {
        background: linear-gradient(135deg, #FF9800 0%, #F57C00 100%);
        color: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .breakdown-header h3 {
        color: white !important;
        text-align: center;
        margin: 0;
        font-weight: 700;
    }
    .nutrition-card {
        color: #025246 !important;
    }
    .nutrition-card h3 {
        color: #025246 !important;
        font-weight: 700;
    }
    .nutrition-card p {
        color: #025246 !important;
    }
    .progress-bar {
        height: 20px;
        background: linear-gradient(90deg, #025246 0%, #013a32 100%);
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Header with animation
st.markdown("""
<div class="header">
    <h2>🍎 Nutrition Tracker</h2>
</div>
""", unsafe_allow_html=True)

# Load Lottie animation
def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.json()
        return None
    except Exception as e:
        return None

# Load and display welcome animation
nutrition_animation = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_obhph3sh.json")
if nutrition_animation:
    st_lottie(nutrition_animation, height=200, key="welcome")

# Load data
df = pd.read_csv("models/food1.csv", encoding='mac_roman')

# Main container
with st.container():
    # Daily Goals Section
    st.markdown("""
    <div class="daily-goal">
        <h3>Set Your Daily Goals</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        daily_calories = st.number_input('Daily Calorie Goal', min_value=1000, max_value=5000, value=2000)
    with col2:
        daily_protein = st.number_input('Daily Protein Goal (g)', min_value=20, max_value=200, value=50)
    with col3:
        daily_carbs = st.number_input('Daily Carbs Goal (g)', min_value=50, max_value=500, value=250)
    
    # Nutrition Tips
    nutrition_tips = [
        "Stay hydrated! Drink at least 8 glasses of water daily.",
        "Include a variety of colorful vegetables in your diet.",
        "Don't skip breakfast - it's the most important meal of the day.",
        "Choose whole grains over refined grains when possible.",
        "Limit processed foods and added sugars."
    ]
    
    st.markdown(f"""
    <div class="nutrition-tip">
        <h3>💡 Nutrition Tip</h3>
        <p>{nutrition_tips[np.random.randint(0, len(nutrition_tips))]}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="nutrition-card">
        <h3>Track Your Daily Nutrition</h3>
        <p>Select your meals and track your nutritional intake</p>
    </div>
    """, unsafe_allow_html=True)
    
    ye = st.number_input('Enter Number of dishes', min_value=1, max_value=10)
    
    i = 0
    j = 0
    calories = 0
    total_protein = 0
    total_carbs = 0
    list1 = []
    list2 = []
    list3 = []
    list4 = []
    list5 = []
    list6 = []
    list7 = []
    list8 = []

    try:
        while(i < ye):
            st.markdown("""
            <div class="nutrition-card">
            """, unsafe_allow_html=True)
            
            sel = selectbox('Select the food', df['Shrt_Desc'].unique(), no_selection_label=" ", key=i)
            list1.append(sel)
            
            sel_serving = st.number_input('Select the number of servings', min_value=1, max_value=10, value=1, step=1, key=j+100)
            
            st.markdown(f"""
            <div class="summary-card">
                <h4>Food Details</h4>
                <p>Food: {sel}</p>
                <p>Serving: {sel_serving}</p>
                <p>Calories per serving: {df[df['Shrt_Desc']==sel]['Energ_Kcal'].values[0]}</p>
            </div>
            """, unsafe_allow_html=True)
            
            cal = df[df['Shrt_Desc']==sel]['Energ_Kcal'].values[0] * sel_serving
            list2.append(cal)
            
            protine = df[df['Shrt_Desc']==sel]['Protein_(g)'].values[0] * sel_serving
            list3.append(protine)
            total_protein += protine
            
            carbs = df[df['Shrt_Desc']==sel]['Carbohydrt_(g)'].values[0] * sel_serving
            list4.append(carbs)
            total_carbs += carbs
            
            fat = df[df['Shrt_Desc']==sel]['Lipid_Tot_(g)'].values[0] * sel_serving
            list5.append(fat)
            
            sugar = df[df['Shrt_Desc']==sel]['Sugar_Tot_(g)'].values[0] * sel_serving
            list7.append(sugar)
            
            calcium = df[df['Shrt_Desc']==sel]['Calcium_(mg)'].values[0] * sel_serving
            list8.append(calcium)
            
            calories += cal
            
            i += 1
            j += 1
            
            st.markdown("</div>", unsafe_allow_html=True)

        # Progress Section
        st.markdown("""
        <div class="progress-container">
            <h3>Daily Progress</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            calorie_progress = min(100, (calories / daily_calories) * 100)
            st.markdown(f"""
            <div class="progress-container">
                <h4>Calories</h4>
                <p>{calories} / {daily_calories} kcal</p>
                <div class="progress-bar" style="width: {calorie_progress}%"></div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            protein_progress = min(100, (total_protein / daily_protein) * 100)
            st.markdown(f"""
            <div class="progress-container">
                <h4>Protein</h4>
                <p>{total_protein:.1f} / {daily_protein} g</p>
                <div class="progress-bar" style="width: {protein_progress}%"></div>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            carbs_progress = min(100, (total_carbs / daily_carbs) * 100)
            st.markdown(f"""
            <div class="progress-container">
                <h4>Carbs</h4>
                <p>{total_carbs:.1f} / {daily_carbs} g</p>
                <div class="progress-bar" style="width: {carbs_progress}%"></div>
            </div>
            """, unsafe_allow_html=True)

        # Charts with orange background
        st.markdown("""
        <div class="chart-container">
            <h3>Nutritional Breakdown</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            fig = go.Figure(data=[go.Pie(labels=list1, values=list2, textinfo='percent', insidetextorientation='radial')])
            fig.update_layout(
                title="Calorie Breakdown",
                template="plotly_white",
                showlegend=True,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            fig1 = go.Figure(data=[go.Pie(labels=list1, values=list3, textinfo='percent', insidetextorientation='radial')])
            fig1.update_layout(
                title="Protein Breakdown",
                template="plotly_white",
                showlegend=True,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig1, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col3:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            fig2 = go.Figure(data=[go.Pie(labels=list1, values=list4, textinfo='percent', insidetextorientation='radial')])
            fig2.update_layout(
                title="Carbs Breakdown",
                template="plotly_white",
                showlegend=True,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Additional charts with orange background
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            fig3 = go.Figure(data=[go.Pie(labels=list1, values=list5, textinfo='percent', insidetextorientation='radial')])
            fig3.update_layout(
                title="Fat Breakdown",
                template="plotly_white",
                showlegend=True,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig3, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            fig4 = go.Figure(data=[go.Pie(labels=list1, values=list7, textinfo='percent', insidetextorientation='radial')])
            fig4.update_layout(
                title="Sugar Breakdown",
                template="plotly_white",
                showlegend=True,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig4, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col3:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            fig5 = go.Figure(data=[go.Pie(labels=list1, values=list8, textinfo='percent', insidetextorientation='radial')])
            fig5.update_layout(
                title="Calcium Breakdown",
                template="plotly_white",
                showlegend=True,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig5, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    except:
        st.markdown("""
        <div class="nutrition-card">
            <p>Please select your meals to see the nutritional breakdown</p>
        </div>
        """, unsafe_allow_html=True)

# Footer animation
if nutrition_animation:
    st.markdown("""
    <div class="animation-container">
        <div style="text-align: center;">
            <h3>Stay Healthy! 🍎</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st_lottie(nutrition_animation, height=100, key="footer")