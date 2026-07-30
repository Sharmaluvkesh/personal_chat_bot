import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs("report_diagrams", exist_ok=True)

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']

# 1. System Architecture Diagram
def draw_architecture_diagram():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)

    ax.text(5, 5.7, "Figure 1: Personal RAG Chatbot System Architecture", fontsize=12, fontweight='bold', ha='center')

    box_props = dict(boxstyle='round,pad=0.5', facecolor='#e8f0fe', edgecolor='#1a73e8', lw=1.5)
    accent_props = dict(boxstyle='round,pad=0.5', facecolor='#fce8e6', edgecolor='#d93025', lw=1.5)
    green_props = dict(boxstyle='round,pad=0.5', facecolor='#e6f4ea', edgecolor='#137333', lw=1.5)
    purple_props = dict(boxstyle='round,pad=0.5', facecolor='#f3e8fd', edgecolor='#8ab4f8', lw=1.5)

    ax.text(1.5, 4.2, "User Interface\n(React + Vite Web App)\n• Glassmorphic UI\n• Voice & Markdown\n• Citation Drawer", bbox=box_props, ha='center', va='center', fontsize=9)
    ax.text(5.0, 4.2, "FastAPI Backend Server\n(main.py)\n• CORS / REST API\n• File Upload Handler\n• Fact Manager", bbox=green_props, ha='center', va='center', fontsize=9)
    ax.text(8.5, 4.2, "Groq Cloud API\n(Llama-3.3-70B)\n• High-Speed LLM\n• Context Synthesis\n• Response Stream", bbox=accent_props, ha='center', va='center', fontsize=9)

    ax.text(3.2, 1.8, "RAG Engine Core\n(rag_engine.py)\n• Sliding Window Chunker\n• Text Normalizer\n• Document Sampling", bbox=purple_props, ha='center', va='center', fontsize=9)
    ax.text(6.8, 1.8, "Vector Index & Storage\n(SentenceTransformers + FAISS)\n• all-MiniLM-L6-v2\n• Dense Vector Matrix\n• Page Metadata Store", bbox=box_props, ha='center', va='center', fontsize=9)

    arrow_props = dict(arrowstyle='<->', color='#3c4043', lw=1.5)
    ax.annotate('', xy=(3.0, 4.2), xytext=(3.5, 4.2), arrowprops=arrow_props)
    ax.annotate('', xy=(6.5, 4.2), xytext=(7.0, 4.2), arrowprops=arrow_props)
    ax.annotate('', xy=(5.0, 3.4), xytext=(3.2, 2.5), arrowprops=arrow_props)
    ax.annotate('', xy=(3.2, 1.8), xytext=(5.3, 1.8), arrowprops=arrow_props)
    ax.annotate('', xy=(5.0, 3.4), xytext=(6.8, 2.5), arrowprops=arrow_props)

    plt.tight_layout()
    plt.savefig("report_diagrams/architecture_diagram.png", bbox_inches='tight')
    plt.close()

# 2. Use Case Diagram
def draw_use_case_diagram():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)

    ax.text(5, 6.6, "Figure 2: Use Case Diagram of Personal RAG Chatbot", fontsize=12, fontweight='bold', ha='center')

    rect = patches.Rectangle((2.5, 0.5), 5.5, 5.7, linewidth=1.5, edgecolor='#5f6368', facecolor='#f8f9fa')
    ax.add_patch(rect)
    ax.text(5.25, 5.9, "Personal RAG System Boundary", fontsize=10, fontweight='bold', ha='center', color='#202124')

    actor_props = dict(boxstyle='round,pad=0.5', facecolor='#e8eaed', edgecolor='#3c4043', lw=1.5)
    ax.text(1.0, 4.8, "[User]\nVisitor / Recruiter", bbox=actor_props, fontsize=9, ha='center', va='center')
    ax.text(1.0, 1.8, "[Admin]\nLuvkesh Sharma", bbox=actor_props, fontsize=9, ha='center', va='center')

    use_cases = [
        (5.25, 5.1, "UC1: Ask Questions about Luvkesh"),
        (5.25, 4.2, "UC2: View Verified Source Citations"),
        (5.25, 3.3, "UC3: Use Voice Input & Audio Readout"),
        (5.25, 2.4, "UC4: Upload Resume / PDF Documents"),
        (5.25, 1.5, "UC5: Manage Custom Facts & API Key"),
        (5.25, 0.8, "UC6: Re-index Vector Knowledge Base")
    ]

    for x, y, label in use_cases:
        ax.text(x, y, label, bbox=dict(boxstyle='round,pad=0.4', facecolor='#ffffff', edgecolor='#1a73e8', lw=1.2), fontsize=8.5, ha='center', va='center')

    arrow = dict(arrowstyle='-', color='#5f6368', lw=1.2)
    ax.annotate('', xy=(1.5, 4.8), xytext=(3.5, 5.1), arrowprops=arrow)
    ax.annotate('', xy=(1.5, 4.8), xytext=(3.5, 4.2), arrowprops=arrow)
    ax.annotate('', xy=(1.5, 4.8), xytext=(3.5, 3.3), arrowprops=arrow)

    ax.annotate('', xy=(1.5, 1.8), xytext=(3.5, 2.4), arrowprops=arrow)
    ax.annotate('', xy=(1.5, 1.8), xytext=(3.5, 1.5), arrowprops=arrow)
    ax.annotate('', xy=(1.5, 1.8), xytext=(3.5, 0.8), arrowprops=arrow)

    plt.tight_layout()
    plt.savefig("report_diagrams/use_case_diagram.png", bbox_inches='tight')
    plt.close()

