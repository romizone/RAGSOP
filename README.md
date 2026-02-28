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

# 📋 RAG SOP Assistant

### *Intelligent Q&A System for Corporate Standard Operating Procedures*

[![Release](https://img.shields.io/badge/Release-v1.0.0-blue?style=for-the-badge&logo=semantic-release&logoColor=white)](https://github.com/romizone/RAGSOP/releases)
[![HF Space](https://img.shields.io/badge/🤗%20Live%20Demo-Hugging%20Face-yellow?style=for-the-badge)](https://huggingface.co/spaces/romizone/RAG-SOP)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)

<br/>

<img src="https://em-content.zobj.net/source/twitter/408/robot_1f916.png" width="80"/>

**An AI-powered smart Q&A system** that enables employees to ask questions about company procedures in natural language and receive accurate answers directly from official SOP documents.

[🚀 Try Live Demo](https://huggingface.co/spaces/romizone/RAG-SOP) · [📖 Documentation](#-how-it-works) · [🐛 Report Bug](https://github.com/romizone/RAGSOP/issues)

</div>

---

## 🎯 About

**RAG SOP Assistant** is an enterprise-ready solution that combines **Retrieval-Augmented Generation (RAG)** with a **Large Language Model (LLM)** to turn corporate SOP documents into an easily accessible knowledge base.

### 💡 Why This Matters

| Problem | Solution |
|---------|----------|
| 📚 SOP documents are scattered and hard to find | 🔍 AI-powered semantic search |
| ⏰ New employees need a long time to learn procedures | 💬 Natural language Q&A like chatting |
| 🔄 Information is spread across many files | 📊 Centralized database with vector search |
| 📞 HR/Admin repeatedly answering the same questions | 🤖 AI assistant available 24/7 |

### ✨ Key Features

| Feature | Description |
|---------|-------------|
| 💬 **AI Chat** | Natural language Q&A about company SOPs |
| 📤 **Multi-Format Upload** | Supports PDF, Word (.docx), and TXT |
| 🧠 **Semantic Search** | Meaning-based retrieval, not just keyword matching |
| 📊 **Database Management** | View stats, document list, and clear database |
| 🔒 **Thread-Safe** | Safe for concurrent access |
| 🛡️ **XSS Protected** | All inputs & outputs are sanitized |
| 📄 **Auto-Index** | Default SOP documents are automatically indexed at startup |
| 🎨 **Premium UI** | Modern interface with custom CSS design |

---

## 🏗️ Architecture & Tech Stack

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
| 🧠 **LLM** | DeepSeek-V3 | Indonesian language answer generation |
| 🔮 **Embedding** | intfloat/multilingual-e5-small | Multilingual text vector representation |
| 💾 **Vector DB** | ChromaDB | Vector storage & similarity search |
| 📄 **PDF Parser** | PyMuPDF | Text extraction from PDF files |
| 📝 **DOCX Parser** | python-docx | Text extraction from Word documents |

---

## 🚀 Quick Start

### Option 1: Hugging Face Spaces (Recommended)

> **Zero setup!** Run it instantly in the cloud.

1. **Fork** this Space to your HF account
2. Add Secret: `DEEPSEEK_API_KEY` in Settings
3. Wait for the build to complete (~3-5 minutes)
4. Upload SOP documents and start asking questions!

### Option 2: Local Development

```bash
# 1. Clone the repository
git clone https://github.com/romizone/RAGSOP.git
cd RAGSOP

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your API key
export DEEPSEEK_API_KEY="your-api-key-here"

# 4. Run the application
python app.py
```

Open `http://localhost:7860` in your browser.

---

## 📖 How It Works

### 1️⃣ Upload & Chunking
```
📄 SOP Document  →  ✂️ Sentence-Boundary Chunking  →  ~500 char chunks
```
PDF/DOCX/TXT files are split into ~500 character text chunks with intelligent sentence-boundary splitting (never cuts mid-word).

### 2️⃣ Embedding & Storage
```
📝 Text Chunks  →  🔮 E5-Small Embedding  →  💾 ChromaDB (Cosine Similarity)
```
Each chunk is converted into a 384-dimensional vector and stored in ChromaDB for fast similarity search.

### 3️⃣ Query & Retrieval
```
❓ Question  →  🔍 Semantic Search (Top 5)  →  🧠 DeepSeek V3  →  💬 Answer
```
The user's question is matched against the most relevant chunks, then the LLM generates an accurate answer based on the retrieved context.

---

## 🔒 Security

| Feature | Implementation |
|---------|---------------|
| 🛡️ XSS Prevention | All inputs/outputs escaped via `html.escape()` |
| 🔐 API Key Protection | Stored as environment variable (HF Secrets) |
| 🚫 Error Sanitization | Error messages never expose sensitive information |
| 📏 Input Validation | Questions capped at 1000 chars, files capped at 50MB |
| 🔒 Thread Safety | `threading.Lock` for safe concurrent access |

---

## 📁 Project Structure

```
RAGSOP/
├── 📄 app.py              # Main application (Gradio + RAG pipeline)
├── 📋 requirements.txt    # Python dependencies
├── 📖 README.md           # Documentation (this file)
├── 🚫 .gitignore          # Git ignore rules
└── 📂 SOP/                # Default SOP documents (auto-indexed)
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
| ⏱️ Startup Time | ~30-60s (includes model loading) |
| 📄 Default SOP Files | 5 documents, ~256 chunks |
| 🔮 Embedding Model Size | ~470MB |
| 💬 Query Response Time | ~3-5s per question |
| 💾 Hardware | CPU Basic (2 vCPU, 16GB RAM) |

---

## 🗺️ Roadmap

- [x] ~~v1.0 — Core RAG + Premium UI + Auto-indexing~~
- [ ] v1.1 — Persistent storage (data survives restart)
- [ ] v1.2 — Multi-language support (EN/ID)
- [ ] v1.3 — Document version tracking
- [ ] v2.0 — Authentication + multi-tenant support

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an [Issue](https://github.com/romizone/RAGSOP/issues) or submit a Pull Request.

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
