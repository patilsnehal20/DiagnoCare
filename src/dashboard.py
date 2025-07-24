import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# ------------------------ PAGE SETTINGS ------------------------
st.set_page_config(page_title="Medical Imaging Dashboard", layout="wide")
if st.button("Back"):
    st.switch_page("pages/Insights.py")
st.markdown(
    """
    <style>
    .main {
        background-color: #FFFFFF;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------ MAIN DASHBOARD ------------------------

def main():
    st.title("Medical Imaging Data Dashboard")

    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        st.success("File uploaded successfully!")
        
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()

        st.subheader("Data Preview")
        st.dataframe(df.head())

        st.subheader("Summary Statistics")
        st.dataframe(df.describe(include='all'))

        st.sidebar.header("Choose Plot Type")

        plot_type = st.sidebar.selectbox(
            "Select the plot you want to see:",
            ("Histogram", "Pie Chart", "Scatter Plot", "Box Plot", "Correlation Heatmap")
        )

        if plot_type == "Histogram":
            column = st.sidebar.selectbox("Select numeric column for Histogram:", numeric_cols)
            if column:
                fig = px.histogram(df, x=column, nbins=20, title=f"Histogram of {column}")
                st.plotly_chart(fig, use_container_width=True)

        elif plot_type == "Pie Chart":
            column = st.sidebar.selectbox("Select categorical column for Pie Chart:", categorical_cols)
            if column:
                fig = px.pie(df, names=column, title=f"Pie Chart of {column}")
                st.plotly_chart(fig, use_container_width=True)

        elif plot_type == "Scatter Plot":
            x_col = st.sidebar.selectbox("Select X-axis (numeric):", numeric_cols)
            y_col = st.sidebar.selectbox("Select Y-axis (numeric):", numeric_cols)
            color_col = st.sidebar.selectbox("Select Color by (optional):", [None] + categorical_cols)
            if x_col and y_col:
                fig = px.scatter(df, x=x_col, y=y_col, color=color_col, title=f"{y_col} vs {x_col}")
                st.plotly_chart(fig, use_container_width=True)

        elif plot_type == "Box Plot":
            x_col = st.sidebar.selectbox("Select X-axis (categorical):", categorical_cols)
            y_col = st.sidebar.selectbox("Select Y-axis (numeric):", numeric_cols)
            if x_col and y_col:
                fig = px.box(df, x=x_col, y=y_col, title=f"Box Plot of {y_col} by {x_col}")
                st.plotly_chart(fig, use_container_width=True)

        elif plot_type == "Correlation Heatmap":
            st.subheader("Correlation Heatmap")
            corr = df[numeric_cols].corr()
            fig, ax = plt.subplots(figsize=(12, 8))
            sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
            st.pyplot(fig)

    else:
        st.info("Please upload a CSV file to get started.")

if __name__ == "__main__":
    main()
