import os
import json
import uuid
import glob
import re
import math
from typing import List, Dict, Any, Optional

import requests

# Try importing pypdf for PDF reading
try:
    import pypdf
    PYPDF_AVAILABLE = True
except ImportError:
    PYPDF_AVAILABLE = False

# Try importing SentenceTransformers
try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
    ST_AVAILABLE = True
except ImportError:
    ST_AVAILABLE = False

DEFAULT_GROQ_KEY = os.environ.get("GROQ_API_KEY", "")


class DocumentChunk:
    def __init__(self, content: str, source_name: str, file_type: str = "text", page_number: int = 1, fact_id: str = None):
        self.content = content
        self.source_name = source_name
        self.file_type = file_type
        self.page_number = page_number
        self.fact_id = fact_id


def normalize_pdf_text(text: str) -> str:
    """Clean up raw extracted text from PDFs by normalizing newlines and spaces."""
    if not text:
        return ""
    # Replace carriage returns
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # Replace multiple spaces
    text = re.sub(r'[ \t]+', ' ', text)
    # Restore paragraph breaks (double newlines) where single newlines occur mid-sentence
    lines = text.split("\n")
    cleaned_lines = []
    for i, line in enumerate(lines):
        line_str = line.strip()
        if not line_str:
            continue
        cleaned_lines.append(line_str)
    return "\n\n".join(cleaned_lines)


def split_text(text: str, chunk_size: int = 700, chunk_overlap: int = 150) -> List[str]:
    """Robust sliding window chunker for PDF & text documents."""
    text = normalize_pdf_text(text)
    if not text:
        return []
    
    # Split into logical blocks/paragraphs first
    paragraphs = text.split("\n\n")
    chunks = []
    current_chunk = ""

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        if len(current_chunk) + len(para) <= chunk_size:
            current_chunk += ("\n\n" if current_chunk else "") + para
        else:
            if current_chunk:
                chunks.append(current_chunk)
            if len(para) > chunk_size:
                # Sliding window split for long paragraphs
                words = para.split(" ")
                sub_chunk = ""
                for w in words:
                    if len(sub_chunk) + len(w) <= chunk_size:
                        sub_chunk += (" " if sub_chunk else "") + w
                    else:
                        chunks.append(sub_chunk)
                        # Overlap: keep last few words
                        overlap_words = sub_chunk.split(" ")[-20:]
                        sub_chunk = " ".join(overlap_words) + " " + w
                if sub_chunk:
                    current_chunk = sub_chunk
            else:
                current_chunk = para

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


