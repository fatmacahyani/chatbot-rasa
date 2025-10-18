from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

API_BASE_URL = "http://localhost:3000"

class ActionQueryProdi(Action):
    def name(self) -> Text:
        return "action_query_prodi"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        print("Masuk ke ActionQueryProdi")
        
        try:
            # Simple database query (seperti project transkrip)
            response = requests.get(f"{API_BASE_URL}/api/prodi", timeout=10)
            
            if response.status_code == 200:
                prodi_list = response.json()
                
                if prodi_list:
                    msg = "🎓 **Program Studi Pascasarjana ITS:**\n\n"
                    
                    current_fakultas = ""
                    count = 0
                    
                    for prodi in prodi_list:
                        if prodi['fakultas'] != current_fakultas:
                            current_fakultas = prodi['fakultas']
                            msg += f"**📚 {current_fakultas}**\n"
                        
                        count += 1
                        msg += f"   {count}. {prodi['prodi']}\n"
                    
                    msg += f"\n📊 **Total: {len(prodi_list)} program studi**"
                    dispatcher.utter_message(text=msg)
                else:
                    dispatcher.utter_message(text="❌ Data program studi tidak ditemukan.")
            else:
                dispatcher.utter_message(text="⚠️ Gagal mengambil data program studi.")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            dispatcher.utter_message(text="⚠️ Layanan sedang tidak tersedia.")
        
        return []

class ActionQueryBiaya(Action):
    def name(self) -> Text:
        return "action_query_biaya"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        print("Masuk ke ActionQueryBiaya")
        
        try:
            # Simple database query
            response = requests.get(f"{API_BASE_URL}/api/biaya", timeout=10)
            
            if response.status_code == 200:
                biaya_list = response.json()
                
                if biaya_list:
                    msg = "💰 **Informasi Biaya Pascasarjana ITS:**\n\n"
                    
                    # Show first 8 results
                    for i, biaya in enumerate(biaya_list[:8], 1):
                        msg += f"**{i}. {biaya['jenjang']} - {biaya['program']}**\n"
                        msg += f"   📋 {biaya['kategori']}\n"
                        
                        try:
                            biaya_num = f"Rp {int(float(biaya['biaya_per_semester'])):,}".replace(',', '.')
                            msg += f"   💵 {biaya_num}/semester\n\n"
                        except:
                            msg += f"   💵 {biaya.get('biaya_label', 'Info tersedia')}\n\n"
                    
                    if len(biaya_list) > 8:
                        msg += f"... dan {len(biaya_list) - 8} program lainnya\n\n"
                    
                    msg += "📞 **Info:** pascasarjana@its.ac.id"
                    dispatcher.utter_message(text=msg)
                else:
                    dispatcher.utter_message(text="❌ Data biaya tidak ditemukan.")
            else:
                dispatcher.utter_message(text="⚠️ Gagal mengambil data biaya.")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            dispatcher.utter_message(text="⚠️ Layanan sedang tidak tersedia.")
        
        return []

class ActionAnswerQnaStatic(Action):
    def name(self) -> Text:
        return "action_answer_qna_static"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        intent_name = tracker.latest_message['intent']['name']
        print(f"QnA Static: {intent_name}")
        
        # Simple static responses
        responses = {
            "tanya_jalur_pendaftaran": "🎓 **Jalur Pendaftaran:** Reguler, Kerjasama, dan Beasiswa.\n\n📞 **Info:** pascasarjana@its.ac.id",
            "cara_mendaftar": "📝 **Cara Mendaftar:** Online di https://admission.its.ac.id\n\n📞 **Bantuan:** pascasarjana@its.ac.id",
            "tanya_beasiswa": "🏆 **Beasiswa:** ITS, LPDP, dan Kerjasama tersedia.\n\n📞 **Info:** pascasarjana@its.ac.id",
            "jadwal_pendaftaran_2025": "📅 **Pendaftaran 2025:** 06 Oktober - 29 Desember 2025\n\n📞 **Info:** pascasarjana@its.ac.id"
        }
        
        response_text = responses.get(intent_name)
        
        if response_text:
            dispatcher.utter_message(text=response_text)
        else:
            dispatcher.utter_message(text="📋 Informasi tersedia di website resmi.\n📞 **Kontak:** pascasarjana@its.ac.id")
        
        return []

class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(
            text="🤔 Maaf, saya belum memahami.\n\n"
                 "**Coba tanyakan:**\n"
                 "• Apa saja prodi pascasarjana di ITS?\n"
                 "• Berapa biaya kuliah?\n"
                 "• Bagaimana cara mendaftar?\n\n"
                 "📞 **Bantuan:** pascasarjana@its.ac.id"
        )
        
        return []