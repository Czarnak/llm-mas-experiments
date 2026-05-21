import streamlit as st
import requests
import pandas as pd
from typing import Dict, List

# Initialize session state
if 'reports' not in st.session_state:
    st.session_state.reports = []

st.set_page_config(page_title="Health Agent System - Admin Dashboard", layout="wide")

st.title("🏥 Health Agent System - Admin Dashboard")

# API base URL
API_BASE_URL = "http://localhost:8000"

# Function to fetch reports
@st.cache_data(ttl=60)
def fetch_reports():
    try:
        response = requests.get(f"{API_BASE_URL}/reports")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching reports: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
        return []

# Function to fetch detailed report
@st.cache_data(ttl=60)
def fetch_detailed_report(report_id: str):
    try:
        response = requests.get(f"{API_BASE_URL}/reports/{report_id}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching report: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
        return None

# Main dashboard content
st.subheader("📊 Recent Reports")

# Fetch reports
reports = fetch_reports()

if not reports:
    st.info("No reports available yet.")
else:
    # Display reports in a table
    df = pd.DataFrame(reports)
    
    # Display basic information
    st.dataframe(df[['id', 'symptoms', 'potential_disease', 'medical_field', 'timestamp', 'location']], 
                use_container_width=True)
    
    # Detailed view section
    st.subheader("🔍 Detailed Report View")
    
    # Select report to view details
    report_ids = [report['id'] for report in reports]
    selected_report_id = st.selectbox("Select a report to view details:", report_ids)
    
    if selected_report_id:
        detailed_report = fetch_detailed_report(selected_report_id)
        if detailed_report:
            st.write("### Detailed Report Information")
            st.json(detailed_report)

# Refresh button
if st.button("🔄 Refresh Reports"):
    st.experimental_rerun()

# Health check
st.subheader("🏥 System Status")
try:
    response = requests.get(f"{API_BASE_URL}/health")
    if response.status_code == 200:
        st.success("✅ API is running and healthy")
    else:
        st.error("❌ API is not responding")
except Exception as e:
    st.error(f"❌ Error connecting to API: {str(e)}")
