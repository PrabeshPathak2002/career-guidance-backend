"""
Test script to verify rate limiting functionality.
Run this to test if rate limits are working properly.
"""

import requests
import time
import json

BASE_URL = "http://localhost:8000"

def test_rate_limits():
    """Test various endpoints to ensure rate limiting is working."""
    
    print("🧪 Testing Rate Limits for Career Guidance API")
    print("=" * 50)
    
    # Test 1: Root endpoint (30/minute)
    print("\n1. Testing root endpoint (limit: 30/minute)")
    for i in range(35):
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 429:  # Too Many Requests
            print(f"   ✅ Rate limit hit after {i+1} requests")
            break
        elif i == 34:
            print(f"   ⚠️  Rate limit not hit after {i+1} requests")
    
    time.sleep(2)  # Wait a bit
    
    # Test 2: Session creation (20/minute)
    print("\n2. Testing session creation (limit: 20/minute)")
    for i in range(25):
        response = requests.post(f"{BASE_URL}/session")
        if response.status_code == 429:
            print(f"   ✅ Rate limit hit after {i+1} requests")
            break
        elif i == 24:
            print(f"   ⚠️  Rate limit not hit after {i+1} requests")
    
    time.sleep(2)
    
    # Test 3: AI recommendations (10/minute) - most expensive
    print("\n3. Testing AI recommendations (limit: 10/minute)")
    # First create a session and add some answers
    session_response = requests.post(f"{BASE_URL}/session")
    if session_response.status_code == 200:
        session_data = session_response.json()
        session_id = session_data["session_id"]
        
        # Add a test answer
        answer_data = {"session_id": session_id, "answer": "I like technology and problem solving"}
        requests.post(f"{BASE_URL}/answer", json=answer_data)
        
        # Test recommendation endpoint
        for i in range(15):
            response = requests.get(f"{BASE_URL}/recommend?session_id={session_id}")
            if response.status_code == 429:
                print(f"   ✅ Rate limit hit after {i+1} requests")
                break
            elif i == 14:
                print(f"   ⚠️  Rate limit not hit after {i+1} requests")
    else:
        print("   ❌ Could not create session for testing")
    
    print("\n" + "=" * 50)
    print("🎯 Rate limit testing complete!")
    print("Note: If limits aren't hit, it might be because the time window has passed.")

if __name__ == "__main__":
    try:
        test_rate_limits()
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API. Make sure it's running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error during testing: {e}") 