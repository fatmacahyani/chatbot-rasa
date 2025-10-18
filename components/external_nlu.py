import requests
from typing import Any, Dict, List, Text, Optional
from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.constants import INTENT, ENTITIES

@DefaultV1Recipe.register(
    component_class="components.external_nlu.ExternalNLU", is_trainable=False
)
class ExternalNLU(GraphComponent):
    
    @classmethod
    def create(
        cls,
        config: Dict[Text, Any],
        execution_context: ExecutionContext,
    ) -> "ExternalNLU":
        return cls(config)
    
    def __init__(self, config: Dict[Text, Any]) -> None:
        self.nlu_url = config.get("url", "http://localhost:3000/parse")
        print(f"🔗 External NLU initialized: {self.nlu_url}")
    
    def process(self, messages: List[Message]) -> List[Message]:
        for message in messages:
            text = message.get("text")
            print(f"🔍 Processing: {text}")
            
            try:
                response = requests.post(
                    self.nlu_url,
                    json={"text": text},
                    timeout=5,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ External NLU Response: {data}")
                    
                    # Set intent
                    message.set(INTENT, {
                        "name": data["intent"]["name"],
                        "confidence": data["intent"]["confidence"]
                    })
                    
                    # Set entities
                    message.set(ENTITIES, data.get("entities", []))
                    
                else:
                    print(f"❌ External NLU Error: {response.status_code}")
                    message.set(INTENT, {"name": "nlu_fallback", "confidence": 0.1})
                    
            except Exception as e:
                print(f"❌ External NLU Exception: {e}")
                message.set(INTENT, {"name": "nlu_fallback", "confidence": 0.1})
        
        return messages