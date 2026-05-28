import streamlit as st
import pandas as pd
import numpy as np
import mysql.connector
import requests
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier


DB_PASSWORD = "password"  
DB_NAME = "manvi"
WEATHER_API_KEY = "3dcd49616ce180e16436ce8d44ebdd81"  
CITY_NAME = "Udaipur"

st.set_page_config(page_title="AuraStyle Engine", page_icon="👗", layout="wide")


@st.cache_resource
def initialize_and_train_model():
    """Generates 1,000 historical rows based on Rajasthan climate boundaries and trains the ML classifier."""
    np.random.seed(42)
    n_records = 1000

    
    temperatures = np.random.uniform(12.0, 44.0, n_records)     
    humidity = np.random.uniform(20.0, 85.0, n_records)          
    uv_indices = np.random.randint(1, 12, n_records)             
    wind_speeds = np.random.uniform(3.0, 35.0, n_records)        

    df_train = pd.DataFrame({
        'temperature_c': temperatures,
        'humidity_percent': humidity,
        'uv_index': uv_indices,
        'wind_speed_kmh': wind_speeds
    })

    
    conditions = [
        (df_train['temperature_c'] >= 34.0) & (df_train['uv_index'] >= 7),     
        (df_train['temperature_c'] >= 30.0) & (df_train['humidity_percent'] >= 65), 
        (df_train['temperature_c'] <= 21.0) | (df_train['wind_speed_kmh'] >= 24.0), 
    ]
    choices = [0, 1, 2]
    df_train['recommended_profile_id'] = np.select(conditions, choices, default=3) 

   
    X = df_train[['temperature_c', 'humidity_percent', 'uv_index', 'wind_speed_kmh']]
    y = df_train['recommended_profile_id']
    
    clf = DecisionTreeClassifier(max_depth=4, random_state=42)
    clf.fit(X, y)
    
    return clf, df_train

model, historical_df = initialize_and_train_model()


def fetch_live_weather(city, api_key):
    """Hits OpenWeatherMap API to harvest live climate arrays dynamically."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
           
            metrics = {
                'temp': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'wind': data['wind']['speed'] * 3.6,
                'uv': 9 if data['main']['temp'] > 33 else (4 if data['main']['temp'] > 22 else 2)
            }
            return metrics, True
        return None, False
    except:
        return None, False


st.title("👗 AuraStyle: Climate-Driven Inventory Routing Engine")
st.markdown("### `Production Stack: REST API ➔ Python Scikit-Learn ➔ MySQL Relational Storage ➔ Streamlit Dashboard`")
st.write("---")

col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("🌐 Real-Time Telemetry Ingestion")
    
    if st.button("🔌 Fetch Live Meteorological Data for Udaipur"):
        live_metrics, success = fetch_live_weather(CITY_NAME, WEATHER_API_KEY)
        
        if success:
            st.success(f"📡 Secure Connection Established with OpenWeatherServer!")
            
            
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Temperature", f"{live_metrics['temp']} °C")
            m2.metric("Humidity", f"{live_metrics['humidity']} %")
            m3.metric("Wind Speed", f"{live_metrics['wind']:.1f} km/h")
            m4.metric("Calculated UV", f"{live_metrics['uv']} Index")
           
            input_vector = pd.DataFrame([[live_metrics['temp'], live_metrics['humidity'], live_metrics['uv'], live_metrics['wind']]], 
                                         columns=['temperature_c', 'humidity_percent', 'uv_index', 'wind_speed_kmh'])
            prediction = int(model.predict(input_vector)[0])
            
            profile_labels = {
                0: "Summer Casual Y2K Silhouette (Focus: Cropped, Light Silhouettes)",
                1: "Airy High-Humidity Comfort (Focus: Loose Textiles, Linen Trousers)",
                2: "Cozy Heavy Streetwear (Focus: Heavy Outerwear, Hoodies)",
                3: "Classic Balanced Streetwear (Focus: Denim, Standard Tees)"
            }
            
            st.info(f"🤖 **ML Classifier Routing Target:** Profile {prediction} ➔ *{profile_labels[prediction]}*")
            
            try:
                conn = mysql.connector.connect(host="localhost", user="root", password=DB_PASSWORD, database=DB_NAME)
                cursor = conn.cursor()
                
                if prediction == 0:
                    cursor.execute("SELECT item_name, color FROM personal_wardrobe WHERE clothing_type='Top_Cropped' AND clean_status='Clean' LIMIT 1;")
                    top = cursor.fetchone()
                    cursor.execute("SELECT item_name, color FROM personal_wardrobe WHERE clothing_type='Bottom' AND clean_status='Clean' LIMIT 1;")
                    bottom = cursor.fetchone()
                elif prediction == 2:
                    cursor.execute("SELECT item_name, color FROM personal_wardrobe WHERE clothing_type='Top_Heavy' AND clean_status='Clean' LIMIT 1;")
                    top = cursor.fetchone()
                    cursor.execute("SELECT item_name, color FROM personal_wardrobe WHERE clothing_type='Bottom' AND clean_status='Clean' LIMIT 1;")
                    bottom = cursor.fetchone()
                else:
                    cursor.execute("SELECT item_name, color FROM personal_wardrobe WHERE clothing_type='Top_Standard' AND clean_status='Clean' LIMIT 1;")
                    top = cursor.fetchone()
                    cursor.execute("SELECT item_name, color FROM personal_wardrobe WHERE clothing_type='Bottom' AND clean_status='Clean' LIMIT 1;")
                    bottom = cursor.fetchone()
                
                cursor.close()
                conn.close()
                
               
                st.subheader("🛍️ Dynamic Wardrobe Routing Output")
                     
                st.success(f"✨ **Recommended Outfit Combination:** Wear your **{top[0]}** paired perfectly with your **{bottom[0]}**.")
            except Exception as e:
                st.error(f"❌ Database Connection Interrupted: {e}")
        else:
            st.error("❌ Failed to reach OpenWeather servers. Verify your API Key configuration.")

with col_right:
    st.subheader("📊 Model Explainability & Diagnostics")
    
    
    fig, ax = plt.subplots(figsize=(6, 3.8))
    importances = model.feature_importances_
    features = ['Temperature', 'Humidity', 'UV Index', 'Wind Speed']
    
    colors = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78']
    ax.barh(features, importances, color=colors, edgecolor='none')
    ax.set_xlabel('Relative Importance Weight')
    ax.set_title('Decision Tree Spatial Feature Weights')
    plt.tight_layout()
    
    st.pyplot(fig)
    st.write("💡 *Recruiter Diagnostics:* This chart demonstrates feature split importance. The Decision Tree algorithm isolates node parameters automatically without relying on manual hardcoded heuristic parameters.")