import streamlit as st
import pyrebase
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import date

firebaseConfig = {
    "apiKey": "AIzaSyBuxnQ0FlM4HRNY38VnvLHqXXLsiLNsDvc",
    "authDomain": "sleep-productivity-tracker.firebaseapp.com",
    "databaseURL": "https://sleep-productivity-tracker-default-rtdb.firebaseio.com",
    "projectId": "sleep-productivity-tracker",
    "storageBucket": "sleep-productivity-tracker.appspot.com",
    "messagingSenderId": "41046554692",
    "appId": "1:41046554692:web:a9ed8981f583538c0b2411",
    "measurementId": "G-FQBY8X1D43"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

st.markdown("""
    <style>
    .main { background-color: #f0f2f6; padding: 20px; }
    .title { font-size: 42px; color: #333; text-align: center; margin-bottom: 25px; }
    .box { background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.08); }
    .stButton button { background-color: #4CAF50; color: white; border: none; padding: 12px 28px; border-radius: 10px; }
    .stButton button:hover { background-color: #45a049; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">Sleep vs Productivity Tracker</div>', unsafe_allow_html=True)

page = st.sidebar.selectbox("Go to", ["Enter Data", "View Dashboard"])

if page == "Enter Data":
    st.subheader("Enter Today's Data")
    sleep_input = st.text_input("Sleep Hours (0-24):")
    prod_input = st.text_input("Productivity Score (1-10):")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Submit"):
        try:
            sleep_hours = float(sleep_input)
            productivity = float(prod_input)

            if not (0 <= sleep_hours <= 24) or not (1 <= productivity <= 10):
                st.error("Enter valid values: Sleep (0-24) and Productivity (1-10)")
            else:
                data = {
                    "date": str(date.today()),
                    "sleep_hours": sleep_hours,
                    "productivity": productivity
                }
                db.child("tracker_data").push(data)
                st.success("Data submitted successfully!")

        except ValueError:
            st.error("Please enter numeric values only.")

elif page == "View Dashboard":
    st.subheader("📊 Dashboard")

    result = db.child("tracker_data").get()

    if result.each():
        records = [item.val() for item in result.each()]
        df = pd.DataFrame(records)
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date")

        st.markdown("### Sleep Hours Over Time")
        fig1 = px.line(df, x="date", y="sleep_hours", markers=True)
        fig1.update_traces(line_color="#4CAF50", marker=dict(size=10, color="black"))
        fig1.update_layout(template="plotly_white")
        st.plotly_chart(fig1, use_container_width=True)

        st.markdown("### Productivity Levels")
        fig2 = px.bar(df, x="date", y="productivity", color="productivity",
                      color_continuous_scale="Viridis")
        fig2.update_layout(template="plotly_white")
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown("### Latest Sleep vs Awake")
        latest = df.iloc[-1]
        sleep = latest["sleep_hours"]
        awake = 24 - sleep
        fig3, ax = plt.subplots()
        ax.pie([sleep, awake],
               labels=["Sleep", "Awake"],
               autopct='%1.1f%%',
               startangle=90,
               colors=["#4CAF50", "#FFC107"],
               wedgeprops={"edgecolor": "black"})
        ax.axis('equal')
        st.pyplot(fig3)

        avg_sleep = df["sleep_hours"].mean()
        avg_prod = df["productivity"].mean()

        st.info(f"**Average Sleep:** {avg_sleep:.1f} hrs | **Average Productivity:** {avg_prod:.1f} / 10")

        st.markdown("### Insights")
        if sleep < 5:
            st.warning(" Too little sleep yesterday. Rest more today.")
        elif sleep >= 8:
            st.success(" Great sleep hours!")

        if latest["productivity"] < 4:
            st.warning("Low productivity yesterday — adjust your routine.")
        elif latest["productivity"] >= 8:
            st.success(" High productivity! Keep going.")

    else:
        st.info("No data yet. Go to 'Enter Data' and submit values.")
