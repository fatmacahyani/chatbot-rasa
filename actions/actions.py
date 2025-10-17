from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
import json

class ActionQueryProdi(Action):
    def name(self) -> Text:
        return "action_query_prodi"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        fakultas = tracker.get_slot("fakultas")
        
        try:
            # Query ke NLU service untuk data prodi
            if fakultas:
                response = requests.get(f"http://localhost:3000/api/prodi/{fakultas}")
            else:
                response = requests.get("http://localhost:3000/api/prodi")
            
            if response.status_code == 200:
                prodi_list = response.json()
                
                if prodi_list:
                    if fakultas:
                        message = f"Berikut program studi pascasarjana di fakultas {fakultas}:\n\n"
                    else:
                        message = "Berikut seluruh program studi pascasarjana di ITS:\n\n"
                    
                    current_fakultas = ""
                    for prodi in prodi_list:
                        if prodi['fakultas'] != current_fakultas:
                            current_fakultas = prodi['fakultas']
                            message += f"🏛️ **{current_fakultas}**\n"
                        
                        message += f"   • {prodi['prodi']}\n"
                    
                    message += "\nApakah ada yang ingin Anda tanyakan lebih lanjut tentang program studi tertentu?"
                else:
                    message = "Maaf, data program studi tidak ditemukan."
            else:
                message = "Maaf, terjadi kendala dalam mengambil data program studi."
                
        except Exception as e:
            print(f"Error in ActionQueryProdi: {e}")
            message = "Maaf, terjadi kesalahan sistem. Silakan coba lagi."
        
        dispatcher.utter_message(text=message)
        return []

class ActionQueryBiaya(Action):
    def name(self) -> Text:
        return "action_query_biaya"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        jenjang = tracker.get_slot("jenjang")
        program = tracker.get_slot("program")
        
        try:
            # Query ke NLU service untuk data biaya
            url = "http://localhost:3000/api/biaya"
            if jenjang or program:
                url += f"/{jenjang or 'undefined'}/{program or 'undefined'}"
            
            response = requests.get(url)
            
            if response.status_code == 200:
                biaya_list = response.json()
                
                if biaya_list:
                    message = "💰 **Informasi Biaya Pascasarjana ITS:**\n\n"
                    
                    for biaya in biaya_list:
                        message += f"🎓 **{biaya['jenjang']} - {biaya['program']}**\n"
                        message += f"   📋 Kategori: {biaya['kategori']}\n"
                        message += f"   💵 {biaya['biaya_label']}\n"
                        
                        # Format biaya per semester
                        biaya_formatted = f"Rp {int(biaya['biaya_per_semester']):,}".replace(',', '.')
                        message += f"   💰 Biaya per semester: {biaya_formatted}\n"
                        
                        # Tambahkan info SPI dan IPITS jika ada
                        if biaya.get('spi') and biaya['spi'] != 'Tidak Ada':
                            message += f"   📊 SPI: {biaya['spi']}\n"
                        if biaya.get('ipits') and biaya['ipits'] != 'Tidak Ada':
                            message += f"   🏛️ IPITS: {biaya['ipits']}\n"
                        
                        message += "\n"
                    
                    message += "ℹ️ Untuk informasi lebih detail, silakan hubungi bagian administrasi pascasarjana ITS."
                else:
                    message = "Maaf, data biaya untuk kriteria tersebut tidak ditemukan. Silakan coba dengan kriteria lain."
            else:
                message = "Maaf, terjadi kendala dalam mengambil data biaya."
                
        except Exception as e:
            print(f"Error in ActionQueryBiaya: {e}")
            message = "Maaf, terjadi kesalahan sistem. Silakan coba lagi."
        
        dispatcher.utter_message(text=message)
        return []

class ActionAnswerFromQna(Action):
    def name(self) -> Text:
        return "action_answer_from_qna"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        intent_name = tracker.latest_message['intent']['name']
        
        try:
            # Query ke database t_qna berdasarkan intent
            response = requests.get(f"http://localhost:3000/api/qna/{intent_name}")
            
            if response.status_code == 200:
                qna_list = response.json()
                
                if qna_list:
                    # Ambil jawaban pertama jika ada multiple
                    answer = qna_list[0]['answer']
                    dispatcher.utter_message(text=answer)
                else:
                    dispatcher.utter_message(text="Maaf, informasi tersebut belum tersedia. Silakan hubungi admin pascasarjana ITS.")
            else:
                dispatcher.utter_message(text="Maaf, terjadi kendala dalam mengambil informasi.")
                
        except Exception as e:
            print(f"Error in ActionAnswerFromQna: {e}")
            dispatcher.utter_message(text="Maaf, terjadi kesalahan sistem. Silakan coba lagi.")
        
        return []