# 3. Data Flow Diagram (DFD Level 1)
def draw_dfd_diagram():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)

    ax.text(5, 5.6, "Figure 3: Data Flow Diagram (DFD Level 1)", fontsize=12, fontweight='bold', ha='center')

    ax.text(0.8, 3.0, "User / Visitor", bbox=dict(boxstyle='square,pad=0.6', facecolor='#feefc3', edgecolor='#f9ab00', lw=1.5), fontsize=9, ha='center')

    p_props = dict(boxstyle='circle,pad=0.5', facecolor='#e8f0fe', edgecolor='#1a73e8', lw=1.5)
    ax.text(3.0, 4.5, "1.0\nText Normalizer\n& Chunker", bbox=p_props, fontsize=8, ha='center')
    ax.text(5.5, 4.5, "2.0\nEmbedding\nGenerator", bbox=p_props, fontsize=8, ha='center')
    ax.text(5.5, 1.8, "3.0\nSimilarity\nRanker", bbox=p_props, fontsize=8, ha='center')
    ax.text(8.2, 3.0, "4.0\nLLM Response\nSynthesizer", bbox=p_props, fontsize=8, ha='center')

    ax.text(3.0, 1.8, "D1: Knowledge Store & Vector DB\n(PDF, TXT, FAISS Index)", bbox=dict(boxstyle='round,pad=0.5', facecolor='#e6f4ea', edgecolor='#137333', lw=1.5), fontsize=8.5, ha='center')

    af = dict(arrowstyle='->', color='#202124', lw=1.2)
    ax.annotate('Query / File Upload', xy=(2.0, 4.5), xytext=(1.2, 3.3), arrowprops=af, fontsize=7.5)
    ax.annotate('Clean Chunks', xy=(4.5, 4.5), xytext=(3.8, 4.5), arrowprops=af, fontsize=7.5)
    ax.annotate('Dense Vectors', xy=(3.8, 2.0), xytext=(4.8, 4.0), arrowprops=af, fontsize=7.5)
    ax.annotate('Query Embeddings', xy=(5.5, 2.5), xytext=(5.5, 3.8), arrowprops=af, fontsize=7.5)
    ax.annotate('Top 8 Diverse Chunks', xy=(7.2, 3.0), xytext=(6.3, 1.8), arrowprops=af, fontsize=7.5)
    ax.annotate('Final Response & Citations', xy=(1.0, 2.5), xytext=(8.0, 2.2), arrowprops=dict(arrowstyle='->', color='#d93025', lw=1.2, connectionstyle="arc3,rad=-0.3"), fontsize=7.5)

    plt.tight_layout()
    plt.savefig("report_diagrams/dfd_diagram.png", bbox_inches='tight')
    plt.close()

# 4. RAG Query & Citation Generation Flowchart
def draw_flowchart_diagram():
    fig, ax = plt.subplots(figsize=(8, 9), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 10)

    ax.text(4, 9.6, "Figure 4: RAG Query Processing & Citation Flowchart", fontsize=11, fontweight='bold', ha='center')

    nodes = [
        (4, 9.0, "Start: User Inputs Query", "startend"),
        (4, 8.0, "Check Conversation History & Query String", "process"),
        (4, 7.0, "Compute SentenceTransformer Query Embedding", "process"),
        (4, 6.0, "Are Document Embeddings in Memory?", "decision"),
        (4, 5.0, "Perform Cosine Similarity Ranking across Chunks", "process"),
        (4, 4.0, "Apply Multi-Document Diversity Filter (Top 8 Chunks)", "process"),
        (4, 3.0, "Construct System Prompt with Context & Source Tags", "process"),
        (4, 2.0, "Call Groq API (llama-3.3-70b-versatile)", "process"),
        (4, 1.0, "Render Markdown Answer & Expandable Source Citations", "process"),
        (4, 0.2, "End: Display Result to User", "startend")
    ]

    for x, y, text, ntype in nodes:
        if ntype == "startend":
            bprops = dict(boxstyle='round,pad=0.5', facecolor='#fce8e6', edgecolor='#d93025', lw=1.5)
        elif ntype == "decision":
            bprops = dict(boxstyle='round,pad=0.5', facecolor='#feefc3', edgecolor='#f9ab00', lw=1.5)
        else:
            bprops = dict(boxstyle='round,pad=0.4', facecolor='#e8f0fe', edgecolor='#1a73e8', lw=1.2)
        ax.text(x, y, text, bbox=bprops, fontsize=8.5, ha='center', va='center')

    af = dict(arrowstyle='->', color='#3c4043', lw=1.3)
    y_coords = [9.0, 8.0, 7.0, 6.0, 5.0, 4.0, 3.0, 2.0, 1.0, 0.2]
    for i in range(len(y_coords) - 1):
        ax.annotate('', xy=(4, y_coords[i+1] + 0.35), xytext=(4, y_coords[i] - 0.35), arrowprops=af)

    plt.tight_layout()
    plt.savefig("report_diagrams/flowchart_diagram.png", bbox_inches='tight')
    plt.close()

