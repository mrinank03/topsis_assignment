import streamlit as st
import pandas as pd
import io
import os
from dotenv import load_dotenv
import numpy as np
import requests

# Load environment variables (for local development)
load_dotenv()

def send_email_with_sendgrid(recipient_email: str, df, weights: str, impacts: str):
    """
    Send TOPSIS results using SendGrid API (works on Streamlit Cloud)
    """
    api_key = st.secrets.get("SENDGRID_API_KEY") or os.getenv("SENDGRID_API_KEY")
    sender_email = st.secrets.get("SENDER_EMAIL") or os.getenv("SENDER_EMAIL")
    
    if not api_key:
        raise ValueError("SENDGRID_API_KEY not found. Add it to Streamlit Cloud Secrets or .env file.")
    if not sender_email:
        raise ValueError("SENDER_EMAIL not found. Add it to Streamlit Cloud Secrets or .env file.")
    
    # Build email body
    body_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #007bff; color: white; padding: 20px; border-radius: 5px; }}
            .content {{ padding: 20px; }}
            .info {{ background-color: #f0f0f0; padding: 10px; margin: 10px 0; border-left: 4px solid #007bff; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
            th {{ background-color: #007bff; color: white; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎯 TOPSIS Analysis Results</h1>
            </div>
            <div class="content">
                <p>Hello,</p>
                <p>Your TOPSIS analysis has been completed successfully.</p>
                
                <div class="info">
                    <strong>Analysis Configuration:</strong><br>
                    Weights: {weights}<br>
                    Impacts: {impacts}
                </div>
                
                <h3>Summary Statistics:</h3>
                <ul>
                    <li><strong>Best Score:</strong> {df['Topsis Score'].max():.4f}</li>
                    <li><strong>Worst Score:</strong> {df['Topsis Score'].min():.4f}</li>
                    <li><strong>Average Score:</strong> {df['Topsis Score'].mean():.4f}</li>
                    <li><strong>Total Alternatives:</strong> {len(df)}</li>
                </ul>
                
                <h3>Top 3 Alternatives:</h3>
                <table>
                    <tr>
                        <th>Rank</th>
                        <th>Alternative</th>
                        <th>Score</th>
                    </tr>
    """
    
    # Add top 3
    top_3 = df.nsmallest(3, 'Rank')[['Alternative', 'Topsis Score', 'Rank']].sort_values('Rank')
    for idx, row in top_3.iterrows():
        body_html += f"""
                    <tr>
                        <td>#{int(row['Rank'])}</td>
                        <td>{row['Alternative']}</td>
                        <td>{row['Topsis Score']:.4f}</td>
                    </tr>
        """
    
    body_html += """
                </table>
                <p>Thank you for using TOPSIS Decision Support Tool!</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # SendGrid API payload
    payload = {
        "personalizations": [
            {
                "to": [{"email": recipient_email}],
                "subject": "Your TOPSIS Analysis Results"
            }
        ],
        "from": {"email": sender_email, "name": "TOPSIS Tool"},
        "content": [
            {
                "type": "text/html",
                "value": body_html
            }
        ]
    }
    
    # Send via SendGrid API
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(
        "https://api.sendgrid.com/v3/mail/send",
        json=payload,
        headers=headers
    )
    
    if response.status_code != 202:
        error_msg = response.text if response.text else f"Status code: {response.status_code}"
        raise Exception(f"SendGrid API error: {error_msg}")
    
    return True

# Page configuration
st.set_page_config(
    page_title="TOPSIS Decision Support Tool",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stTitle {
        color: #ffffff;
        text-align: center;
        padding: 2rem 0;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎯 TOPSIS Decision Support Tool")
st.markdown("---")

# Create columns for layout
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📁 Upload CSV File")
    st.write("The first column should contain alternative names, and subsequent columns should contain numerical criteria values.")
    
    # Download sample CSV
    if st.button("📥 Download Sample CSV"):
        sample_data = {
            'Alternative': ['A1', 'A2', 'A3', 'A4'],
            'Criterion 1': [250, 200, 300, 275],
            'Criterion 2': [16, 20, 12, 14],
            'Criterion 3': [12, 8, 15, 10]
        }
        df_sample = pd.DataFrame(sample_data)
        csv = df_sample.to_csv(index=False)
        st.download_button(
            label="Download sample_data.csv",
            data=csv,
            file_name="sample_data.csv",
            mime="text/csv"
        )
    
    # File upload
    uploaded_file = st.file_uploader(
        "Drag and drop file here",
        type="csv",
        help="Limit 200MB per file • CSV"
    )

with col2:
    st.subheader("⚙️ Configure TOPSIS")
    
    weights_input = st.text_input(
        "Enter weights (comma-separated, sum should be 1.0)",
        placeholder="1,1,1",
        help="e.g., 0.5,0.3,0.2 or 1,1,1"
    )
    
    impacts_input = st.text_input(
        "Enter impacts (+ or -, comma-separated)",
        placeholder="+,+,-",
        help="+ for benefit criteria, - for cost criteria. e.g., +,+,-,+"
    )
    
    email_input = st.text_input(
        "Enter email address (optional)",
        placeholder="your.email@example.com",
        help="Results will be emailed to this address"
    )

st.markdown("---")

# Main processing
if st.button("🚀 Run TOPSIS", use_container_width=True):
    if uploaded_file is None:
        st.error("❌ Please upload a CSV file")
    elif not weights_input.strip():
        st.error("❌ Please enter weights")
    elif not impacts_input.strip():
        st.error("❌ Please enter impacts")
    else:
        try:
            # Read the uploaded file
            df = pd.read_csv(uploaded_file)
            
            # Validate input
            if df.shape[1] < 3:
                st.error("❌ Input file must contain at least 3 columns (1 name + 2 criteria)")
            else:
                # Import TOPSIS from the PyPI package
                try:
                    from topsis_mrinank_102303235.cli import (
                        parse_weights, 
                        parse_impacts, 
                        ensure_numeric, 
                        compute_topsis
                    )
                except ImportError:
                    st.error("❌ TOPSIS package not installed. Install with: pip install topsis-mrinank-102303235")
                    st.stop()
                
                # Parse inputs
                num_criteria = df.shape[1] - 1
                weights = parse_weights(weights_input)
                impacts = parse_impacts(impacts_input)
                
                # Validate
                if len(weights) != num_criteria:
                    st.error(f"❌ Number of weights ({len(weights)}) must equal number of criteria ({num_criteria})")
                elif len(impacts) != num_criteria:
                    st.error(f"❌ Number of impacts ({len(impacts)}) must equal number of criteria ({num_criteria})")
                else:
                    # Process TOPSIS
                    criteria_data = ensure_numeric(df, list(range(1, df.shape[1])))
                    data_mat = criteria_data.values
                    score = compute_topsis(data_mat, weights, impacts)
                    
                    # Add results to dataframe
                    df['Topsis Score'] = np.round(score, 6)
                    df['Rank'] = df['Topsis Score'].rank(method='max', ascending=False).astype(int)
                    
                    # Display results
                    st.success("✅ TOPSIS calculation completed successfully!")
                    
                    # Show results table
                    st.subheader("📊 Results")
                    st.dataframe(df, use_container_width=True)
                    
                    # Download results
                    csv_results = df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Results as CSV",
                        data=csv_results,
                        file_name="topsis_results.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                    
                    # Send email if provided
                    if email_input.strip():
                        if st.button("📧 Send Results to Email", use_container_width=True):
                            try:
                                send_email_with_sendgrid(
                                    email_input.strip(),
                                    df,
                                    weights_input,
                                    impacts_input
                                )
                                st.success(f"✅ Results sent successfully to {email_input.strip()}")
                            except Exception as e:
                                st.error(f"❌ Failed to send email: {str(e)}")
                                st.info("📋 Setup Instructions:\n1. Get SendGrid API key: https://sendgrid.com\n2. Go to Streamlit Cloud Dashboard → App Settings → Secrets\n3. Add: `SENDGRID_API_KEY = 'SG.xxxxx'`\n4. Add: `SENDER_EMAIL = 'your@email.com'`")
                    
                    # Show statistics
                    st.subheader("📈 Statistics")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Best Score", f"{df['Topsis Score'].max():.4f}")
                    with col2:
                        st.metric("Worst Score", f"{df['Topsis Score'].min():.4f}")
                    with col3:
                        st.metric("Average Score", f"{df['Topsis Score'].mean():.4f}")
                    
                    # Show ranking
                    st.subheader("🏆 Rankings")
                    ranking_df = df[['Alternative', 'Topsis Score', 'Rank']].sort_values('Rank')
                    for idx, row in ranking_df.iterrows():
                        medal = "🥇" if row['Rank'] == 1 else "🥈" if row['Rank'] == 2 else "🥉" if row['Rank'] == 3 else f"#{row['Rank']}"
                        st.write(f"{medal} **{row['Alternative']}** - Score: {row['Topsis Score']:.4f}")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #888;">
        <p>TOPSIS Decision Support Tool | Powered by Streamlit</p>
        <p>For issues or feedback, contact: mrinankjit@gmail.com</p>
    </div>
""", unsafe_allow_html=True)
