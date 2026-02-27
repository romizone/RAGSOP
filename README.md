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

# 📋 RAG SOP Perusahaan

Sistem tanya jawab cerdas berbasis AI untuk dokumen Standard Operating Procedure perusahaan.

## Stack
- **Embedding**: `intfloat/multilingual-e5-large`
- **Vector DB**: ChromaDB
- **LLM**: DeepSeek-V3
- **UI**: Gradio

## Setup
1. Buat HF Space baru (SDK: Gradio)
2. Upload `app.py`, `requirements.txt`, dan `README.md`
3. Tambahkan Secret: `DEEPSEEK_API_KEY`
4. Tunggu build selesai (~3-5 menit)
5. Upload dokumen SOP → Mulai bertanya!
