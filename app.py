import streamlit as st
import pandas as pd

st.title("💧 Jal Devta – Water Quality Checker")

@st.cache_data
def load_data():
    df = pd.read_csv("water_quality.csv")
    return df

df = load_data()
df.columns = df.columns.str.strip()

user_input = st.text_input("Enter your District or Location:")

if user_input:
    results = df[df['District'].str.contains(user_input, case=False) |
                 df['Location'].str.contains(user_input, case=False)]

    if not results.empty:
        for index, row in results.iterrows():
            st.subheader(f"📍 {row['Location']} ({row['District']})")

            st.write({
                "Year": row["Year"],
                "pH": row["pH"],
                "Fluoride (F)": row["F (mg/L)"],
                "Nitrate (NO3)": row["NO3"],
                "Arsenic (As)": row["As (ppb)"],
                "Uranium (U)": row["U (ppb)"],
                "Iron (Fe)": row["Fe (ppm)"],
                "Total Hardness": row["Total Hardness"]
            })

            comments = []

            try:
                if row["pH"] < 6.5 or row["pH"] > 8.5:
                    comments.append("⚠️ pH is outside safe range (6.5–8.5).")
                if row["F (mg/L)"] > 1.5:
                    comments.append("⚠️ Fluoride above 1.5 mg/L – risk of fluorosis.")
                if row["NO3"] > 50:
                    comments.append("⚠️ Nitrate above 50 mg/L – unsafe for infants.")
                if row["As (ppb)"] > 10:
                    comments.append("⚠️ Arsenic above 10 ppb – may cause cancer.")
                if row["U (ppb)"] > 30:
                    comments.append("⚠️ Uranium above 30 ppb – kidney risk.")
                if row["Fe (ppm)"] > 0.3:
                    comments.append("⚠️ Iron above 0.3 ppm – metallic taste possible.")

                if not comments:
                    st.success("✅ Water appears safe as per standard parameters.")
                else:
                    for comment in comments:
                        st.warning(comment)
            except:
                st.error("⚠️ Error checking values for this entry.")
    else:
        st.info("❌ No data found for that location.")
else:
    st.write("🔎 Please enter a location or district to begin.")
