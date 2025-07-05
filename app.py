import os
import pickle
import requests
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(page_title="Health Assistant 🧠", layout="wide", page_icon="🧑‍⚕️")

# -----------------------------
# Custom Background & Styles
# -----------------------------
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1588776814546-ec7e7b8823e6?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        backdrop-filter: blur(3px);
        color: white;
    }
    .stContainer {
        background-color: rgba(0, 0, 0, 0.6);
        padding: 1rem;
        border-radius: 10px;
    }
    div[data-testid="stHorizontalBlock"] div:hover {
        transform: scale(1.02);
        transition: 0.3s ease-in-out;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# Floating Theme Toggle (optional visual label)
# -----------------------------
toggle = st.sidebar.checkbox("🌗 Toggle Dark Mode", value=True)
theme_color = "#08E8DE" if toggle else "#007BFF"
text_color = "white" if toggle else "black"

# -----------------------------
# Load Lottie Animation
# -----------------------------
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_health = load_lottieurl("https://lottie.host/00bc19ed-2db2-466b-9f70-3c3ce6f3515e/2aDn0gHX33.json")

# -----------------------------
# Load ML Models
# -----------------------------
working_dir = os.path.dirname(os.path.abspath(__file__))
diabetes_model = pickle.load(open(f'{working_dir}/saved_models/diabetes_model.sav', 'rb'))
heart_disease_model = pickle.load(open(f'{working_dir}/saved_models/heart_disease_model.sav', 'rb'))
parkinsons_model = pickle.load(open(f'{working_dir}/saved_models/parkinsons_model.sav', 'rb'))

# -----------------------------
# Custom Result Card
# -----------------------------
def result_card(text, color="#00cc66"):
    st.markdown(f"""
    <div style="background-color:{color};padding:15px;border-radius:12px;color:white;font-size:18px;">
        {text}
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown(f"<h1 style='color:{theme_color};'>🧠 Health Assistant - Disease Predictor</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:{text_color}; font-size: 18px;'>Predict Diabetes, Heart Disease, and Parkinson's using ML</p>", unsafe_allow_html=True)
with col2:
    if lottie_health:
        st_lottie(lottie_health, height=200, key="health")

# -----------------------------
# Sidebar Navigation
# -----------------------------
with st.sidebar:
    selected = option_menu(
        menu_title="Choose Prediction",
        options=["Diabetes Prediction", "Heart Disease Prediction", "Parkinsons Prediction"],
        icons=["activity", "heart", "person"],
        menu_icon="hospital-fill",
        default_index=0,
        styles={
            "container": {"background-color": "#0e1117"},
            "icon": {"color": theme_color, "font-size": "20px"},
            "nav-link": {"color": "#FFFFFF"},
            "nav-link-selected": {"background-color": theme_color, "color": "black"},
        })

# -----------------------------
# Diabetes Page
# -----------------------------
if selected == "Diabetes Prediction":
    st.subheader("🔷 Diabetes Prediction")
    col1, col2, col3 = st.columns(3)
    with col1: Pregnancies = st.text_input("Number of Pregnancies")
    with col2: Glucose = st.text_input("Glucose Level")
    with col3: BloodPressure = st.text_input("Blood Pressure")
    with col1: SkinThickness = st.text_input("Skin Thickness")
    with col2: Insulin = st.text_input("Insulin Level")
    with col3: BMI = st.text_input("BMI")
    with col1: DiabetesPedigreeFunction = st.text_input("Diabetes Pedigree Function")
    with col2: Age = st.text_input("Age")

    if st.button("🎯 Predict Diabetes"):
        try:
            input_data = [float(x) for x in [Pregnancies, Glucose, BloodPressure, SkinThickness,
                                             Insulin, BMI, DiabetesPedigreeFunction, Age]]
            prediction = diabetes_model.predict([input_data])[0]
            result = "✅ The person is diabetic" if prediction == 1 else "🎉 The person is not diabetic"
            result_card(result)
        except:
            st.error("⚠️ Please enter valid numeric values.")

    with st.expander("💡 Did you know?", expanded=True):
        st.markdown(
            "- **Regular exercise** helps control blood sugar.\n"
            "- Choose **whole grains** and **fiber-rich** foods.\n"
            "- Stay hydrated and **avoid sugary drinks**."
        )

# -----------------------------
# Heart Disease Page
# -----------------------------
elif selected == "Heart Disease Prediction":
    st.subheader("❤️ Heart Disease Prediction")
    col1, col2, col3 = st.columns(3)
    with col1: age = st.text_input("Age")
    with col2: sex = st.text_input("Sex (1=Male, 0=Female)")
    with col3: cp = st.text_input("Chest Pain Type (0-3)")
    with col1: trestbps = st.text_input("Resting Blood Pressure")
    with col2: chol = st.text_input("Cholesterol")
    with col3: fbs = st.text_input("Fasting Blood Sugar > 120 (1/0)")
    with col1: restecg = st.text_input("Resting ECG (0-2)")
    with col2: thalach = st.text_input("Max Heart Rate")
    with col3: exang = st.text_input("Exercise Induced Angina (1/0)")
    with col1: oldpeak = st.text_input("ST Depression")
    with col2: slope = st.text_input("Slope (0-2)")
    with col3: ca = st.text_input("Major Vessels (0-3)")
    with col1: thal = st.text_input("Thal (0=Normal, 1=Fixed, 2=Reversible)")

    if st.button("🎯 Predict Heart Disease"):
        try:
            input_data = [float(x) for x in [age, sex, cp, trestbps, chol, fbs,
                                             restecg, thalach, exang, oldpeak,
                                             slope, ca, thal]]
            prediction = heart_disease_model.predict([input_data])[0]
            result = "❤️ The person has heart disease" if prediction == 1 else "✅ The person does not have heart disease"
            result_card(result)
        except:
            st.error("⚠️ Please enter valid numeric values.")

    with st.expander("💡 Heart Health Tips", expanded=True):
        st.markdown(
            "- Include **cardio exercises** like walking or cycling.\n"
            "- Eat foods rich in **Omega-3** (like salmon, walnuts).\n"
            "- Quit smoking and **reduce sodium** in diet."
        )

# -----------------------------
# Parkinson's Page
# -----------------------------
elif selected == "Parkinsons Prediction":
    st.subheader("🧠 Parkinson's Disease Prediction")

    fields = [
        'MDVP:Fo(Hz)', 'MDVP:Fhi(Hz)', 'MDVP:Flo(Hz)', 'MDVP:Jitter(%)', 'MDVP:Jitter(Abs)',
        'MDVP:RAP', 'MDVP:PPQ', 'Jitter:DDP', 'MDVP:Shimmer', 'MDVP:Shimmer(dB)',
        'Shimmer:APQ3', 'Shimmer:APQ5', 'MDVP:APQ', 'Shimmer:DDA', 'NHR', 'HNR',
        'RPDE', 'DFA', 'spread1', 'spread2', 'D2', 'PPE'
    ]

    inputs = []
    for i in range(0, len(fields), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(fields):
                with cols[j]:
                    inputs.append(st.text_input(fields[i + j]))

    if st.button("🎯 Predict Parkinson's"):
        try:
            input_data = [float(x) for x in inputs]
            prediction = parkinsons_model.predict([input_data])[0]
            result = "🧠 The person has Parkinson's disease" if prediction == 1 else "✅ The person does not have Parkinson's disease"
            result_card(result)
        except:
            st.error("⚠️ Please enter valid numeric values.")

    with st.expander("💡 Did you know?", expanded=True):
        st.markdown(
            "- Early signs: **tremors**, **slowed movement**, and **voice changes**.\n"
            "- Regular **physical activity** helps maintain mobility.\n"
            "- Deep brain stimulation can improve symptoms in some cases."
        )

# -----------------------------
# Footer
# -----------------------------
st.markdown("""
    <hr style="border: 0.5px solid #888;">
    <p style="text-align:center; color: lightgray;">© 2025 Health Assistant — Built with ❤️ by Ashutosh Kumar</p>
""", unsafe_allow_html=True)
