import torch
import pandas as pd
import numpy as np
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from transformers import BertTokenizer, BertForSequenceClassification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt

# ==============================
# Model dan Parameter
# ==============================
bertModel = 'distilbert-base-uncased'  # ringan tapi akurat
n_epochs = 8
batch_size = 16
lr = 2e-5

# ==============================
# Dataset Intent
# ==============================
data = {
    "text": [
        # ===== GREETING =====
        "halo", "selamat pagi", "hai", "permisi", "hello", "assalamualaikum",

        # ===== GOODBYE =====
        "terima kasih", "sampai jumpa", "dadah", "bye", "selamat tinggal", "ok makasih ya",

        # ===== TANYA JALUR PENDAFTARAN =====
        "apa saja jalur pendaftaran pascasarjana di ITS",
        "jalur masuk S2 apa saja",
        "ada jalur beasiswa atau reguler",
        "jalur apa yang tersedia untuk Pascasarjana ITS",

        # ===== TANYA PRODI =====
        "program studi apa saja di Pascasarjana ITS",
        "ada prodi apa di S2 ITS",
        "jurusan apa yang dibuka untuk Pascasarjana",
        "tolong tampilkan semua program studi magister dan doktor",

        # ===== TANYA BIAYA =====
        "berapa biaya kuliah magister manajemen teknologi",
        "berapa UKT program doktor teknik sipil",
        "tolong tampilkan biaya S2 ITS",
        "berapa biaya per semester Pascasarjana",

        # ===== TANYA SYARAT =====
        "apa saja syarat pendaftaran S2 ITS",
        "dokumen apa yang harus diunggah",
        "apa persyaratan pendaftaran Pascasarjana",
        "apa saja berkas untuk daftar doktor ITS",

        # ===== TANYA CARA PENDAFTARAN =====
        "bagaimana cara mendaftar Pascasarjana ITS",
        "link pendaftarannya apa",
        "bagaimana prosedur registrasi online",
        "dimana saya bisa daftar S2 ITS",

        # ===== TANYA BEASISWA =====
        "apakah ada beasiswa untuk S2 ITS",
        "beasiswa apa saja yang tersedia di Pascasarjana",
        "apakah ada LPDP di ITS",
        "bisa dapat beasiswa kerjasama tidak",

        # ===== TANYA JADWAL =====
        "kapan jadwal pendaftaran Pascasarjana semester genap",
        "kapan ujian masuk S2 ITS",
        "kapan hasil seleksi diumumkan",
        "kapan daftar ulang dan pembayaran UKT",

        # ===== TANYA ASRAMA =====
        "apakah ada asrama untuk mahasiswa Pascasarjana",
        "bisa tinggal di asrama ITS tidak",

        # ===== TANYA MASA STUDI =====
        "berapa lama masa studi magister",
        "lama kuliah doktor ITS berapa tahun",

        # ===== TANYA CUTI =====
        "apakah bisa cuti studi di Pascasarjana",
        "berapa lama maksimal cuti kuliah",

        # ===== TANYA KEGIATAN MAHASISWA =====
        "apakah mahasiswa Pascasarjana bisa ikut kegiatan kampus",
        "ada organisasi mahasiswa S2 ITS tidak",

        # ===== BOT CHALLENGE =====
        "apakah kamu bot", "siapa kamu", "apakah saya bicara dengan manusia",
    ],

    "label": [
        # 1. GREETING
        "greet","greet","greet","greet","greet","greet",

        # 2. GOODBYE
        "goodbye","goodbye","goodbye","goodbye","goodbye","goodbye",

        # 3. TANYA JALUR PENDAFTARAN
        "tanya_jalur_pendaftaran","tanya_jalur_pendaftaran","tanya_jalur_pendaftaran","tanya_jalur_pendaftaran",

        # 4. TANYA PRODI
        "tanya_prodi_tersedia","tanya_prodi_tersedia","tanya_prodi_tersedia","tanya_prodi_tersedia",

        # 5. TANYA BIAYA
        "tanya_biaya_kuliah","tanya_biaya_kuliah","tanya_biaya_kuliah","tanya_biaya_kuliah",

        # 6. TANYA SYARAT
        "tanya_syarat_pendaftaran","tanya_syarat_pendaftaran","tanya_syarat_pendaftaran","tanya_syarat_pendaftaran",

        # 7. TANYA CARA PENDAFTARAN
        "cara_mendaftar","cara_mendaftar","cara_mendaftar","cara_mendaftar",

        # 8. TANYA BEASISWA
        "tanya_beasiswa","tanya_beasiswa","tanya_beasiswa","tanya_beasiswa",

        # 9. TANYA JADWAL
        "tanya_jadwal_pendaftaran","tanya_jadwal_ujian","tanya_jadwal_pengumuman","tanya_jadwal_pendaftaran",

        # 10. TANYA ASRAMA
        "tanya_asrama","tanya_asrama",

        # 11. TANYA MASA STUDI
        "tanya_masa_studi","tanya_masa_studi",

        # 12. TANYA CUTI
        "tanya_cuti","tanya_cuti",

        # 13. TANYA KEGIATAN MAHASISWA
        "tanya_kegiatan_mahasiswa","tanya_kegiatan_mahasiswa",

        # 14. BOT CHALLENGE
        "bot_challenge","bot_challenge","bot_challenge"
    ]
}

