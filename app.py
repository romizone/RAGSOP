"""
RAG SOP Perusahaan - Premium UI
Deploy di Hugging Face Spaces
Stack: ChromaDB + Sentence Transformers + DeepSeek API + Gradio
"""

import os
import gradio as gr
import chromadb
from chromadb.utils import embedding_functions
from openai import OpenAI
import hashlib
from pathlib import Path
import time

# ============================================
# CONFIGURATION
# ============================================
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
COLLECTION_NAME = "sop_perusahaan"
EMBEDDING_MODEL = "intfloat/multilingual-e5-small"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
TOP_K = 5

# ============================================
# INITIALIZE COMPONENTS (lazy loading)
# ============================================
chroma_client = chromadb.PersistentClient(path="./chroma_db")

ef = None
collection = None

def get_collection():
    global ef, collection
    if collection is None:
        ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=EMBEDDING_MODEL
        )
        collection = chroma_client.get_or_create_collection(
            name=COLLECTION_NAME,
            embedding_function=ef,
            metadata={"hnsw:space": "cosine"}
        )
    return collection

deepseek_client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)

# ============================================
# DOCUMENT PROCESSING
# ============================================

def extract_text_from_pdf(file_path):
    try:
        import pymupdf
        doc = pymupdf.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text() + "\n"
        doc.close()
        return text.strip()
    except Exception as e:
        print(f"Error reading PDF {file_path}: {e}")
        return ""


def extract_text_from_docx(file_path):
    try:
        import docx
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
        return text.strip()
    except Exception as e:
        print(f"Error reading DOCX {file_path}: {e}")
        return ""


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    if not text:
        return []
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk.strip())
        start = end - overlap
    return chunks


def generate_chunk_id(filename, chunk_index):
    raw = f"{filename}_chunk_{chunk_index}"
    return hashlib.md5(raw.encode()).hexdigest()


def process_and_store(files, progress=gr.Progress()):
    if not files:
        return "❌ Tidak ada file yang diupload."

    total_chunks = 0
    processed_files = 0
    skipped_files = []

    progress(0, desc="Memulai proses...")

    for i, file in enumerate(files):
        file_path = file.name if hasattr(file, 'name') else str(file)
        filename = Path(file_path).name
        suffix = Path(file_path).suffix.lower()

        progress((i + 1) / len(files), desc=f"📄 {filename}")

        if suffix == ".pdf":
            text = extract_text_from_pdf(file_path)
        elif suffix == ".docx":
            text = extract_text_from_docx(file_path)
        elif suffix == ".txt":
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
        else:
            skipped_files.append(filename)
            continue

        if not text:
            skipped_files.append(filename)
            continue

        chunks = chunk_text(text)
        if not chunks:
            skipped_files.append(filename)
            continue

        ids = [generate_chunk_id(filename, j) for j in range(len(chunks))]
        metadatas = [{"source": filename, "chunk_index": j} for j in range(len(chunks))]

        batch_size = 100
        for batch_start in range(0, len(chunks), batch_size):
            batch_end = min(batch_start + batch_size, len(chunks))
            get_collection().upsert(
                ids=ids[batch_start:batch_end],
                documents=chunks[batch_start:batch_end],
                metadatas=metadatas[batch_start:batch_end]
            )

        total_chunks += len(chunks)
        processed_files += 1

    result = f"""
<div style="background: linear-gradient(135deg, #0c4a6e22, #0e7a6d22); border-radius: 16px; padding: 24px; border: 1px solid #0e7a6d33;">
    <h3 style="margin:0 0 16px 0; color: #0e7a6d;">✅ Upload Berhasil!</h3>
    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px;">
        <div style="background: white; border-radius: 12px; padding: 16px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
            <div style="font-size: 28px; font-weight: 700; color: #0c4a6e;">{processed_files}</div>
            <div style="font-size: 13px; color: #64748b;">File Diproses</div>
        </div>
        <div style="background: white; border-radius: 12px; padding: 16px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
            <div style="font-size: 28px; font-weight: 700; color: #0e7a6d;">{total_chunks}</div>
            <div style="font-size: 13px; color: #64748b;">Chunks Dibuat</div>
        </div>
        <div style="background: white; border-radius: 12px; padding: 16px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
            <div style="font-size: 28px; font-weight: 700; color: #6366f1;">{get_collection().count()}</div>
            <div style="font-size: 13px; color: #64748b;">Total di Database</div>
        </div>
    </div>
</div>
"""
    if skipped_files:
        result += f'\n<p style="color: #f59e0b; font-size: 13px; margin-top: 12px;">⚠️ Dilewati: {", ".join(skipped_files[:10])}</p>'

    return result


