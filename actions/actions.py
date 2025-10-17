# Improved action.py with better error handling
import requests
import logging
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ActionAnswerFromQnA(Action):
    def name(self) -> Text:
        return "action_answer_from_qna"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            intent = tracker.latest_message.get("intent", {}).get("name")
            logger.info(f"Processing intent: {intent}")
            
            # Static QnA responses - same as before
            qna_responses = {
                "tanya_jalur_pendaftaran": """Jalur pendaftaran Pascasarjana ITS meliputi:
• Jalur Reguler dan Riset
• Jalur PJJ (Pendidikan Jarak Jauh)
• Jalur Kerjasama
• Jalur Beasiswa
Untuk informasi detail, silakan kunjungi website resmi Pascasarjana ITS.""",
                
                "tanya_syarat_pendaftaran": """Syarat umum pendaftaran Pascasarjana ITS:
• Ijazah S1 (untuk Magister) atau S2 (untuk Doktor) yang terakreditasi
• Transkrip nilai dengan IPK minimal 2.75
• Sertifikat TOEFL/IELTS (skor minimal bervariasi per prodi)
• Surat rekomendasi dari dosen atau atasan
• Proposal penelitian (untuk beberapa program)
• Dokumen lainnya sesuai program yang dipilih""",
                
                "cara_mendaftar": """Cara mendaftar Pascasarjana ITS:
1. Kunjungi website pendaftaran resmi ITS
2. Buat akun dan isi formulir online
3. Upload dokumen persyaratan
4. Bayar biaya pendaftaran
5. Ikuti tahap seleksi sesuai jadwal
6. Tunggu pengumuman hasil seleksi
Link: https://my.its.ac.id""",
                
                "tanya_beasiswa": """Beasiswa tersedia untuk Pascasarjana ITS:
• LPDP (Beasiswa Pendidikan Indonesia)
• Beasiswa Kementerian/BUMN
• Beasiswa dari industri partner
• Beasiswa internal ITS
• Teaching/Research Assistantship
Informasi lengkap dapat dilihat di website Pascasarjana ITS.""",

                "tanya_toefl": """Persyaratan TOEFL/IELTS untuk Pascasarjana ITS:
• TOEFL ITP: minimal skor 450
• TOEFL iBT: minimal skor 61
• IELTS: minimal skor 6.0
• Sertifikat bahasa Inggris harus masih berlaku (maksimal 2 tahun)
• Beberapa program memiliki persyaratan skor yang lebih tinggi""",

                "tanya_jadwal_pendaftaran": """Jadwal pendaftaran Pascasarjana ITS:
• Gelombang 1: Januari - Februari
• Gelombang 2: Mei - Juni  
• Gelombang 3: September - Oktober
Jadwal dapat berubah setiap tahun. Silakan cek website resmi untuk jadwal terkini.""",

                "tanya_jadwal_ujian": """Jadwal ujian masuk Pascasarjana ITS:
• Tes tertulis: 1-2 minggu setelah penutupan pendaftaran
• Wawancara: 1 minggu setelah tes tertulis
• Jadwal detail akan diinformasikan kepada peserta yang lolos administrasi""",

                "tanya_jadwal_pengumuman": """Jadwal pengumuman hasil seleksi:
• Hasil tes tertulis: 3-5 hari setelah ujian
• Hasil akhir: 1 minggu setelah wawancara
• Pengumuman melalui website resmi dan email pendaftar""",

                "tanya_biaya_pendaftaran": """Biaya pendaftaran Pascasarjana ITS:
• Jalur Reguler: Rp 300.000
• Jalur PJJ: Rp 250.000
• Jalur Beasiswa: Gratis
Pembayaran dapat dilakukan melalui bank yang telah ditentukan.""",

                "cara_pembayaran": """Cara pembayaran biaya pendaftaran:
• Bank BNI, BRI, Mandiri, atau BCA
• Virtual Account yang diberikan setelah registrasi online
• ATM, Internet Banking, atau Mobile Banking
• Simpan bukti pembayaran untuk upload ke sistem""",

                "tanya_double_degree": """Program Double Degree Pascasarjana ITS:
• Tersedia untuk beberapa program Magister dan Doktor
• Kerjasama dengan universitas luar negeri
• Durasi biasanya 2-3 tahun
• Syarat khusus: IPK minimal 3.25 dan TOEFL/IELTS tinggi
• Informasi detail dapat dilihat di website Pascasarjana ITS""",

                "tanya_ipk_minimum": """IPK minimum untuk Pascasarjana ITS:
• Program Magister: IPK minimal 2.75
• Program Doktor: IPK minimal 3.00
• Beberapa program memiliki persyaratan IPK yang lebih tinggi
• IPK dihitung dari transkrip nilai S1 (untuk Magister) atau S2 (untuk Doktor)""",

                "tanya_periode_pendaftaran": """Periode pendaftaran Pascasarjana ITS:
• Gelombang 1: Januari - Februari (mulai kuliah Semester Genap)
• Gelombang 2: Mei - Juni (mulai kuliah Semester Ganjil)
• Gelombang 3: September - Oktober (mulai kuliah Semester Genap)
Jadwal dapat berubah, silakan cek website resmi untuk informasi terkini.""",

                "tanya_seleksi": """Prosedur seleksi Pascasarjana ITS:
• Seleksi administrasi (kelengkapan dokumen)
• Tes tertulis (sesuai program studi)
• Wawancara dengan dosen program studi
• Tes bahasa Inggris (untuk beberapa program)
• Presentasi proposal (untuk program Doktor)""",

                "tanya_transfer": """Transfer mahasiswa Pascasarjana:
• ITS menerima mahasiswa transfer dari perguruan tinggi lain
• Syarat: akreditasi program asal minimal B
• Maksimal transfer 50% dari total SKS
• Harus lulus seleksi masuk ITS
• Pengakuan SKS ditentukan oleh program studi tujuan"""
            }
            
            answer = qna_responses.get(intent)
            if answer:
                logger.info(f"Found answer for intent: {intent}")
                dispatcher.utter_message(text=answer)
            else:
                logger.warning(f"No answer found for intent: {intent}")
                dispatcher.utter_message(text="Maaf, saya belum memiliki informasi untuk pertanyaan tersebut. Silakan hubungi admin Pascasarjana ITS untuk informasi lebih lanjut.")
            
        except Exception as e:
            logger.error(f"Error in ActionAnswerFromQnA: {e}")
            dispatcher.utter_message(text="Maaf, terjadi kesalahan teknis. Silakan coba lagi.")
        
        return []

