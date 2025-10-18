from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted
import requests

# Base URL untuk NLU service
NLU_SERVICE_URL = "http://localhost:3000"

class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(
            text="🤔 Maaf, saya belum memahami pertanyaan Anda.\n\n"
        )
        
        return [UserUtteranceReverted()]

# ========================================
# EXTERNAL NLU ACTIONS (Dynamic Data)
# ========================================

class ActionQueryProdi(Action):
    def name(self) -> Text:
        return "action_query_prodi"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        print("Masuk ke ActionQueryProdi")  # Debug log
        fakultas = tracker.get_slot("fakultas")
        
        try:
            # Query ke NLU service
            if fakultas:
                response = requests.get(f"{NLU_SERVICE_URL}/api/prodi/{fakultas}", timeout=10)
            else:
                response = requests.get(f"{NLU_SERVICE_URL}/api/prodi", timeout=10)
            
            if response.status_code == 200:
                prodi_list = response.json()
                
                if prodi_list:
                    if fakultas:
                        msg = f"🏛️ **Program Studi di {fakultas}:**\n\n"
                    else:
                        msg = "🎓 **Seluruh Program Studi Pascasarjana ITS:**\n\n"
                    
                    # Group by fakultas
                    current_fakultas = ""
                    count = 0
                    for prodi in prodi_list:
                        if prodi['fakultas'] != current_fakultas:
                            current_fakultas = prodi['fakultas']
                            msg += f"**📚 {current_fakultas}**\n"
                        
                        count += 1
                        msg += f"   {count}. {prodi['prodi']}\n"
                    
                    msg += f"\n📊 **Total: {len(prodi_list)} program studi**\n\n"
                    msg += "💡 **Ingin tahu lebih detail?**\n"
                    msg += "• Tanyakan biaya: *\"Berapa biaya kuliah [nama prodi]?\"*\n"
                    msg += "• Tanyakan syarat: *\"Apa syarat pendaftaran?\"*"
                    
                    dispatcher.utter_message(text=msg)
                else:
                    dispatcher.utter_message(text="❌ Data program studi tidak ditemukan.")
            else:
                dispatcher.utter_message(text="⚠️ Gagal mengambil data program studi.")
                
        except Exception as e:
            print(f"❌ Error in ActionQueryProdi: {e}")
            dispatcher.utter_message(text="⚠️ Layanan sedang tidak tersedia.")
        
        return []

class ActionQueryBiaya(Action):
    def name(self) -> Text:
        return "action_query_biaya"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        print("Masuk ke ActionQueryBiaya")  # Debug log
        jenjang = tracker.get_slot("jenjang")
        program = tracker.get_slot("program")
        
        try:
            # Query ke NLU service
            url = f"{NLU_SERVICE_URL}/api/biaya"
            if jenjang or program:
                url += f"/{jenjang or 'undefined'}/{program or 'undefined'}"
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                biaya_list = response.json()
                
                if biaya_list:
                    msg = "💰 **Informasi Biaya Pascasarjana ITS:**\n\n"
                    
                    for i, biaya in enumerate(biaya_list, 1):
                        msg += f"**{i}. {biaya['jenjang']} - {biaya['program']}**\n"
                        msg += f"   📋 Kategori: {biaya['kategori']}\n"
                        
                        # Format biaya per semester
                        try:
                            biaya_formatted = f"Rp {int(float(biaya['biaya_per_semester'])):,}".replace(',', '.')
                            msg += f"   💵 Biaya per semester: {biaya_formatted}\n"
                        except:
                            msg += f"   💵 {biaya['biaya_label']}\n"
                        
                        # Info tambahan
                        if biaya.get('spi') and str(biaya['spi']) != 'Tidak Ada':
                            msg += f"   📊 SPI: {biaya['spi']}\n"
                        if biaya.get('ipits') and str(biaya['ipits']) != 'Tidak Ada':
                            msg += f"   🏛️ IPITS: {biaya['ipits']}\n"
                        
                        msg += "\n"
                    
                    msg += "📞 **Kontak:** pascasarjana@its.ac.id"
                    dispatcher.utter_message(text=msg)
                else:
                    dispatcher.utter_message(text="❌ Data biaya tidak ditemukan.")
            else:
                dispatcher.utter_message(text="⚠️ Gagal mengambil data biaya.")
                
        except Exception as e:
            print(f"❌ Error in ActionQueryBiaya: {e}")
            dispatcher.utter_message(text="⚠️ Layanan sedang tidak tersedia.")
        
        return []

