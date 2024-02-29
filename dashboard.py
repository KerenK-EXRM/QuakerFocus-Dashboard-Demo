# Import necessary libraries
import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image

# Defining column names as constants
GENDER_COLUMN = 'Gender'
ETHNICITY_COLUMN = 'Ethnicity'
AGE_RANGE_COLUMN = 'Age Range'
EMPLOYMENT_STATUS_COLUMN = 'Employment Status'
ANNUAL_INCOME_COLUMN = 'Approximate Annual Household Income'
EDUCATION_LEVEL_COLUMN = 'Education level'
PERMANENT_DISABLE_COLUMN = "Do you agree that the plaintiff is permanently disabled as a result of the accident?"

# Constants for paths and color scheme
DATASET_PATH = "C:\\Test\\FocusGroupAI\\test.csv"
LOGO_PATH = "C:\\Test\\FocusGroupAI\\QuakerAnalytics_Logo_Stacked_GradientA.png"
COLOR_SCHEME = ['#1A85FF', '#005AB5', '#08366F', '#EE3177', '#D41159', '#666666']

# Load data with encoding handling
def load_data(filepath):
    try:
        df = pd.read_csv(filepath, encoding='utf-8')
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(filepath, encoding='ISO-8859-1')
        except:
            df = pd.read_csv(filepath, encoding='utf-8', errors='ignore')
    return df

# Function to plot donut charts
def plot_donut_chart(df, column_name, title, color_discrete_sequence):
    fig = px.pie(df, names=column_name, title=title, hole=0.5, 
                 color_discrete_sequence=color_discrete_sequence)
    fig.update_traces(textinfo='percent+label', hoverinfo='label+percent', showlegend=True)
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5))
    return fig

# Function to plot bar chart
def plot_bar_chart(df, column_name, title, color_discrete_sequence):
    df_count = df[column_name].value_counts().reset_index()
    df_count.columns = ['category', 'counts']
    fig = px.bar(df_count, x='category', y='counts', title=title,
                 color='category', color_discrete_sequence=color_discrete_sequence)
    return fig

# Streamlit interface setup
st.set_page_config(layout="wide")
logo = Image.open(LOGO_PATH)
st.sidebar.image(logo, width=120)
st.markdown("<h1 style='text-align: center; color: #08366F;'>Focus Group Response Dashboard</h1>", unsafe_allow_html=True)

data = load_data(DATASET_PATH)

# Sidebar filters
gender_filter = st.sidebar.multiselect("Gender", options=data[GENDER_COLUMN].unique())
ethnicity_filter = st.sidebar.multiselect("Ethnicity", options=data[ETHNICITY_COLUMN].unique())
employment_status_filter = st.sidebar.multiselect("Employment Status", options=data[EMPLOYMENT_STATUS_COLUMN].unique())
age_range_filter = st.sidebar.multiselect("Age Range", options=data[AGE_RANGE_COLUMN].unique())

filtered_data = data.copy()
if gender_filter:
    filtered_data = filtered_data[filtered_data[GENDER_COLUMN].isin(gender_filter)]
if ethnicity_filter:
    filtered_data = filtered_data[filtered_data[ETHNICITY_COLUMN].isin(ethnicity_filter)]
if employment_status_filter:
    filtered_data = filtered_data[filtered_data[EMPLOYMENT_STATUS_COLUMN].isin(employment_status_filter)]
if age_range_filter:
    filtered_data = filtered_data[filtered_data[AGE_RANGE_COLUMN].isin(age_range_filter)]

# Display Visualizations
col1, col2, col3 = st.columns(3)
with col1:
    st.plotly_chart(plot_donut_chart(filtered_data, GENDER_COLUMN, "Gender Distribution", COLOR_SCHEME), use_container_width=True)
with col2:
    st.plotly_chart(plot_donut_chart(filtered_data, ETHNICITY_COLUMN, "Ethnicity Distribution", COLOR_SCHEME), use_container_width=True)
with col3:
    st.plotly_chart(plot_donut_chart(filtered_data, AGE_RANGE_COLUMN, "Age Range Distribution", COLOR_SCHEME), use_container_width=True)

col4, col5, col6 = st.columns(3)
with col4:
    st.plotly_chart(plot_donut_chart(filtered_data, EMPLOYMENT_STATUS_COLUMN, "Employment Status", COLOR_SCHEME), use_container_width=True)
with col5:
    st.plotly_chart(plot_donut_chart(filtered_data, ANNUAL_INCOME_COLUMN, "Annual Income Distribution", COLOR_SCHEME), use_container_width=True)
with col6:
    st.plotly_chart(plot_donut_chart(filtered_data, EDUCATION_LEVEL_COLUMN, "Education Level Distribution", COLOR_SCHEME), use_container_width=True)

st.plotly_chart(plot_bar_chart(filtered_data, PERMANENT_DISABLE_COLUMN, "Permanently Disabled", COLOR_SCHEME), use_container_width=True)