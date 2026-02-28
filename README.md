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

**RAG SOP Assistant** is an enterprise-ready, AI-powered knowledge management system designed to revolutionize how organizations interact with their Standard Operating Procedure (SOP) documents.

Built on top of the **Retrieval-Augmented Generation (RAG)** architecture, this system transforms static, hard-to-navigate SOP files into a dynamic, conversational knowledge base. Employees can simply type a question in natural language — just like chatting with a colleague — and receive accurate, context-aware answers sourced directly from official company documents.

Under the hood, the system leverages **multilingual sentence embeddings** to understand the semantic meaning behind every question, performs **vector similarity search** across all indexed documents using ChromaDB, and then passes the most relevant context to **DeepSeek V3 LLM** to generate a clear, well-structured answer in Indonesian.

### 🧩 Core Concepts

> **What is RAG?** Retrieval-Augmented Generation is an AI pattern that enhances LLM responses by first retrieving relevant information from a knowledge base, then using that context to generate grounded, factual answers — eliminating hallucination and ensuring accuracy.

```
┌──────────┐     ┌───────────┐     ┌──────────┐     ┌──────────┐
│ 📝 Query │ ──▶ │ 🔍 Search │ ──▶ │ 📄 Docs  │ ──▶ │ 🧠 LLM   │
│          │     │ (Vectors) │     │ (Context)│     │ (Answer) │
└──────────┘     └───────────┘     └──────────┘     └──────────┘
```

### 💡 Why This Matters

Every organization maintains dozens — sometimes hundreds — of SOP documents covering everything from employee onboarding to emergency protocols. These documents are critical for compliance, consistency, and operational excellence. Yet in practice, they often collect dust in shared drives, rarely read, and hard to search.

**RAG SOP Assistant** solves this by making SOPs instantly accessible through conversation:

| Problem | Solution |
|---------|----------|
| 📚 SOP documents are scattered across drives and hard to find | 🔍 AI-powered semantic search across all documents at once |
| ⏰ New employees spend weeks learning procedures manually | 💬 Instant answers through natural language Q&A |
| 🔄 Critical information is buried deep inside long documents | 📊 Intelligent chunking & retrieval surfaces the right section |
| 📞 HR/Admin teams waste hours answering repetitive questions | 🤖 AI assistant handles FAQs 24/7 with zero fatigue |
| 🔎 Keyword search fails when you don't know the exact term | 🧠 Semantic understanding matches meaning, not just words |
| 📋 Compliance audits require quick access to procedures | ⚡ Instant lookup with source document references |

### 🏢 Use Cases

- **🧑‍💼 HR & People Ops** — Employee onboarding, leave policies, benefits, disciplinary procedures
- **🏭 Operations** — Warehouse safety, equipment handling, quality control processes
- **💰 Finance & Procurement** — Purchase approval workflows, expense policies, vendor management
- **🛡️ Compliance** — Regulatory procedures, audit checklists, emergency response protocols
- **🎓 Training** — Quick reference for trainees, refresher on procedures, knowledge assessment

### ✨ Key Features

| Feature | Description |
|---------|-------------|
| 💬 **AI Chat** | Natural language Q&A — ask anything about your company SOPs |
| 📤 **Multi-Format Upload** | Supports PDF, Word (.docx), and plain TXT documents |
| 🧠 **Semantic Search** | Meaning-based retrieval powered by multilingual embeddings |
| ✂️ **Smart Chunking** | Sentence-boundary aware splitting — never cuts mid-word |
| 📊 **Database Management** | Real-time stats, document list, and one-click database clear |
| 📄 **Auto-Index on Startup** | Default SOP documents are automatically indexed when the app starts |
| 🔒 **Thread-Safe** | Lock-based concurrency control for safe multi-user access |
| 🛡️ **XSS Protected** | All user inputs & filenames are HTML-escaped |
| 🚫 **Error Sanitization** | Sensitive information (API keys) never leaks in error messages |
| 📏 **Input Validation** | Questions capped at 1000 chars, file uploads capped at 50MB |
| 🎨 **Premium UI** | Polished interface with custom CSS, gradient headers, and animations |
| 🔍 **Source Attribution** | Every answer includes references to the source SOP document |

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
