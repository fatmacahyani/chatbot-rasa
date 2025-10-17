# actions.py
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


# ==============================
# 🔹 ACTION: JAWAB DARI QnA STATIS
# ==============================
class ActionAnswerFromQnA(Action):
    def name(self) -> Text:
        return "action_answer_from_qna"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        intent = tracker.latest_message.get("intent", {}).get("name")
        
        # Static QnA responses
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
            
            "tanya_jadwal_pendaftaran": """Jadwal pendaftaran Pascasarjana ITS:
• Semester Genap: Biasanya Oktober - Desember
• Semester Ganjil: Biasanya April - Juni
Jadwal pasti akan diumumkan di website resmi ITS.
Pastikan selalu cek update terbaru!""",
            
            "tanya_jadwal_ujian": """Jadwal ujian masuk Pascasarjana ITS:
• Ujian tulis: 2-3 minggu setelah penutupan pendaftaran
• Ujian wawancara: 1 minggu setelah ujian tulis
• Jadwal detail akan diinformasikan via email ke pendaftar""",
            
            "tanya_jadwal_pengumuman": """Pengumuman hasil seleksi:
• Hasil ujian tulis: 1 minggu setelah ujian
• Hasil akhir: 2-3 minggu setelah wawancara
• Pengumuman dipublikasi di website dan email pribadi""",
            
            "tanya_masa_studi": """Masa studi Pascasarjana ITS:
• Program Magister (S2): 2-4 tahun
• Program Doktor (S3): 3-7 tahun
Masa studi tergantung pada program dan kemampuan menyelesaikan penelitian.""",
            
            "tanya_cuti": """Kebijakan cuti kuliah:
• Mahasiswa dapat mengajukan cuti maksimal 2 semester berturut-turut
• Cuti tidak menambah masa studi maksimal
• Harus mengajukan permohonan ke fakultas dengan alasan yang jelas
• Tetap dikenakan biaya administrasi selama cuti""",
            
            "tanya_kegiatan_mahasiswa": """Kegiatan mahasiswa Pascasarjana:
• Seminar nasional dan internasional
• Publikasi jurnal ilmiah
• Kegiatan riset bersama dosen
• Organisasi mahasiswa pascasarjana
• Workshop dan pelatihan akademik""",
            
            "tanya_asrama": """Fasilitas asrama:
• Tersedia asrama untuk mahasiswa pascasarjana
• Lokasi di dalam kampus ITS
• Fasilitas lengkap: kamar, Wi-Fi, kantin
• Pendaftaran terpisah dari pendaftaran kuliah
• Kuota terbatas, first come first served""",
            
            "tanya_toefl": """Persyaratan TOEFL/IELTS:
• TOEFL ITP: minimal skor 450
• TOEFL IBT: minimal skor 45
• IELTS: minimal band 5.0
• Berlaku maksimal 2 tahun dari tanggal tes
• Beberapa program studi mungkin memiliki skor minimal yang berbeda""",
            
            "tanya_seleksi": """Proses seleksi Pascasarjana ITS:
• Seleksi administrasi (kelengkapan dokumen)
• Tes tertulis (sesuai program studi)
• Tes wawancara
• Tes kemampuan bahasa Inggris
• Presentasi proposal penelitian (untuk beberapa program)
Total proses seleksi sekitar 2-4 minggu""",
            
            "tanya_ipk_minimum": """IPK minimal pendaftaran:
• Program Magister: IPK minimal 2.75
• Program Doktor: IPK minimal 3.00
• Untuk program studi tertentu mungkin ada persyaratan IPK yang lebih tinggi
• IPK dihitung dari transkrip nilai yang dilegalisir""",
            
            "tanya_biaya_pendaftaran": """Biaya pendaftaran:
• Biaya pendaftaran: Rp 300.000
• Pembayaran melalui bank yang ditunjuk
• Biaya tidak dapat dikembalikan
• Bukti pembayaran harus diupload saat pendaftaran online""",
            
            "cara_pembayaran": """Metode pembayaran:
• Transfer bank ke rekening yang ditentukan
• Virtual account melalui ATM/mobile banking
• Pembayaran di teller bank
• E-wallet (untuk beberapa layanan)
Detail rekening akan diberikan setelah registrasi online""",
            
            "tanya_periode_pendaftaran": """Periode pendaftaran:
• Gelombang 1: Februari - Maret
• Gelombang 2: Mei - Juni  
• Gelombang 3: September - Oktober
Tanggal pasti akan diumumkan di website resmi ITS setiap tahunnya""",
            
            "tanya_double_degree": """Program Double Degree:
• Tersedia untuk beberapa program studi
• Kerjasama dengan universitas luar negeri
• Durasi studi 2-3 tahun
• Mendapat gelar dari kedua universitas
• Persyaratan khusus: TOEFL/IELTS tinggi, IPK minimal 3.25""",
            
            "tanya_transfer": """Transfer mahasiswa:
• Menerima mahasiswa transfer dari universitas lain
• Maksimal transfer 50% SKS
• IPK minimal 3.00
• Mata kuliah yang diakui sesuai kurikulum ITS
• Proses evaluasi transkrip oleh program studi"""
        }
        
        answer = qna_responses.get(intent)
        if answer:
            dispatcher.utter_message(text=answer)
        else:
            dispatcher.utter_message(text="Maaf, saya belum memiliki informasi untuk pertanyaan tersebut. Silakan hubungi admin Pascasarjana ITS untuk informasi lebih lanjut.")
        
        return []


