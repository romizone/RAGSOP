---
title: RAG SOP Perusahaan
emoji: 📋
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: "5.9.1"
app_file: app.py
pinned: true
---

<div align="center">

# 📋 RAG SOP Perusahaan

### *Intelligent Q&A System for Corporate Standard Operating Procedures*

[![Release](https://img.shields.io/badge/Release-v1.0.0-blue?style=for-the-badge&logo=semantic-release&logoColor=white)](https://github.com/romizone/RAGSOP/releases)
[![HF Space](https://img.shields.io/badge/🤗%20Live%20Demo-Hugging%20Face-yellow?style=for-the-badge)](https://huggingface.co/spaces/romizone/RAG-SOP)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)

<br/>

<img src="https://em-content.zobj.net/source/twitter/408/robot_1f916.png" width="80"/>

**Sistem tanya jawab cerdas berbasis AI** yang memungkinkan karyawan bertanya tentang prosedur perusahaan secara natural dan mendapat jawaban akurat langsung dari dokumen SOP resmi.

[🚀 Coba Live Demo](https://huggingface.co/spaces/romizone/RAG-SOP) · [📖 Dokumentasi](#-cara-kerja) · [🐛 Report Bug](https://github.com/romizone/RAGSOP/issues)

</div>

---

## 🎯 Tentang Proyek

**RAG SOP Perusahaan** adalah solusi enterprise-ready yang menggabungkan teknologi **Retrieval-Augmented Generation (RAG)** dengan **Large Language Model (LLM)** untuk menjadikan dokumen SOP perusahaan sebagai sumber pengetahuan yang mudah diakses.

### 💡 Mengapa Ini Dibutuhkan?

| Masalah | Solusi |
|---------|--------|
| 📚 Dokumen SOP bertumpuk dan sulit dicari | 🔍 Pencarian semantik berbasis AI |
| ⏰ Karyawan baru butuh waktu lama memahami prosedur | 💬 Tanya jawab natural seperti chat |
| 🔄 Informasi tersebar di banyak file | 📊 Database terpusat dengan vector search |
| 📞 HR/Admin sering menjawab pertanyaan berulang | 🤖 Asisten AI yang selalu tersedia 24/7 |

### ✨ Fitur Utama

| Fitur | Deskripsi |
|-------|-----------|
| 💬 **Chat AI** | Tanya jawab natural tentang SOP perusahaan |
| 📤 **Multi-Format Upload** | Mendukung PDF, Word (.docx), dan TXT |
| 🧠 **Semantic Search** | Pencarian berbasis makna, bukan sekadar kata kunci |
| 📊 **Database Management** | Lihat statistik, daftar dokumen, clear database |
| 🔒 **Thread-Safe** | Aman untuk concurrent access |
| 🛡️ **XSS Protected** | Input & output ter-sanitasi |
| 📄 **Auto-Index** | Dokumen default otomatis ter-index saat startup |
| 🎨 **Premium UI** | Antarmuka modern dengan custom CSS |

---

## 🏗️ Arsitektur & Tech Stack

```
┌─────────────────────────────────────────────────┐
│                   👤 User                        │
│              (Browser / Gradio UI)               │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│              🎨 Gradio 5.9.1                     │
│         (Premium UI + 3 Tab Interface)           │
├─────────────┬───────────────┬───────────────────┤
│  💬 Chat    │  📤 Upload    │  📊 Database      │
└──────┬──────┴───────┬───────┴─────────┬─────────┘
       │              │                 │
       ▼              ▼                 ▼
┌─────────────┐ ┌───────────┐  ┌──────────────┐
│ 🧠 DeepSeek │ │ ✂️ Chunker │  │ 📊 ChromaDB  │
│   V3 (LLM)  │ │ (Sentence │  │  (Stats &    │
│             │ │  Boundary) │  │   Manage)    │
└─────────────┘ └─────┬─────┘  └──────────────┘
                      │
                      ▼
              ┌───────────────┐
              │ 🔮 E5-Small   │
              │  (Embedding)  │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │ 💾 ChromaDB   │
              │ (Vector Store)│
              └───────────────┘
```

### 🔧 Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| 🎨 **Frontend** | Gradio 5.9.1 | UI Framework + Custom CSS |
| 🧠 **LLM** | DeepSeek-V3 | Generasi jawaban bahasa Indonesia |
| 🔮 **Embedding** | intfloat/multilingual-e5-small | Vektor representasi teks multilingual |
| 💾 **Vector DB** | ChromaDB | Penyimpanan & pencarian vektor |
| 📄 **PDF Parser** | PyMuPDF | Ekstraksi teks dari PDF |
| 📝 **DOCX Parser** | python-docx | Ekstraksi teks dari Word |

---

## 🚀 Quick Start

### Option 1: Hugging Face Spaces (Recommended)

> **Zero setup!** Langsung pakai di cloud.

1. **Fork** Space ini ke akun HF kamu
2. Tambahkan Secret: `DEEPSEEK_API_KEY` di Settings
3. Tunggu build selesai (~3-5 menit)
4. Upload dokumen SOP dan mulai bertanya!

### Option 2: Local Development

```bash
# 1. Clone repository
git clone https://github.com/romizone/RAGSOP.git
cd RAGSOP

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set API key
export DEEPSEEK_API_KEY="your-api-key-here"

# 4. Run
python app.py
```

Buka `http://localhost:7860` di browser.

---

## 📖 Cara Kerja

### 1️⃣ Upload & Chunking
```
📄 Dokumen SOP  →  ✂️ Sentence-Boundary Chunking  →  500 char chunks
```
File PDF/DOCX/TXT dipecah menjadi potongan teks ~500 karakter dengan pemotongan di batas kalimat (bukan di tengah kata).

### 2️⃣ Embedding & Storage
```
📝 Text Chunks  →  🔮 E5-Small Embedding  →  💾 ChromaDB (Cosine Similarity)
```
Setiap chunk dikonversi menjadi vektor 384-dimensi dan disimpan di ChromaDB.

### 3️⃣ Query & Retrieval
```
❓ Pertanyaan  →  🔍 Semantic Search (Top 5)  →  🧠 DeepSeek V3  →  💬 Jawaban
```
Pertanyaan dicocokkan dengan chunk paling relevan, lalu LLM menghasilkan jawaban berdasarkan konteks.

---

## 🔒 Security

| Fitur | Implementasi |
|-------|-------------|
| 🛡️ XSS Prevention | Semua input/output di-escape via `html.escape()` |
| 🔐 API Key Protection | Disimpan sebagai environment variable (HF Secrets) |
| 🚫 Error Sanitization | Error messages tidak mengekspos informasi sensitif |
| 📏 Input Validation | Pertanyaan max 1000 karakter, file max 50MB |
| 🔒 Thread Safety | `threading.Lock` untuk concurrent access |

---

## 📁 Struktur Proyek

```
RAGSOP/
├── 📄 app.py              # Aplikasi utama (Gradio + RAG pipeline)
├── 📋 requirements.txt    # Python dependencies
├── 📖 README.md           # Dokumentasi (file ini)
├── 🚫 .gitignore          # Git ignore rules
└── 📂 SOP/                # Dokumen SOP default (auto-indexed)
    ├── Kumpulan_SOP_Perusahaan.pdf
    ├── Pelatihan staf_8.pdf
    ├── Penggunaan teknologi_7.pdf
    ├── Penyimpanan dan pemeliharaan_4.pdf
    └── SOP darurat_5.pdf
```

---

## 📊 Performance

| Metric | Value |
|--------|-------|
| ⏱️ Startup Time | ~30-60s (termasuk model loading) |
| 📄 Default SOP Files | 5 dokumen, ~256 chunks |
| 🔮 Embedding Model Size | ~470MB |
| 💬 Query Response Time | ~3-5s per pertanyaan |
| 💾 Hardware | CPU Basic (2 vCPU, 16GB RAM) |

---

## 🗺️ Roadmap

- [x] ~~v1.0 — Core RAG + Premium UI + Auto-indexing~~
- [ ] v1.1 — Persistent storage (data survive restart)
- [ ] v1.2 — Multi-language support (EN/ID)
- [ ] v1.3 — Document version tracking
- [ ] v2.0 — Authentication + multi-tenant

---

## 🤝 Contributing

Contributions welcome! Silakan buka [Issue](https://github.com/romizone/RAGSOP/issues) atau kirim Pull Request.

---

## 👨‍💻 Author

**Romi Nur Ismanto**
- 🌐 [rominur.com](https://rominur.com)
- 🤗 [Hugging Face](https://huggingface.co/romizone)
- 🐙 [GitHub](https://github.com/romizone)

---

<div align="center">

Built with ❤️ using **ChromaDB** · **DeepSeek** · **Multilingual E5** · **Gradio**

[![Star](https://img.shields.io/github/stars/romizone/RAGSOP?style=social)](https://github.com/romizone/RAGSOP)

</div>