# Simplified other actions to avoid Node.js dependency errors
class ActionQueryBiaya(Action):
    def name(self) -> Text:
        return "action_query_biaya"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Informasi biaya kuliah akan segera tersedia. Untuk sementara, silakan hubungi admin Pascasarjana ITS.")
        return []

class ActionListProdiByFakultas(Action):
    def name(self) -> Text:
        return "action_list_prodi_by_fakultas"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Daftar program studi akan segera tersedia. Untuk informasi lengkap, silakan kunjungi website resmi ITS.")
        return []

class ActionLookupFakultasByProdi(Action):
    def name(self) -> Text:
        return "action_lookup_fakultas_by_prodi"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Pencarian fakultas berdasarkan prodi akan segera tersedia.")
        return []

class ActionRouteAfterClarify(Action):
    def name(self) -> Text:
        return "action_route_after_clarify"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Silakan tanyakan hal lain yang ingin Anda ketahui tentang Pascasarjana ITS.")
        return []

class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        logger.info("Default fallback triggered")
        
        # Get the user's message
        user_message = tracker.latest_message.get('text', '')
        
        fallback_responses = [
            f"Maaf, saya belum memahami pertanyaan '{user_message}'. Silakan coba dengan kata-kata lain.",
            "Saya kurang mengerti maksud Anda. Bisa dijelaskan lebih spesifik?",
            "Mohon maaf, saya belum bisa membantu dengan pertanyaan tersebut. Silakan tanyakan tentang:\n• Biaya kuliah\n• Program studi\n• Syarat pendaftaran\n• Jadwal pendaftaran"
        ]
        
        # Use different response based on how many times fallback has been triggered
        fallback_count = len([event for event in tracker.events 
                            if event.get('name') == 'action_default_fallback'])
        
        if fallback_count < len(fallback_responses):
            response = fallback_responses[fallback_count]
        else:
            response = "Untuk bantuan lebih lanjut, silakan hubungi admin Pascasarjana ITS di website resmi."
        
        dispatcher.utter_message(text=response)
        return []