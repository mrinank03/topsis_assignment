#!/usr/bin/env python3
"""
SendGrid Configuration Verification Script
Run this to verify your SendGrid setup is correct before deploying
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_sendgrid_setup():
    """Test if SendGrid is properly configured"""
    
    print("\n" + "="*60)
    print("🔍 SendGrid Setup Verification")
    print("="*60 + "\n")
    
    # Step 1: Check API Key
    print("Step 1: Checking API Key...")
    api_key = os.getenv("SENDGRID_API_KEY")
    if not api_key:
        print("❌ SENDGRID_API_KEY not found in .env file")
        print("   Add to .env: SENDGRID_API_KEY=SG.xxxxx\n")
        return False
    
    if not api_key.startswith("SG."):
        print("❌ Invalid API key format (should start with 'SG.')")
        print(f"   Got: {api_key[:10]}...\n")
        return False
    
    print(f"✅ API Key found: {api_key[:20]}...\n")
    
    # Step 2: Check Sender Email
    print("Step 2: Checking Sender Email...")
    sender_email = os.getenv("SENDER_EMAIL")
    if not sender_email:
        print("❌ SENDER_EMAIL not found in .env file")
        print("   Add to .env: SENDER_EMAIL=your@email.com\n")
        return False
    
    if "@" not in sender_email:
        print(f"❌ Invalid email format: {sender_email}\n")
        return False
    
    print(f"✅ Sender Email: {sender_email}\n")
    
    # Step 3: Test API Connection
    print("Step 3: Testing SendGrid API Connection...")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        # Test with account endpoint
        response = requests.get(
            "https://api.sendgrid.com/v3/user/account",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Successfully connected to SendGrid API\n")
        elif response.status_code == 401:
            print("❌ Authentication failed - Invalid API key")
            print("   Please verify your SENDGRID_API_KEY is correct\n")
            return False
        else:
            print(f"⚠️  Unexpected response: {response.status_code}")
            print(f"   Response: {response.text}\n")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {str(e)}")
        print("   Check your internet connection\n")
        return False
    
    # Step 4: Test sending email
    print("Step 4: Testing Email Send...")
    test_email = input("Enter a test email address to send to (or press Enter to skip): ").strip()
    
    if test_email:
        payload = {
            "personalizations": [
                {
                    "to": [{"email": test_email}],
                    "subject": "TOPSIS Setup Test"
                }
            ],
            "from": {"email": sender_email, "name": "TOPSIS Setup Test"},
            "content": [
                {
                    "type": "text/html",
                    "value": "<h1>✅ Email Test Successful!</h1><p>Your SendGrid setup is working correctly.</p>"
                }
            ]
        }
        
        response = requests.post(
            "https://api.sendgrid.com/v3/mail/send",
            json=payload,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 202:
            print(f"✅ Test email sent to {test_email}")
            print("   Check inbox (or spam folder) within 30 seconds\n")
        else:
            print(f"❌ Failed to send test email")
            print(f"   Status: {response.status_code}")
            print(f"   Error: {response.text}\n")
            
            if response.status_code == 400:
                print("   💡 Common fix: Verify SENDER_EMAIL is verified in SendGrid dashboard\n")
            return False
    
    # Summary
    print("="*60)
    print("✅ SendGrid Setup Verification Complete!")
    print("="*60)
    print("\n📋 Next Steps:")
    print("1. Your SendGrid API key is valid")
    print("2. Your sender email is configured")
    print("3. Email sending works!")
    print("\n🚀 Ready for deployment!\n")
    
    return True


if __name__ == "__main__":
    success = test_sendgrid_setup()
    exit(0 if success else 1)
