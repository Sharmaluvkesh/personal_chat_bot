import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs("report_diagrams", exist_ok=True)

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']

# 1. UI Screenshot 1: Active RAG Chat Window with Citations
def draw_chat_ui_screenshot():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)

    win_bg = patches.Rectangle((0.2, 0.2), 9.6, 6.6, facecolor='#0f172a', edgecolor='#38bdf8', lw=2)
    ax.add_patch(win_bg)

    hdr_bg = patches.Rectangle((0.2, 6.1), 9.6, 0.7, facecolor='#1e293b', edgecolor='#334155', lw=1)
    ax.add_patch(hdr_bg)
    ax.text(0.6, 6.45, "Ask AI Luvkesh - Personal RAG Ambassador", color='#f8fafc', fontsize=11, fontweight='bold', va='center')
    ax.text(9.4, 6.45, "Server Online | Groq Llama-3.3", color='#38bdf8', fontsize=9, ha='right', va='center')

    usr_bg = patches.Rectangle((2.8, 5.0), 6.8, 0.8, facecolor='#312e81', edgecolor='#6366f1', lw=1.2)
    ax.add_patch(usr_bg)
    ax.text(9.4, 5.4, "User: What are Luvkesh's top technical skills and recent project achievements?", color='#ffffff', fontsize=8.5, ha='right', va='center')

    bot_bg = patches.Rectangle((0.4, 2.0), 9.2, 2.7, facecolor='#1e293b', edgecolor='#475569', lw=1.2)
    ax.add_patch(bot_bg)
    bot_text = (
        "AI Luvkesh:\n"
        "Luvkesh Sharma is a B.Tech Computer Science student at BPIT (Enrollment: 11720802724) specializing in:\n"
        "• Core Skills: C++, Python, Data Structures, Algorithms, RAG Systems, FastAPI, React.js.\n"
        "• Key Achievements: Finalist in EY Techathon 5.0 Grand Finale and Smart Delhi Ideathon.\n"
        "• Key Projects: Personal RAG Chatbot v2.0 (sliding window PDF parsing, multi-file memory retention).\n\n"
        "Verified Source Citations:\n"
        "  1. luvkesh resume.pdf (Page 1) -> 'Driven B.Tech Computer Science student at BPIT with 97% academic record...'\n"
        "  2. projects.md (Page 1) -> 'Personal RAG Chatbot System built using SentenceTransformers & FAISS...'"
    )
    ax.text(0.6, 3.35, bot_text, color='#e2e8f0', fontsize=8.5, va='center')

    inp_bg = patches.Rectangle((0.4, 0.4), 8.0, 0.6, facecolor='#090d16', edgecolor='#334155', lw=1)
    ax.add_patch(inp_bg)
    ax.text(0.6, 0.7, "Ask anything about Luvkesh (skills, projects, experience)...", color='#64748b', fontsize=9, va='center')

    btn_bg = patches.Rectangle((8.5, 0.4), 1.1, 0.6, facecolor='#4f46e5', edgecolor='#6366f1', lw=1)
    ax.add_patch(btn_bg)
    ax.text(9.05, 0.7, "Send ->", color='#ffffff', fontsize=9, fontweight='bold', ha='center', va='center')

    plt.tight_layout()
    plt.savefig("report_diagrams/ui_screenshot_chat.png", bbox_inches='tight')
    plt.close()

# 2. UI Screenshot 2: Knowledge Manager Admin Modal
def draw_km_ui_screenshot():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)

    win_bg = patches.Rectangle((0.5, 0.3), 9.0, 5.4, facecolor='#0f172a', edgecolor='#c084fc', lw=2)
    ax.add_patch(win_bg)

    ax.text(5.0, 5.3, "Knowledge Store & Document Manager", color='#f8fafc', fontsize=12, fontweight='bold', ha='center')

    doc_bg = patches.Rectangle((0.8, 2.5), 8.4, 2.4, facecolor='#1e293b', edgecolor='#334155', lw=1)
    ax.add_patch(doc_bg)
    ax.text(1.0, 4.6, "Active Knowledge Base Documents (4 Files Loaded):", color='#38bdf8', fontsize=9.5, fontweight='bold')
    
    docs_info = (
        "• luvkesh resume.pdf  | Size: 45 KB | Total Chunks: 6  | Status: Indexed & Active\n"
        "• bio.txt            | Size: 1.2 KB | Total Chunks: 2  | Status: Indexed & Active\n"
        "• projects.md       | Size: 3.4 KB | Total Chunks: 3  | Status: Indexed & Active\n"
        "• faq.md            | Size: 2.1 KB | Total Chunks: 3  | Status: Indexed & Active"
    )
    ax.text(1.0, 3.5, docs_info, color='#cbd5e1', fontsize=8.5)

    up_bg = patches.Rectangle((0.8, 0.6), 8.4, 1.6, facecolor='#090d16', edgecolor='#818cf8', lw=1.2, linestyle='--')
    ax.add_patch(up_bg)
    ax.text(5.0, 1.4, "Drag and Drop PDF / TXT / MD Resume Documents Here", color='#a5b4fc', fontsize=10, fontweight='bold', ha='center')
    ax.text(5.0, 0.9, "Supports Multi-File Indexing with Automatic Sliding Window Chunk Normalization", color='#64748b', fontsize=8.5, ha='center')

    plt.tight_layout()
    plt.savefig("report_diagrams/ui_screenshot_knowledge_manager.png", bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    draw_chat_ui_screenshot()
    draw_km_ui_screenshot()
    print("UI Screenshots generated in 'report_diagrams/' directory!")
