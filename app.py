
import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------------
# 1. Page configuration
# -------------------------------------
st.set_page_config(
    page_title="AI Student Performance Dashboard",
    page_icon="🎓",
    layout="wide"
)

# -------------------------------------
# 2. Application title
# -------------------------------------
st.title("🎓 AI Student Performance Dashboard")
st.write("Cloud-based student performance analysis")

# -------------------------------------
# 3. Load dataset
# -------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("students.csv")

df = load_data()

# -------------------------------------
# 4. Upload a new CSV dataset
# -------------------------------------
uploaded_file = st.file_uploader(
    "Upload student CSV file",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

# -------------------------------------
# 5. Calculate total and average
# -------------------------------------
subjects = [
    "AI",
    "Programming",
    "Statistics",
    "DataScience"
]

df["Total"] = df[subjects].sum(axis=1)

df["Average"] = df[subjects].mean(axis=1).round(2)

# -------------------------------------
# 6. Define performance level
# -------------------------------------
def performance_level(score):

    if score >= 85:
        return "Excellent"

    elif score >= 70:
        return "Good"

    elif score >= 50:
        return "Pass"

    else:
        return "Needs Support"

df["Performance"] = df["Average"].apply(
    performance_level
)

# -------------------------------------
# 7. Dashboard KPI cards
# -------------------------------------
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Students",
    len(df)
)

col2.metric(
    "Class Average",
    round(df["Average"].mean(), 2)
)

col3.metric(
    "Highest Average",
    round(df["Average"].max(), 2)
)

col4.metric(
    "Needs Support",
    int((df["Performance"] == "Needs Support").sum())
)

col5.metric(
    "Hiwa Omer Hassan",
    len(df)
)
st.divider()

# -------------------------------------
# 8. Search student
# -------------------------------------
st.subheader("🔍 Student Search")

search = st.text_input(
    "Enter Student Name or ID"
)

if search:

    filtered_df = df[
        df["Name"].astype(str).str.contains(
            search, case=False, na=False
        ) |
        df["Student_ID"].astype(str).str.contains(
            search, case=False, na=False
        )
    ]

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

else:

    st.dataframe(
        df,
        use_container_width=True
    )

# -------------------------------------
# 9. Student average chart
# -------------------------------------
st.subheader("📊 Student Average Scores")

fig1 = px.bar(
    df,
    x="Name",
    y="Average",
    color="Performance",
    title="Average Score by Student",
    text="Average"
)

fig1.update_layout(
    yaxis_range=[0, 100]
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# -------------------------------------
# 10. Subject comparison
# -------------------------------------
st.subheader("📚 Subject Performance")

subject_avg = df[subjects].mean().reset_index()

subject_avg.columns = [
    "Subject",
    "Average Score"
]

fig2 = px.bar(
    subject_avg,
    x="Subject",
    y="Average Score",
    color="Subject",
    title="Average Scores by Subject"
)

fig2.update_layout(
    yaxis_range=[0, 100]
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# -------------------------------------
# 11. Performance distribution
# -------------------------------------
st.subheader("🎯 Student Performance Levels")

performance_counts = (
    df["Performance"]
    .value_counts()
    .reset_index()
)

performance_counts.columns = [
    "Performance",
    "Students"
]

fig3 = px.pie(
    performance_counts,
    names="Performance",
    values="Students",
    title="Performance Distribution",
    hole=0.4
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# -------------------------------------
# 12. Download dataset
# -------------------------------------
st.subheader("📥 Download Results")

csv_data = df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download Student Report CSV",
    data=csv_data,
    file_name="student_report.csv",
    mime="text/csv"
)

# -------------------------------------
# 13. Footer
# -------------------------------------
st.success(
    "Application is running successfully!"
)

st.caption(
    "Cloud Computing Laboratory | AI Department"
)
