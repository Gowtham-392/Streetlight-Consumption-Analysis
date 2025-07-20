import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(
    page_title="Consumption Analysis Dashboard",
    page_icon="🔋",
    layout="wide"
)

st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stPlotlyChart {
        background-color: #ffffff;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
    </style>
    """, unsafe_allow_html=True)
# Load the dataset
@st.cache_data
def load_data():
    file_path = 'consumption.csv'  # Replace with the actual path
    data = pd.read_csv(file_path)
    return data

# Load data
try:
    data = load_data()

    
    # Title and description
    st.title('🔋 Consumption Analysis Dashboard')
    st.markdown('---')

    # Key Metrics
    st.header('Key Metrics Overview')
    total_services = data['totservices'].sum()
    billed_services = data['billdservices'].sum()
    total_units = data['units'].sum()
    total_load = data['load'].sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Services", f"{total_services:,}")
    col2.metric("Billed Services", f"{billed_services:,}")
    col3.metric("Total Units Consumed", f"{total_units:,.2f} kWh")
    col4.metric("Total Load", f"{total_load:,.2f} kW")

    # Category-wise Analysis
    st.markdown('---')
    st.header('Category-wise Analysis')
    category_data = data.groupby('catdesc')[['totservices', 'units']].sum().reset_index()
    fig = px.bar(category_data, x='catdesc', y=['totservices', 'units'],
                 title='Services and Units by Category',
                 labels={'value': 'Count', 'catdesc': 'Category'},
                 barmode='group')
    st.plotly_chart(fig, use_container_width=True)

    # Regional Trends
    st.markdown('---')
    st.header('Regional Trends')

    col5, col6 = st.columns(2)

    with col5:
        circle_data = data.groupby('circle')['totservices'].sum().sort_values(ascending=False).reset_index()
        fig = px.bar(circle_data, x='totservices', y='circle', orientation='h',
                     title='Total Services by Circle',
                     labels={'totservices': 'Total Services', 'circle': 'Circle'})
        st.plotly_chart(fig, use_container_width=True)

    with col6:
        division_data = data.groupby('division')['units'].sum().sort_values(ascending=False).reset_index()
        fig = px.bar(division_data, x='units', y='division', orientation='h',
                     title='Units Consumed by Division',
                     labels={'units': 'Units Consumed', 'division': 'Division'})
        st.plotly_chart(fig, use_container_width=True)

    # SLA Compliance - Stacked Bar Chart
    st.markdown('---')
    st.header('SLA Compliance Overview')
    sla_data = data.groupby('circle')[['billdservices', 'totservices']].sum().reset_index()
    fig = px.bar(sla_data, x='circle', y=['billdservices', 'totservices'],
                 title='Billed vs Total Services by Circle',
                 labels={'value': 'Count', 'circle': 'Circle'},
                 barmode='stack')
    st.plotly_chart(fig, use_container_width=True)

    # Treemap for Regional Trends
    st.markdown('---')
    st.header('Regional Breakdown')
    treemap_data = data.groupby(['circle', 'division'])[['totservices']].sum().reset_index()
    fig = px.treemap(treemap_data, path=['circle', 'division'], values='totservices',
                     title='Regional Breakdown of Services')
    st.plotly_chart(fig, use_container_width=True)

    # Interactive Data Explorer
    st.markdown('---')
    st.header('Interactive Data Explorer')

    selected_circle = st.selectbox('Select Circle', ['All'] + list(data['circle'].unique()))
    filtered_data = data if selected_circle == 'All' else data[data['circle'] == selected_circle]

    selected_metric = st.radio('Select Metric to Visualize', ['Total Services', 'Billed Services', 'Units Consumed'])
    metric_map = {
        'Total Services': 'totservices',
        'Billed Services': 'billdservices',
        'Units Consumed': 'units'
    }
    metric_col = metric_map[selected_metric]

    explorer_data = filtered_data.groupby('subdivision')[metric_col].sum().reset_index()
    fig = px.bar(explorer_data, x='subdivision', y=metric_col,
                 title=f'{selected_metric} by Subdivision',
                 labels={metric_col: selected_metric, 'subdivision': 'Subdivision'})
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    st.info("Please ensure the dataset is correctly formatted and accessible.")