# ============================================
# RAG QUERY
# ============================================

def query_rag(question, chat_history):
    if not question.strip():
        return chat_history, ""

    if get_collection().count() == 0:
        chat_history.append({
            "role": "user",
            "content": question
        })
        chat_history.append({
            "role": "assistant",
            "content": "⚠️ Database masih kosong. Silakan upload dokumen SOP terlebih dahulu di tab **📤 Upload Dokumen**."
        })
        return chat_history, ""

    if not DEEPSEEK_API_KEY:
        chat_history.append({
            "role": "user",
            "content": question
        })
        chat_history.append({
            "role": "assistant",
            "content": "⚠️ DeepSeek API key belum diset. Tambahkan `DEEPSEEK_API_KEY` di Settings → Secrets pada HF Space."
        })
        return chat_history, ""

    # Retrieve relevant chunks
    results = get_collection().query(
        query_texts=[question],
        n_results=TOP_K
    )

    context_parts = []
    sources = set()
    for i, (doc, metadata) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
        context_parts.append(f"[Bagian {i+1} dari {metadata['source']}]\n{doc}")
        sources.add(metadata["source"])

    context = "\n\n---\n\n".join(context_parts)

    system_prompt = """Kamu adalah asisten AI yang membantu menjawab pertanyaan berdasarkan dokumen SOP (Standard Operating Procedure) perusahaan.

ATURAN:
1. Jawab HANYA berdasarkan konteks yang diberikan
2. Jika informasi tidak ada di konteks, katakan "Maaf, saya tidak menemukan informasi tersebut di dokumen SOP yang tersedia."
3. Jawab dalam Bahasa Indonesia
4. Berikan jawaban yang jelas dan terstruktur
5. Sebutkan sumber dokumen jika relevan"""

    user_prompt = f"""Konteks dari dokumen SOP:

{context}

---

Pertanyaan: {question}

Jawab berdasarkan konteks di atas:"""

    try:
        response = deepseek_client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=1500
        )

        answer = response.choices[0].message.content
        source_list = " · ".join([f"📄 {s}" for s in sources])
        full_answer = f"{answer}\n\n---\n🔍 **Sumber:** {source_list}"

    except Exception as e:
        full_answer = f"❌ Error: {str(e)}"

    chat_history.append({"role": "user", "content": question})
    chat_history.append({"role": "assistant", "content": full_answer})
    return chat_history, ""


def get_db_stats():
    count = get_collection().count()
    if count == 0:
        return """
<div style="text-align: center; padding: 60px 20px; color: #94a3b8;">
    <div style="font-size: 48px; margin-bottom: 16px;">📭</div>
    <h3 style="margin: 0 0 8px 0; color: #475569;">Database Kosong</h3>
    <p style="margin: 0;">Upload dokumen SOP di tab <strong>📤 Upload Dokumen</strong> untuk memulai.</p>
</div>
"""

    all_data = get_collection().get(include=["metadatas"])
    sources = set()
    for meta in all_data["metadatas"]:
        sources.add(meta.get("source", "unknown"))

    doc_list = "".join([
        f'<div style="display: flex; align-items: center; gap: 10px; padding: 10px 14px; background: #f8fafc; border-radius: 8px; margin-bottom: 6px; border: 1px solid #e2e8f0;">'
        f'<span style="color: #6366f1;">📄</span>'
        f'<span style="font-size: 13px; color: #334155;">{s}</span>'
        f'</div>'
        for s in sorted(sources)
    ])

    return f"""
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px;">
    <div style="background: linear-gradient(135deg, #6366f1, #8b5cf6); border-radius: 16px; padding: 24px; color: white; box-shadow: 0 4px 16px rgba(99,102,241,0.3);">
        <div style="font-size: 36px; font-weight: 800;">{count}</div>
        <div style="font-size: 14px; opacity: 0.85;">Total Chunks</div>
    </div>
    <div style="background: linear-gradient(135deg, #0e7a6d, #10b981); border-radius: 16px; padding: 24px; color: white; box-shadow: 0 4px 16px rgba(14,122,109,0.3);">
        <div style="font-size: 36px; font-weight: 800;">{len(sources)}</div>
        <div style="font-size: 14px; opacity: 0.85;">Dokumen Tersimpan</div>
    </div>
</div>
<div>
    <h4 style="margin: 0 0 12px 0; color: #1e293b;">📚 Daftar Dokumen</h4>
    {doc_list}
</div>
"""


