import streamlit as st
import pandas as pd

st.title("💧 Jal Devta – Water Quality Checker")

@st.cache_data
def load_data():
    # Read CSV with proper headers set manually
    headers = [
        "S.No", "Year", "District", "Location", "Latitude", "Longitude", "pH", "EC", "Cl",
        "F (mg/L)", "NO3", "SO4", "Fe (ppm)", "As (ppb)", "U (ppb)", "Total Hardness", "Remarks",
        "Column18", "Column19", "Column20", "Column21", "Column22", "Column23", "Column24"
    ]
    df = pd.read_csv("water_quality.csv", names=headers, header=1)
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
                "Latitude": row["Latitude"],
                "Longitude": row["Longitude"],
                "pH": row["pH"],
                "EC": row["EC"],
                "Chloride (Cl)": row["Cl"],
                "Fluoride (F)": row["F (mg/L)"],
                "Nitrate (NO3)": row["NO3"],
                "Sulfate (SO4)": row["SO4"],
                "Iron (Fe)": row["Fe (ppm)"],
                "Arsenic (As)": row["As (ppb)"],
                "Uranium (U)": row["U (ppb)"],
                "Total Hardness": row["Total Hardness"],
                "Remarks": row["Remarks"]
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
