# actions.py
import requests
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
• Kuota terbatas, first come first served"""
        }
        
        answer = qna_responses.get(intent)
        if answer:
            dispatcher.utter_message(text=answer)
        else:
            dispatcher.utter_message(text="Maaf, saya belum memiliki informasi untuk pertanyaan tersebut. Silakan hubungi admin Pascasarjana ITS untuk informasi lebih lanjut.")
        
        return []


# ==============================
# 🔹 ACTION: QUERY BIAYA DARI ENDPOINT /biaya
# ==============================
class ActionQueryBiaya(Action):
    def name(self) -> Text:
        return "action_query_biaya"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        jenjang = tracker.get_slot("jenjang")
        prodi = tracker.get_slot("prodi")

        params = {}
        if jenjang:
            params["jenjang"] = jenjang
        if prodi:
            params["prodi"] = prodi

        try:
            res = requests.get("http://localhost:3000/biaya", params=params)
            if res.status_code == 200:
                data = res.json()
                if data:
                    msg = "Berikut informasi biaya yang ditemukan:\n"
                    for r in data:
                        msg += f"• {r['program']}: {r['biaya_label']} (SPI: {r['spi']}, IPITS: {r['ipits']})\n"
                else:
                    msg = "Data biaya belum tersedia untuk kriteria tersebut."
            else:
                msg = "Server tidak merespons permintaan data biaya."
        except Exception as e:
            msg = f"Gagal terhubung ke server Node.js: {e}"

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
        try:
            if fakultas:
                res = requests.get("http://localhost:3000/prodi", params={"fakultas": fakultas})
                if res.status_code == 200:
                    data = res.json()
                    if data:
                        prodi_list = ", ".join([p["prodi"] for p in data])
                        msg = f"Program studi di Fakultas {fakultas} meliputi: {prodi_list}."
                    else:
                        msg = f"Tidak ditemukan program studi untuk fakultas {fakultas}."
                else:
                    msg = "Server tidak merespons permintaan data prodi."
            else:
                msg = "Fakultas apa yang ingin Anda lihat program studinya?"
        except Exception as e:
            msg = f"Gagal menghubungi server Node.js: {e}"

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
        try:
            if prodi:
                res = requests.get("http://localhost:3000/fakultas", params={"prodi": prodi})
                if res.status_code == 200:
                    data = res.json()
                    if data:
                        msg = f"Program studi {prodi} berada di Fakultas {data['fakultas']}."
                    else:
                        msg = f"Saya tidak menemukan fakultas untuk program studi {prodi}."
                else:
                    msg = "Server tidak merespons permintaan data fakultas."
            else:
                msg = "Silakan sebutkan nama program studi yang ingin Anda cari."
        except Exception as e:
            msg = f"Gagal menghubungi server Node.js: {e}"

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
        if "biaya" in last_intent:
            return [ActionQueryBiaya().run(dispatcher, tracker, domain)]
        elif "prodi" in last_intent:
            return [ActionListProdiByFakultas().run(dispatcher, tracker, domain)]
        else:
            return [ActionAnswerFromQnA().run(dispatcher, tracker, domain)]