def clear_database():
    global collection, ef
    chroma_client.delete_collection(COLLECTION_NAME)
    collection = None
    ef = None
    return """
<div style="text-align: center; padding: 40px; background: #fef2f2; border-radius: 16px; border: 1px solid #fecaca;">
    <div style="font-size: 36px; margin-bottom: 12px;">🗑️</div>
    <h3 style="margin: 0 0 8px 0; color: #dc2626;">Database Dikosongkan</h3>
    <p style="margin: 0; color: #991b1b; font-size: 14px;">Semua data telah dihapus. Upload dokumen baru untuk memulai kembali.</p>
</div>
"""


# ============================================
# PREMIUM CSS
# ============================================

CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

* {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* === MAIN CONTAINER === */
.gradio-container {
    max-width: 1100px !important;
    margin: 0 auto !important;
    background: #f0f4f8 !important;
}

/* === HEADER === */
.app-header {
    background: linear-gradient(135deg, #0c2d48 0%, #0a4d68 40%, #0e7a6d 100%);
    border-radius: 20px;
    padding: 40px 32px;
    margin-bottom: 8px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(12, 45, 72, 0.3);
}

.app-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(14,122,109,0.3) 0%, transparent 70%);
    border-radius: 50%;
}

.app-header::after {
    content: '';
    position: absolute;
    bottom: -30%;
    left: -10%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(99,102,241,0.2) 0%, transparent 70%);
    border-radius: 50%;
}

.header-content {
    position: relative;
    z-index: 1;
}

.header-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(255,255,255,0.12);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 100px;
    padding: 6px 16px;
    font-size: 12px;
    font-weight: 600;
    color: #a7f3d0;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-bottom: 16px;
}

.header-title {
    font-size: 32px;
    font-weight: 800;
    color: white;
    margin: 0 0 8px 0;
    letter-spacing: -0.5px;
    line-height: 1.2;
}

.header-subtitle {
    font-size: 15px;
    color: rgba(255,255,255,0.7);
    margin: 0;
    font-weight: 400;
    max-width: 500px;
}

.header-stats {
    display: flex;
    gap: 24px;
    margin-top: 20px;
}

.header-stat {
    display: flex;
    align-items: center;
    gap: 8px;
    color: rgba(255,255,255,0.6);
    font-size: 13px;
}

.header-stat-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #34d399;
    box-shadow: 0 0 8px rgba(52,211,153,0.5);
}

/* === TABS === */
.tab-nav {
    border: none !important;
    background: transparent !important;
    gap: 4px !important;
    padding: 4px !important;
    margin-bottom: 4px !important;
}

.tab-nav button {
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 24px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    color: #64748b !important;
    background: transparent !important;
    transition: all 0.2s ease !important;
}

.tab-nav button:hover {
    background: #e2e8f0 !important;
    color: #334155 !important;
}

.tab-nav button.selected {
    background: white !important;
    color: #0c4a6e !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
}

/* === CHAT === */
.chatbot {
    border: 1px solid #e2e8f0 !important;
    border-radius: 16px !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04) !important;
    background: white !important;
}

.chatbot .message {
    border-radius: 12px !important;
    font-size: 14px !important;
    line-height: 1.7 !important;
}