df = pd.DataFrame(data)
texts = list(df["text"])
labels = df["label"].values

# Encode label ke angka
label_encoder = LabelEncoder()
encoded_labels = label_encoder.fit_transform(labels)
num_class = len(label_encoder.classes_)
print(f"Total intents: {num_class}")

# ==============================
# Split train-test
# ==============================
X_train, X_test, y_train, y_test = train_test_split(
    texts, encoded_labels, test_size=0.2, random_state=42
)

# ==============================
# Tokenizer dan Dataset
# ==============================
tokenizer = BertTokenizer.from_pretrained(bertModel)

class PascaDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_len=128):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]
        encoding = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            truncation=True,
            max_length=self.max_len,
            return_token_type_ids=False,
            padding='max_length',
            return_attention_mask=True,
            return_tensors='pt'
        )
        return {
            "input_ids": encoding["input_ids"].flatten(),
            "attention_mask": encoding["attention_mask"].flatten(),
            "label": torch.tensor(label, dtype=torch.long)
        }

train_dataset = PascaDataset(X_train, y_train, tokenizer)
test_dataset = PascaDataset(X_test, y_test, tokenizer)
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=batch_size)

# ==============================
# Setup Model & Training
# ==============================
model = BertForSequenceClassification.from_pretrained(bertModel, num_labels=num_class)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

optimizer = torch.optim.Adam(model.parameters(), lr=lr)
loss_fn = nn.CrossEntropyLoss()

print("Device:", device)

# ==============================
# Save model function
# ==============================
def save_model(model, tokenizer, model_name="my_intent_model_pasca"):
    model.save_pretrained(model_name)
    tokenizer.save_pretrained(model_name)
    import pickle
    with open(model_name + "/label_encoder.pkl", "wb") as f:
        pickle.dump(label_encoder, f)
    print(f"✅ Model saved to folder: {model_name}")

# ==============================
# Train loop
# ==============================
def train_model(model, train_loader, loss_fn, optimizer, device, epochs=n_epochs):
    model.train()
    train_losses = []
    for epoch in range(epochs):
        total_loss = 0
        correct_predictions = 0
        for batch in train_loader:
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["label"].to(device)

            optimizer.zero_grad()
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            loss = loss_fn(outputs.logits, labels)
            total_loss += loss.item()

            _, preds = torch.max(outputs.logits, dim=1)
            correct_predictions += torch.sum(preds == labels)

            loss.backward()
            optimizer.step()

        avg_loss = total_loss / len(train_loader)
        acc = correct_predictions.double() / len(train_loader.dataset)
        train_losses.append(avg_loss)

        print(f"Epoch {epoch+1}/{epochs} | Loss: {avg_loss:.4f} | Acc: {acc:.4f}")
    return train_losses

# ==============================
# Evaluation
# ==============================
def evaluate_model(model, test_loader, device):
    model.eval()
    preds, labels = [], []
    with torch.no_grad():
        for batch in test_loader:
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            y_true = batch["label"].to(device)

            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            _, y_pred = torch.max(outputs.logits, dim=1)

            preds.extend(y_pred.cpu().numpy())
            labels.extend(y_true.cpu().numpy())

    acc = accuracy_score(labels, preds)
    print(f"Accuracy: {acc:.4f}")
    print(classification_report(labels, preds, target_names=label_encoder.classes_))
    return acc

# ==============================
# Jalankan Training
# ==============================
train_losses = train_model(model, train_loader, loss_fn, optimizer, device)
save_model(model, tokenizer)
acc = evaluate_model(model, test_loader, device)

plt.plot(train_losses, label="Training Loss")
plt.title("Training Loss over Epochs")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()
plt.show()
