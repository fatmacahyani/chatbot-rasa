#!/usr/bin/env python3

import asyncio
import logging
from rasa.core.agent import Agent

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_chatbot():
    """Test the chatbot with sample messages"""
    
    try:
        # Load the trained model
        agent = Agent.load("models")
        logger.info("✅ Model loaded successfully")
        
        # Test messages
        test_messages = [
            "halo",
            "apa saja jalur pendaftaran pascasarjana ITS?",
            "berapa biaya magister manajemen teknologi?",
            "syarat pendaftaran apa saja?",
            "kapan jadwal pendaftaran?",
            "terima kasih"
        ]
        
        print("\n" + "="*50)
        print("🤖 TESTING CHATBOT")
        print("="*50)
        
        for i, message in enumerate(test_messages, 1):
            print(f"\n👤 User: {message}")
            
            # Get bot response
            response = await agent.handle_text(message)
            
            if response:
                for msg in response:
                    print(f"🤖 Bot: {msg['text']}")
            else:
                print("🤖 Bot: No response")
            
            print("-" * 30)
        
        print("\n✅ Chatbot test completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Error during testing: {e}")
        print(f"\n❌ Test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_chatbot())