# ==============================
# 🔹 ACTION: QUERY BIAYA DARI STATIC DATA
# ==============================
class ActionQueryBiaya(Action):
    def name(self) -> Text:
        return "action_query_biaya"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        jenjang = tracker.get_slot("jenjang")
        prodi = tracker.get_slot("prodi")

        # Simplified static response for biaya queries
        if jenjang and prodi:
            msg = f"Informasi biaya untuk {jenjang} {prodi}:\n"
            msg += "• Jalur Reguler: UKT Rp 12.500.000 per semester\n"
            msg += "• Jalur PJJ: UKT Rp 10.000.000 per semester\n"
            msg += "• SPI: Rp 25.000.000 (sekali bayar)\n"
            msg += "• IPITS: Rp 5.000.000 (sekali bayar)\n"
            msg += "\nUntuk informasi terkini, silakan kunjungi website resmi Pascasarjana ITS."
        elif jenjang:
            msg = f"Biaya kuliah {jenjang} bervariasi tergantung program studi. Silakan sebutkan program studi yang diminati."
        elif prodi:
            msg = f"Biaya kuliah {prodi} bervariasi tergantung jenjang (Magister/Doktor). Silakan pilih jenjang yang diminati."
        else:
            msg = "Silakan sebutkan jenjang (Magister/Doktor) dan program studi untuk informasi biaya yang lebih spesifik."

        dispatcher.utter_message(text=msg)
        return []


# ==============================
# 🔹 ACTION: LIST PRODI BERDASARKAN FAKULTAS
# ==============================
class ActionListProdiByFakultas(Action):
    def name(self) -> Text:
        return "action_list_prodi_by_fakultas"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        fakultas = tracker.get_slot("fakultas")
        
        # Static data for program studi
        fakultas_prodi = {
            "ELECTICS": "Teknik Informatika, Teknik Elektro, Sistem Informasi, Teknik Komputer",
            "Teknologi Elektro dan Informatika Cerdas": "Teknik Informatika, Teknik Elektro, Sistem Informasi",
            "Teknologi Industri dan Rekayasa Sistem": "Teknik Kimia, Teknik Fisika, Teknik Industri, Manajemen Teknologi",
            "Teknologi Kelautan": "Teknik Sipil, Arsitektur, Teknik Lingkungan",
            "Sains dan Analitika Data": "Statistika, Matematika, Fisika"
        }
        
        if fakultas:
            prodi_list = fakultas_prodi.get(fakultas, "")
            if prodi_list:
                msg = f"Program studi di Fakultas {fakultas} meliputi: {prodi_list}."
            else:
                msg = f"Maaf, data program studi untuk fakultas {fakultas} belum tersedia."
        else:
            msg = "Silakan sebutkan nama fakultas yang ingin Anda ketahui program studinya.\n"
            msg += "Fakultas yang tersedia: ELECTICS, Teknologi Industri dan Rekayasa Sistem, Teknologi Kelautan, Sains dan Analitika Data."

        dispatcher.utter_message(text=msg)
        return []


