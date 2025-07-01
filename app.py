import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

# Configure page
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# Create sample data (replace with your actual data)
@st.cache_data  # Cache data for better performance
def load_data():
    data = {
        'Region': ['North', 'South', 'East', 'West', 'Central'] * 12,
        'Sales': [100, 150, 120, 180, 140, 110, 160, 130, 190, 145, 
                 105, 155, 125, 185, 142, 115, 165, 135, 195, 150,
                 108, 158, 128, 188, 144, 118, 168, 138, 198, 152,
                 112, 162, 132, 192, 146, 122, 172, 142, 202, 156,
                 116, 166, 136, 196, 148, 126, 176, 146, 206, 160,
                 120, 170, 140, 200, 150, 130, 180, 150, 210, 164],
        'Month': ['Jan', 'Jan', 'Jan', 'Jan', 'Jan', 'Feb', 'Feb', 'Feb', 'Feb', 'Feb',
                 'Mar', 'Mar', 'Mar', 'Mar', 'Mar', 'Apr', 'Apr', 'Apr', 'Apr', 'Apr',
                 'May', 'May', 'May', 'May', 'May', 'Jun', 'Jun', 'Jun', 'Jun', 'Jun',
                 'Jul', 'Jul', 'Jul', 'Jul', 'Jul', 'Aug', 'Aug', 'Aug', 'Aug', 'Aug',
                 'Sep', 'Sep', 'Sep', 'Sep', 'Sep', 'Oct', 'Oct', 'Oct', 'Oct', 'Oct',
                 'Nov', 'Nov', 'Nov', 'Nov', 'Nov', 'Dec', 'Dec', 'Dec', 'Dec', 'Dec'],
        'Product': ['Widget A', 'Widget A', 'Widget A', 'Widget A', 'Widget A'] * 12,
        'Revenue': [1000, 1500, 1200, 1800, 1400] * 12
    }
    return pd.DataFrame(data)

# Load data
df = load_data()

# Title and description
st.title("📊 Sales Dashboard Demo")
st.markdown("**Interactive dashboard for testing business logic**")
st.markdown("---")

# Sidebar for controls
st.sidebar.header("Dashboard Controls")

# Dropdown for chart type
chart_type = st.sidebar.selectbox(
    "Select Chart Type:",
    options=["Sales by Region", "Sales by Month", "Revenue Trends", "Product Performance"],
    index=0
)

# Additional filters
selected_months = st.sidebar.multiselect(
    "Filter by Months:",
    options=df['Month'].unique(),
    default=df['Month'].unique()[:6]  # Default to first 6 months
)

# Filter data based on selection
filtered_df = df[df['Month'].isin(selected_months)]

# Main content area
col1, col2 = st.columns([3, 1])

with col1:
    # Create charts based on selection
    if chart_type == "Sales by Region":
        fig = px.bar(
            filtered_df.groupby('Region')['Sales'].sum().reset_index(),
            x='Region', 
            y='Sales',
            title='Total Sales by Region',
            color='Region',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
    elif chart_type == "Sales by Month":
        monthly_sales = filtered_df.groupby('Month')['Sales'].sum().reset_index()
        fig = px.line(
            monthly_sales,
            x='Month', 
            y='Sales',
            title='Sales Trend by Month',
            markers=True,
            line_shape='spline'
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
    elif chart_type == "Revenue Trends":
        revenue_data = filtered_df.groupby(['Month', 'Region'])['Revenue'].sum().reset_index()
        fig = px.line(
            revenue_data,
            x='Month', 
            y='Revenue',
            color='Region',
            title='Revenue Trends by Region',
            markers=True
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
    else:  # Product Performance
        product_data = filtered_df.groupby('Product')['Sales'].sum().reset_index()
        fig = px.pie(
            product_data,
            values='Sales', 
            names='Product',
            title='Sales Distribution by Product'
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

with col2:
    # Summary metrics
    st.subheader("📈 Key Metrics")
    
    total_sales = filtered_df['Sales'].sum()
    avg_sales = filtered_df['Sales'].mean()
    total_revenue = filtered_df['Revenue'].sum()
    
    st.metric("Total Sales", f"{total_sales:,}")
    st.metric("Average Sales", f"{avg_sales:.1f}")
    st.metric("Total Revenue", f"${total_revenue:,}")
    
    # Top performing region
    top_region = filtered_df.groupby('Region')['Sales'].sum().idxmax()
    top_sales = filtered_df.groupby('Region')['Sales'].sum().max()
    
    st.subheader("🏆 Top Performer")
    st.success(f"**{top_region}**\n\n{top_sales:,} sales")

# Data table section
st.markdown("---")
st.subheader("📋 Raw Data Preview")

# Show/hide data table
if st.checkbox("Show filtered data"):
    st.dataframe(filtered_df, use_container_width=True)

# Download functionality
st.subheader("💾 Export Data")
csv = filtered_df.to_csv(index=False)
st.download_button(
    label="Download filtered data as CSV",
    data=csv,
    file_name="dashboard_data.csv",
    mime="text/csv"
)

# Footer
st.markdown("---")
st.markdown("*Dashboard created for business logic testing*")

