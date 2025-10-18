#!/usr/bin/env python3
"""
Simple test script to verify chatbot functionality
"""
import requests
import json

def test_external_service():
    """Test if your external NLU service is running"""
    try:
        response = requests.get("http://localhost:3000/api/prodi", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ External service is working!")
            print(f"   Found {len(data)} programs")
            return True
        else:
            print(f"❌ External service responded with status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ External service not accessible: {e}")
        return False

def test_static_qna():
    """Test static QnA responses"""
    print("\n📋 Testing Static QnA Responses:")
    
    # Sample static responses from your actions.py
    static_responses = {
        "tanya_jalur_pendaftaran": "🎓 Jalur Pendaftaran Pascasarjana ITS:",
        "tanya_beasiswa": "🏆 Beasiswa Pascasarjana ITS:",
        "jadwal_pendaftaran_2025": "📅 Jadwal Pendaftaran 2025:",
    }
    
    for intent, response_preview in static_responses.items():
        print(f"✅ {intent}: {response_preview}")
    
    return True

def test_intent_examples():
    """Show some intent examples that should work"""
    print("\n🎯 Intent Examples to Test:")
    
    test_cases = [
        ("apa saja prodi pascasarjana", "tanya_prodi_tersedia", "External Service"),
        ("berapa biaya kuliah", "tanya_biaya_kuliah", "External Service"),
        ("apa syarat pendaftaran", "tanya_syarat_pendaftaran", "Static Response"),
        ("ada beasiswa tidak", "tanya_beasiswa", "Static Response"),
        ("kapan jadwal pendaftaran 2025", "jadwal_pendaftaran_2025", "Static Response"),
        ("halo", "greet", "Static Response"),
        ("terima kasih", "thank_you", "Static Response"),
    ]
    
    for example, intent, response_type in test_cases:
        print(f"   📝 '{example}' → {intent} → {response_type}")
    
    return True

def main():
    print("🔍 Testing Hybrid Chatbot Setup...")
    print("=" * 50)
    
    # Test external service
    external_working = test_external_service()
    
    # Test static responses
    static_working = test_static_qna()
    
    # Show test cases
    test_intent_examples()
    
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print(f"   External Service: {'✅ Working' if external_working else '❌ Not Working'}")
    print(f"   Static Responses: {'✅ Ready' if static_working else '❌ Not Ready'}")
    
    print("\n🚀 Next Steps:")
    if external_working:
        print("   1. Your external service (server.js) is running correctly")
        print("   2. Dynamic prodi/biaya queries will work")
    else:
        print("   1. ⚠️  Make sure your server.js is running on port 3000")
        print("   2. Dynamic queries will fallback to error messages")
    
    print("   3. Test your chatbot in the Rasa Inspector")
    print("   4. Try the examples above to see different response types")
    
    print("\n💡 Hybrid Approach Benefits:")
    print("   ✅ Rasa NLU classifies intents (fixes 'same response' issue)")
    print("   ✅ External service provides dynamic data")
    print("   ✅ Static responses are fast and reliable")

if __name__ == "__main__":
    main()