# 5. Entity Relationship (ERD / Schema Diagram)
def draw_erd_diagram():
    fig, ax = plt.subplots(figsize=(9, 6), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 6)

    ax.text(4.5, 5.6, "Figure 5: Entity-Relationship & Data Schema Diagram", fontsize=11, fontweight='bold', ha='center')

    box = dict(boxstyle='round,pad=0.5', facecolor='#ffffff', edgecolor='#1a73e8', lw=1.5)

    ax.text(2.0, 4.2, "DOCUMENT\n-------------------\n• doc_id (PK)\n• filename\n• file_type\n• upload_date\n• total_chunks", bbox=box, fontsize=8, ha='center')
    ax.text(6.5, 4.2, "DOCUMENT_CHUNK\n-------------------\n• chunk_id (PK)\n• doc_id (FK)\n• page_number\n• content_text\n• vector_embedding", bbox=box, fontsize=8, ha='center')
    ax.text(2.0, 1.5, "CUSTOM_FACT\n-------------------\n• fact_id (PK)\n• question\n• answer\n• category", bbox=box, fontsize=8, ha='center')
    ax.text(6.5, 1.5, "SOURCE_CITATION\n-------------------\n• citation_id (PK)\n• source_name\n• page_number\n• snippet_text", bbox=box, fontsize=8, ha='center')

    af = dict(arrowstyle='<->', color='#5f6368', lw=1.5)
    ax.annotate('1 : N  (Contains)', xy=(4.2, 4.2), xytext=(4.3, 4.2), arrowprops=af, fontsize=8, ha='center')
    ax.annotate('1 : N  (Generates)', xy=(6.5, 2.7), xytext=(6.5, 3.0), arrowprops=af, fontsize=8, ha='center')
    ax.annotate('1 : 1  (Maps)', xy=(4.2, 1.5), xytext=(4.3, 1.5), arrowprops=af, fontsize=8, ha='center')

    plt.tight_layout()
    plt.savefig("report_diagrams/erd_diagram.png", bbox_inches='tight')
    plt.close()

# 6. Document Upload & Vector Indexing Activity Diagram
def draw_activity_diagram():
    fig, ax = plt.subplots(figsize=(8, 8), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 8)

    ax.text(4, 7.7, "Figure 6: Document Upload & Vector Indexing Activity Diagram", fontsize=11, fontweight='bold', ha='center')

    activities = [
        (4, 7.0, "User Selects PDF / Document File", "start"),
        (4, 6.0, "FastAPI /api/documents/upload Endpoint Received", "action"),
        (4, 5.0, "Is File Extension .pdf, .txt, or .md?", "decision"),
        (4, 4.0, "Extract Text & Apply normalize_pdf_text()", "action"),
        (4, 3.0, "Split Text into Chunks via Sliding Window", "action"),
        (4, 2.0, "Compute Dense Vectors using SentenceTransformers", "action"),
        (4, 1.0, "Save File to Disk & Re-index FAISS Matrix", "action"),
        (4, 0.2, "Return Success Message & Refresh UI Stats", "end")
    ]

    for x, y, text, ntype in activities:
        if ntype == "start" or ntype == "end":
            bprops = dict(boxstyle='round,pad=0.5', facecolor='#e6f4ea', edgecolor='#137333', lw=1.5)
        elif ntype == "decision":
            bprops = dict(boxstyle='round,pad=0.5', facecolor='#feefc3', edgecolor='#f9ab00', lw=1.5)
        else:
            bprops = dict(boxstyle='round,pad=0.4', facecolor='#e8f0fe', edgecolor='#1a73e8', lw=1.2)
        ax.text(x, y, text, bbox=bprops, fontsize=8.5, ha='center', va='center')

    af = dict(arrowstyle='->', color='#3c4043', lw=1.3)
    y_coords = [7.0, 6.0, 5.0, 4.0, 3.0, 2.0, 1.0, 0.2]
    for i in range(len(y_coords) - 1):
        ax.annotate('', xy=(4, y_coords[i+1] + 0.3), xytext=(4, y_coords[i] - 0.3), arrowprops=af)

    plt.tight_layout()
    plt.savefig("report_diagrams/activity_diagram.png", bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    draw_architecture_diagram()
    draw_use_case_diagram()
    draw_dfd_diagram()
    draw_flowchart_diagram()
    draw_erd_diagram()
    draw_activity_diagram()
    print("All 6 clean report diagrams generated in 'report_diagrams/' directory!")