class PersonalRAGEngine:
    def __init__(self, knowledge_dir: str = "knowledge_base"):
        self.knowledge_dir = knowledge_dir
        self.embedding_model = None
        self.chunks: List[DocumentChunk] = []
        self.embeddings_matrix = None
        self.documents_meta: List[Dict[str, Any]] = []
        self.custom_facts: List[Dict[str, Any]] = []

        self.load_custom_facts()
        self.build_or_load_vectorstore()

    def get_embedding_model(self):
        """Lazy load SentenceTransformer model when needed."""
        if self.embedding_model is None and ST_AVAILABLE:
            try:
                self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
                print("[RAG Engine] Loaded SentenceTransformer (all-MiniLM-L6-v2)")
            except Exception as e:
                print(f"[RAG Engine] Embedding model load error: {e}")
                self.embedding_model = None
        return self.embedding_model

    def load_custom_facts(self):
        facts_file = os.path.join(self.knowledge_dir, "custom_facts.json")
        if os.path.exists(facts_file):
            try:
                with open(facts_file, "r", encoding="utf-8") as f:
                    self.custom_facts = json.load(f)
            except Exception as e:
                print(f"[RAG Engine] Error loading custom facts: {e}")
                self.custom_facts = []

    def save_custom_facts(self):
        os.makedirs(self.knowledge_dir, exist_ok=True)
        facts_file = os.path.join(self.knowledge_dir, "custom_facts.json")
        with open(facts_file, "w", encoding="utf-8") as f:
            json.dump(self.custom_facts, f, indent=2)

    def add_custom_fact(self, question: str, answer: str, category: str = "General") -> Dict[str, Any]:
        fact = {
            "id": str(uuid.uuid4()),
            "question": question,
            "answer": answer,
            "category": category
        }
        self.custom_facts.append(fact)
        self.save_custom_facts()
        self.build_or_load_vectorstore()
        return fact

    def delete_custom_fact(self, fact_id: str) -> bool:
        initial_len = len(self.custom_facts)
        self.custom_facts = [f for f in self.custom_facts if f.get("id") != fact_id]
        if len(self.custom_facts) < initial_len:
            self.save_custom_facts()
            self.build_or_load_vectorstore()
            return True
        return False

    def load_all_chunks(self) -> List[DocumentChunk]:
        all_chunks = []
        os.makedirs(self.knowledge_dir, exist_ok=True)

        # 1. Load PDFs
        pdf_files = glob.glob(os.path.join(self.knowledge_dir, "*.pdf"))
        for pdf_path in pdf_files:
            filename = os.path.basename(pdf_path)
            if PYPDF_AVAILABLE:
                try:
                    reader = pypdf.PdfReader(pdf_path)
                    for page_num, page in enumerate(reader.pages, 1):
                        text = page.extract_text() or ""
                        page_chunks = split_text(text)
                        for c in page_chunks:
                            all_chunks.append(DocumentChunk(c, filename, "pdf", page_num))
                    print(f"[RAG Engine] Successfully parsed PDF '{filename}' with {len(reader.pages)} pages.")
                except Exception as e:
                    print(f"[RAG Engine] Error reading PDF {filename}: {e}")

        # 2. Load TXT and MD files
        text_files = glob.glob(os.path.join(self.knowledge_dir, "*.txt")) + glob.glob(os.path.join(self.knowledge_dir, "*.md"))
        for txt_path in text_files:
            filename = os.path.basename(txt_path)
            if filename == "custom_facts.json":
                continue
            try:
                with open(txt_path, "r", encoding="utf-8") as f:
                    content = f.read()
                file_chunks = split_text(content)
                for c in file_chunks:
                    all_chunks.append(DocumentChunk(c, filename, "text", 1))
            except Exception as e:
                print(f"[RAG Engine] Error reading file {filename}: {e}")

        # 3. Load Custom Facts
        for fact in self.custom_facts:
            content = f"Question: {fact['question']}\nAnswer: {fact['answer']}\nCategory: {fact.get('category', 'General')}"
            all_chunks.append(DocumentChunk(content, f"Fact: {fact['question'][:30]}", "fact", 1, fact.get("id")))

        return all_chunks

    def build_or_load_vectorstore(self):
        self.chunks = self.load_all_chunks()
        doc_names = set(c.source_name for c in self.chunks)
        
        self.documents_meta = [
            {"name": name, "chunks": sum(1 for c in self.chunks if c.source_name == name)}
            for name in doc_names
        ]
        self.embeddings_matrix = None
        print(f"[RAG Engine] Rebuilt vectorstore: {len(self.chunks)} total chunks across {len(doc_names)} documents.")

    def retrieve(self, query: str, k: int = 8) -> List[Dict[str, Any]]:
        """Retrieve top k chunks with document diversity guaranteeing newly uploaded files are included."""
        if not self.chunks:
            return []

        model = self.get_embedding_model()
        scored_results = []

        if model and ST_AVAILABLE:
            try:
                if self.embeddings_matrix is None:
                    texts = [c.content for c in self.chunks]
                    embeddings = model.encode(texts, show_progress_bar=False)
                    self.embeddings_matrix = np.array(embeddings).astype('float32')

                query_vec = model.encode([query])[0].astype('float32')
                norm_q = np.linalg.norm(query_vec)
                norm_matrix = np.linalg.norm(self.embeddings_matrix, axis=1)
                sims = np.dot(self.embeddings_matrix, query_vec) / (norm_matrix * norm_q + 1e-8)

                for idx, chunk in enumerate(self.chunks):
                    scored_results.append({
                        "content": chunk.content,
                        "source": chunk.source_name,
                        "page": chunk.page_number,
                        "file_type": chunk.file_type,
                        "score": float(sims[idx])
                    })
            except Exception as e:
                print(f"[RAG Engine] Dense search error: {e}")

        if not scored_results:
            # Fallback to BM25/Keyword Overlap search
            query_terms = set(re.findall(r'\w+', query.lower()))
            for chunk in self.chunks:
                content_lower = chunk.content.lower()
                score = sum(1 for term in query_terms if term in content_lower)
                scored_results.append({
                    "content": chunk.content,
                    "source": chunk.source_name,
                    "page": chunk.page_number,
                    "file_type": chunk.file_type,
                    "score": float(score)
                })

        # Ensure Document Diversity (include top chunk from each unique source)
        scored_results.sort(key=lambda x: x["score"], reverse=True)
        final_results = []
        seen_sources = set()

        # Step 1: Pick top scoring chunk from each unique source document
        for item in scored_results:
            if item["source"] not in seen_sources:
                seen_sources.add(item["source"])
                final_results.append(item)
            if len(final_results) >= k:
                break

        # Step 2: Fill remaining slots with remaining highest scoring chunks
        for item in scored_results:
            if item not in final_results:
                final_results.append(item)
            if len(final_results) >= k:
                break

        return final_results

    def generate_answer(self, question: str, groq_api_key: Optional[str] = None, conversation_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        retrieved_chunks = self.retrieve(question, k=8)
        
        doc_names = list(set(c['source'] for c in retrieved_chunks))
        
        context_str = "\n\n".join(
            f"--- Source: {c['source']} (Page {c['page']}) ---\n{c['content']}"
            for c in retrieved_chunks
        ) if retrieved_chunks else "No specific documents found."

        system_prompt = (
            "You are the official AI Persona & Assistant for Luvkesh Sharma.\n"
            "Your purpose is to answer questions about Luvkesh Sharma (skills, software projects, background, resume, contact info, etc.) in a warm, professional, engaging, and accurate manner.\n\n"
            f"Available Uploaded Knowledge Files in memory: {', '.join(doc_names)}\n\n"
            "Guidelines:\n"
            "1. Base your answer on the provided Context about Luvkesh Sharma below. Pay special attention to newly uploaded resume/PDF documents.\n"
            "2. If multiple files (e.g. bio.txt and a newly uploaded resume PDF) contain details, synthesize and merge the information cleanly.\n"
            "3. Speak warmly as Luvkesh's AI ambassador.\n"
            "4. Format your response cleanly using Markdown (bolding, bullet points, code snippets when relevant).\n\n"
            f"Context:\n{context_str}"
        )

        api_key = groq_api_key or os.environ.get("GROQ_API_KEY") or DEFAULT_GROQ_KEY
        answer = self.call_groq_api(system_prompt, question, api_key, conversation_history)

        if not answer:
            answer = self.fallback_answer(question, retrieved_chunks)

        citations = []
        seen = set()
        for c in retrieved_chunks:
            key = f"{c['source']}_p{c['page']}"
            if key not in seen:
                seen.add(key)
                citations.append({
                    "source": c["source"],
                    "page": c["page"],
                    "snippet": c["content"][:160] + "..." if len(c["content"]) > 160 else c["content"]
                })

        return {
            "question": question,
            "answer": answer,
            "citations": citations
        }

    def call_groq_api(self, system_prompt: str, question: str, api_key: str, history: List[Dict[str, str]] = None) -> Optional[str]:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        messages = [{"role": "system", "content": system_prompt}]
        if history:
            for item in history[-6:]:
                messages.append({"role": item.get("role", "user"), "content": item.get("content", "")})
        messages.append({"role": "user", "content": question})

        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": messages,
            "temperature": 0.3,
            "max_tokens": 1024
        }

        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=12)
            if resp.status_code == 200:
                data = resp.json()
                return data["choices"][0]["message"]["content"]
            else:
                print(f"[Groq API] HTTP {resp.status_code}: {resp.text}")
        except Exception as e:
            print(f"[Groq API] Exception calling API: {e}")

        return None

    def fallback_answer(self, question: str, chunks: List[Dict[str, Any]]) -> str:
        if not chunks:
            return "I am Luvkesh Sharma's AI Assistant! I don't have information on that specific query yet. Feel free to ask me about Luvkesh's skills, projects, background, or contact details!"

        ans = "Based on Luvkesh Sharma's knowledge base:\n\n"
        for i, c in enumerate(chunks[:3], 1):
            ans += f"**Information {i}** (from `{c['source']}`):\n{c['content']}\n\n"
        ans += "For further details or questions, feel free to reach out directly to Luvkesh!"
        return ans