/* === INPUT === */
.input-row {
    background: white;
    border-radius: 16px;
    border: 2px solid #e2e8f0;
    transition: border-color 0.2s ease;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.input-row:focus-within {
    border-color: #0e7a6d;
    box-shadow: 0 0 0 3px rgba(14,122,109,0.1);
}

textarea {
    border: none !important;
    background: transparent !important;
    font-size: 14px !important;
    padding: 14px 16px !important;
}

textarea:focus {
    box-shadow: none !important;
}

/* === BUTTONS === */
.primary-btn, button.primary {
    background: linear-gradient(135deg, #0c4a6e, #0e7a6d) !important;
    border: none !important;
    border-radius: 12px !important;
    color: white !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 12px 24px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 8px rgba(14,122,109,0.25) !important;
}

.primary-btn:hover, button.primary:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(14,122,109,0.35) !important;
}

button.secondary {
    background: white !important;
    border: 1.5px solid #e2e8f0 !important;
    border-radius: 12px !important;
    color: #475569 !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}

button.secondary:hover {
    border-color: #0e7a6d !important;
    color: #0e7a6d !important;
}

button.stop {
    background: #fef2f2 !important;
    border: 1.5px solid #fecaca !important;
    border-radius: 12px !important;
    color: #dc2626 !important;
    font-weight: 600 !important;
}

button.stop:hover {
    background: #fee2e2 !important;
}

/* === FILE UPLOAD === */
.upload-area {
    border: 2px dashed #cbd5e1 !important;
    border-radius: 16px !important;
    background: #f8fafc !important;
    transition: all 0.2s ease !important;
    padding: 40px !important;
}

.upload-area:hover {
    border-color: #0e7a6d !important;
    background: #f0fdf4 !important;
}

/* === EXAMPLES === */
.examples-row {
    gap: 8px !important;
}

.examples-row button {
    background: white !important;
    border: 1.5px solid #e2e8f0 !important;
    border-radius: 10px !important;
    padding: 8px 16px !important;
    font-size: 13px !important;
    color: #475569 !important;
    transition: all 0.15s ease !important;
}

.examples-row button:hover {
    border-color: #0e7a6d !important;
    color: #0e7a6d !important;
    background: #f0fdf4 !important;
}

/* === FOOTER === */
.app-footer {
    text-align: center;
    padding: 20px;
    color: #94a3b8;
    font-size: 12px;
}

.app-footer a {
    color: #0e7a6d;
    text-decoration: none;
    font-weight: 600;
}

/* === SCROLLBAR === */
::-webkit-scrollbar {
    width: 6px;
}

::-webkit-scrollbar-track {
    background: transparent;
}

::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
    background: #94a3b8;
}

/* === MISC === */
.block {
    border: none !important;
    box-shadow: none !important;
}

.panel {
    background: white;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    padding: 24px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

footer {
    display: none !important;
}
"""


# ============================================
# GRADIO UI
# ============================================

with gr.Blocks(
    title="RAG SOP Perusahaan",
    theme=gr.themes.Base(
        primary_hue=gr.themes.colors.teal,
        secondary_hue=gr.themes.colors.blue,
        neutral_hue=gr.themes.colors.slate,
        font=gr.themes.GoogleFont("Plus Jakarta Sans"),
        radius_size=gr.themes.sizes.radius_lg,
    ),
    css=CUSTOM_CSS,
) as demo:

    # HEADER
    gr.HTML("""
    <div class="app-header">
        <div class="header-content">
            <div class="header-badge">
                <span class="header-stat-dot"></span>
                AI-Powered
            </div>
            <h1 class="header-title">📋 SOP Assistant</h1>
            <p class="header-subtitle">
                Tanya jawab cerdas berbasis AI untuk dokumen Standard Operating Procedure perusahaan Anda
            </p>
            <div class="header-stats">
                <div class="header-stat">
                    <span>🧠</span> Multilingual E5 Embedding
                </div>
                <div class="header-stat">
                    <span>⚡</span> DeepSeek LLM
                </div>
                <div class="header-stat">
                    <span>💾</span> ChromaDB Vector Store
                </div>
            </div>
        </div>
    </div>
    """)

    with gr.Tabs() as tabs:

        # ======== TAB 1: CHAT ========
        with gr.TabItem("💬 Tanya Jawab", id="chat"):
            chatbot = gr.Chatbot(
                height=480,
                type="messages",
                show_label=False,
                avatar_images=(None, "https://em-content.zobj.net/source/twitter/408/robot_1f916.png"),
                placeholder="""<div style="text-align: center; padding: 40px 20px; color: #94a3b8;">
                    <div style="font-size: 48px; margin-bottom: 16px;">💬</div>
                    <h3 style="margin: 0 0 8px 0; color: #475569; font-weight: 700;">Mulai Bertanya</h3>
                    <p style="margin: 0; font-size: 14px;">Upload dokumen SOP terlebih dahulu, lalu ketik pertanyaan Anda di bawah</p>
                </div>""",
            )

            with gr.Row():
                msg = gr.Textbox(
                    placeholder="Ketik pertanyaan tentang SOP perusahaan...",
                    show_label=False,
                    scale=9,
                    container=False,
                    lines=1,
                    max_lines=3,
                )
                send_btn = gr.Button(
                    "Kirim ➤",
                    variant="primary",
                    scale=1,
                    min_width=100,
                )

            gr.Markdown(
                "<p style='color: #94a3b8; font-size: 12px; margin: 4px 0 8px 0;'>💡 Tekan Enter untuk mengirim · Contoh pertanyaan di bawah</p>"
            )

            gr.Examples(
                examples=[
                    ["Bagaimana prosedur pengajuan cuti karyawan?"],
                    ["Apa saja langkah dalam proses quality control?"],
                    ["Jelaskan SOP penanganan komplain customer"],
                    ["Bagaimana prosedur purchasing barang?"],
                    ["Apa aturan keamanan di area gudang?"],
                ],
                inputs=msg,
                label="",
            )

            msg.submit(query_rag, [msg, chatbot], [chatbot, msg])
            send_btn.click(query_rag, [msg, chatbot], [chatbot, msg])

        # ======== TAB 2: UPLOAD ========
        with gr.TabItem("📤 Upload Dokumen", id="upload"):
            gr.HTML("""
            <div style="margin-bottom: 20px;">
                <h2 style="margin: 0 0 8px 0; color: #1e293b; font-weight: 700; font-size: 22px;">
                    📤 Upload Dokumen SOP
                </h2>
                <p style="margin: 0; color: #64748b; font-size: 14px;">
                    Upload file PDF, Word (.docx), atau TXT. Sistem akan otomatis memproses,
                    memecah menjadi chunks, dan menyimpannya ke vector database.
                </p>
            </div>
            """)

            # How it works
            gr.HTML("""
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 12px; margin-bottom: 24px;">
                <div style="background: white; border-radius: 12px; padding: 16px; text-align: center; border: 1px solid #e2e8f0;">
                    <div style="font-size: 24px; margin-bottom: 8px;">📄</div>
                    <div style="font-size: 12px; font-weight: 600; color: #334155;">1. Upload</div>
                    <div style="font-size: 11px; color: #94a3b8;">PDF, DOCX, TXT</div>
                </div>
                <div style="background: white; border-radius: 12px; padding: 16px; text-align: center; border: 1px solid #e2e8f0;">
                    <div style="font-size: 24px; margin-bottom: 8px;">✂️</div>
                    <div style="font-size: 12px; font-weight: 600; color: #334155;">2. Chunking</div>
                    <div style="font-size: 11px; color: #94a3b8;">Pecah teks</div>
                </div>
                <div style="background: white; border-radius: 12px; padding: 16px; text-align: center; border: 1px solid #e2e8f0;">
                    <div style="font-size: 24px; margin-bottom: 8px;">🧠</div>
                    <div style="font-size: 12px; font-weight: 600; color: #334155;">3. Embedding</div>
                    <div style="font-size: 11px; color: #94a3b8;">Vektor AI</div>
                </div>
                <div style="background: white; border-radius: 12px; padding: 16px; text-align: center; border: 1px solid #e2e8f0;">
                    <div style="font-size: 24px; margin-bottom: 8px;">💾</div>
                    <div style="font-size: 12px; font-weight: 600; color: #334155;">4. Simpan</div>
                    <div style="font-size: 11px; color: #94a3b8;">ChromaDB</div>
                </div>
            </div>
            """)

            file_upload = gr.File(
                file_count="multiple",
                file_types=[".pdf", ".docx", ".txt"],
                label="Drag & drop file SOP di sini",
                type="filepath",
                height=180,
            )

            upload_btn = gr.Button(
                "🚀 Proses & Simpan ke Database",
                variant="primary",
                size="lg",
            )

            upload_output = gr.HTML(label="Status")
            upload_btn.click(process_and_store, inputs=[file_upload], outputs=[upload_output])

        # ======== TAB 3: DATABASE ========
        with gr.TabItem("📊 Database", id="database"):
            gr.HTML("""
            <div style="margin-bottom: 20px;">
                <h2 style="margin: 0 0 8px 0; color: #1e293b; font-weight: 700; font-size: 22px;">
                    📊 Kelola Database
                </h2>
                <p style="margin: 0; color: #64748b; font-size: 14px;">
                    Lihat statistik dan kelola dokumen yang tersimpan di vector database.
                </p>
            </div>
            """)

            with gr.Row():
                stats_btn = gr.Button("🔄 Refresh Statistik", variant="secondary", size="lg")
                clear_btn = gr.Button("🗑️ Kosongkan Database", variant="stop", size="lg")

            db_output = gr.HTML()
            stats_btn.click(get_db_stats, outputs=[db_output])
            clear_btn.click(clear_database, outputs=[db_output])

    # FOOTER
    gr.HTML("""
    <div class="app-footer">
        <p>Built with ❤️ using <strong>ChromaDB</strong> · <strong>DeepSeek</strong> · <strong>Multilingual E5</strong> · <strong>Gradio</strong></p>
    </div>
    """)

# Launch
demo.launch()