# ==============================
# 🔹 ACTION: CARI FAKULTAS DARI NAMA PRODI
# ==============================
class ActionLookupFakultasByProdi(Action):
    def name(self) -> Text:
        return "action_lookup_fakultas_by_prodi"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        prodi = tracker.get_slot("prodi")
        
        # Static data mapping prodi to fakultas
        prodi_fakultas = {
            "Teknik Informatika": "Teknologi Elektro dan Informatika Cerdas (ELECTICS)",
            "Teknik Elektro": "Teknologi Elektro dan Informatika Cerdas (ELECTICS)",
            "Sistem Informasi": "Teknologi Elektro dan Informatika Cerdas (ELECTICS)",
            "Teknik Komputer": "Teknologi Elektro dan Informatika Cerdas (ELECTICS)",
            "Teknik Kimia": "Teknologi Industri dan Rekayasa Sistem",
            "Teknik Fisika": "Teknologi Industri dan Rekayasa Sistem",
            "Teknik Industri": "Teknologi Industri dan Rekayasa Sistem",
            "Manajemen Teknologi": "Teknologi Industri dan Rekayasa Sistem",
            "Teknik Sipil": "Teknologi Kelautan",
            "Arsitektur": "Teknologi Kelautan",
            "Teknik Lingkungan": "Teknologi Kelautan",
            "Statistika": "Sains dan Analitika Data",
            "Matematika": "Sains dan Analitika Data",
            "Fisika": "Sains dan Analitika Data"
        }
        
        if prodi:
            fakultas = prodi_fakultas.get(prodi)
            if fakultas:
                msg = f"Program studi {prodi} berada di Fakultas {fakultas}."
            else:
                msg = f"Maaf, saya belum memiliki data fakultas untuk program studi {prodi}."
        else:
            msg = "Silakan sebutkan nama program studi yang ingin Anda cari fakultasnya."

        dispatcher.utter_message(text=msg)
        return []


# ==============================
# 🔹 ACTION: ROUTE SETELAH FALLBACK / CLARIFY
# ==============================
class ActionRouteAfterClarify(Action):
    def name(self) -> Text:
        return "action_route_after_clarify"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        last_intent = tracker.get_intent_of_latest_message(skip_fallback_intent=False)
        if "biaya" in str(last_intent):
            return [ActionQueryBiaya().run(dispatcher, tracker, domain)]
        elif "prodi" in str(last_intent):
            return [ActionListProdiByFakultas().run(dispatcher, tracker, domain)]
        else:
            return [ActionAnswerFromQnA().run(dispatcher, tracker, domain)]


# ==============================
# 🔹 ACTION: DEFAULT FALLBACK
# ==============================
class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Maaf, saya belum memahami pertanyaan Anda. Silakan coba tanyakan dengan cara lain atau pilih dari topik berikut:")
        dispatcher.utter_message(text="Contoh yang bisa Anda tanyakan:\n• Berapa biaya Magister Manajemen Teknologi?\n• Apa saja prodi di Fakultas ELECTICS?\n• Bagaimana cara mendaftar?\n• Kapan jadwal ujian masuk?")
        return []