# ========================================
# STATIC QnA ACTIONS (Ground Truth Data)
# ========================================

class ActionAnswerQnaStatic(Action):
    def name(self) -> Text:
        return "action_answer_qna_static"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        intent_name = tracker.latest_message['intent']['name']
        print(f"Masuk ke ActionAnswerQnaStatic: {intent_name}")  # Debug log
        
        # Static responses berdasarkan ground truth
        static_responses = {
            "tanya_jalur_pendaftaran": "🎓 **Jalur Pendaftaran Pascasarjana ITS:**\n\nJalur pendaftaran meliputi Reguler, Kerjasama, dan Beasiswa.\n\n📋 **Detail lengkap:** https://pascasarjana.its.ac.id\n📞 **Info:** pascasarjana@its.ac.id",
            
            "tanya_periode_pendaftaran": "📅 **Periode Pendaftaran:**\n\nJadwal pendaftaran terdiri dari beberapa gelombang. Detailnya dapat dilihat di laman resmi ITS.\n\n🌐 **Website:** https://pascasarjana.its.ac.id\n📞 **Kontak:** pascasarjana@its.ac.id",
            
            "tanya_syarat_pendaftaran": "📋 **Syarat Umum Pendaftaran:**\n\nSyarat umum antara lain ijazah S1/S2 sesuai jenjang yang didaftar, transkrip nilai, dan dokumen administrasi lain.\n\n📝 **Detail lengkap:** https://admission.its.ac.id\n📞 **Info:** pascasarjana@its.ac.id",
            
            "cara_mendaftar": "📝 **Cara Mendaftar Pascasarjana ITS:**\n\nPendaftaran dilakukan secara online melalui website https://admission.its.ac.id\n\n✅ **Langkah-langkah:**\n1. Buat akun di portal pendaftaran\n2. Lengkapi data dan upload dokumen\n3. Pilih program studi\n4. Bayar biaya pendaftaran\n5. Submit aplikasi\n\n📞 **Bantuan:** pascasarjana@its.ac.id",
            
            "tanya_biaya_pendaftaran": "💰 **Biaya Pendaftaran:**\n\nYa, terdapat biaya pendaftaran yang dibayarkan melalui virtual account bank atau sesuai instruksi di portal pendaftaran.\n\n💳 **Pembayaran:** Virtual account bank\n📞 **Info:** pascasarjana@its.ac.id",
            
            "tanya_beasiswa": "🏆 **Beasiswa Pascasarjana ITS:**\n\nITS menyediakan beberapa skema beasiswa seperti Beasiswa ITS, LPDP, dan beasiswa kerjasama lainnya.\n\n📋 **Jenis Beasiswa:**\n• Beasiswa ITS\n• LPDP\n• Beasiswa Kerjasama\n• Bantuan Penelitian\n\n📞 **Info:** pascasarjana@its.ac.id",
            
            "tanya_prosedur_seleksi": "🎯 **Prosedur Seleksi:**\n\nSeleksi meliputi seleksi administrasi, tes tertulis, dan/atau wawancara.\n\n📋 **Tahapan:**\n1. Seleksi Administrasi\n2. Tes Tertulis (jika ada)\n3. Wawancara\n\n📞 **Info:** pascasarjana@its.ac.id",
            
            "dokumen_diunggah": "📄 **Dokumen yang Perlu Diunggah:**\n\nDokumen utama meliputi ijazah, transkrip, KTP, pas foto, surat rekomendasi, dan proposal riset (untuk S3).\n\n📋 **List Dokumen:**\n• Ijazah & Transkrip\n• KTP & Pas Foto\n• Surat Rekomendasi\n• Proposal Riset (S3)\n\n📞 **Info:** pascasarjana@its.ac.id",
            
            "batas_usia": "🎂 **Batas Usia:**\n\nTidak ada batasan usia untuk mendaftar program Pascasarjana di ITS.\n\n✅ **Terbuka untuk semua usia**\n📞 **Info:** pascasarjana@its.ac.id",
            
            "cara_pembayaran_pendaftaran": "💳 **Cara Pembayaran:**\n\nPembayaran dilakukan melalui virtual account bank sesuai instruksi di portal pendaftaran.\n\n💰 **Metode:**\n• Virtual Account Bank\n• Sesuai petunjuk di portal\n\n📞 **Bantuan:** pascasarjana@its.ac.id",
            
            "daftar_multi_prodi": "📚 **Mendaftar Lebih dari Satu Program:**\n\nYa, calon mahasiswa dapat memilih lebih dari satu program studi dengan ketentuan biaya pendaftaran berlaku per pilihan.\n\n✅ **Diperbolehkan**\n💰 **Biaya per pilihan program**\n📞 **Info:** pascasarjana@its.ac.id",
            
            "ipk_minimum": "📊 **IPK Minimal:**\n\nIPK minimal biasanya 2,75 untuk S2, dan 3,00 untuk S3, namun ketentuan dapat berbeda di tiap program studi.\n\n📋 **Ketentuan Umum:**\n• S2: IPK ≥ 2,75\n• S3: IPK ≥ 3,00\n• *Dapat berbeda per prodi\n\n📞 **Info:** pascasarjana@its.ac.id",
            
            "jadwal_pendaftaran_2025": "📅 **Jadwal Pendaftaran 2025:**\n\nPendaftaran dibuka mulai 06 Oktober - 29 Desember 2025\n\n🗓️ **Periode:** 06 Oktober - 29 Desember 2025\n📞 **Info:** pascasarjana@its.ac.id",
            
            "jadwal_ujian_2025": "📝 **Jadwal Ujian 2025/2026:**\n\nUjian masuk dilaksanakan pada 05 - 09 Januari 2026\n\n🗓️ **Ujian:** 05 - 09 Januari 2026\n📞 **Info:** pascasarjana@its.ac.id",
            
            "jadwal_pengumuman_2025": "📢 **Pengumuman Hasil 2025:**\n\nHasil ujian diumumkan pada 12 Januari 2026 pukul 21.00 WIB\n\n🗓️ **Pengumuman:** 12 Januari 2026, 21:00 WIB\n📞 **Info:** pascasarjana@its.ac.id"
        }
        
        # Get response dari static data
        response_text = static_responses.get(intent_name)
        
        if response_text:
            dispatcher.utter_message(text=response_text)
        else:
            # Fallback ke database jika tidak ada static response
            try:
                response = requests.get(f"{NLU_SERVICE_URL}/api/qna/{intent_name}", timeout=5)
                if response.status_code == 200:
                    qna_list = response.json()
                    if qna_list:
                        answer = qna_list[0]['answer']
                        dispatcher.utter_message(text=f"📋 {answer}\n\n📞 **Kontak:** pascasarjana@its.ac.id")
                    else:
                        dispatcher.utter_message(text="❌ Informasi tidak ditemukan.\n📞 **Hubungi:** pascasarjana@its.ac.id")
                else:
                    dispatcher.utter_message(text="⚠️ Layanan informasi tidak tersedia.")
            except:
                dispatcher.utter_message(text="❌ Informasi tidak tersedia saat ini.\n📞 **Hubungi:** pascasarjana@its.ac.id")
        
        return []