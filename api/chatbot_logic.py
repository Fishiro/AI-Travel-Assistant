import os, json, numpy as np, faiss, voyageai
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Khởi tạo client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
vo_client = voyageai.Client(api_key=os.getenv("VOYAGE_API_KEY"))

# Load FAISS index và metadata (chỉ chạy 1 lần khi module được import)
FAISS_PATH = os.path.join(os.path.dirname(__file__), "data", "camau.faiss")
JSON_PATH = os.path.join(os.path.dirname(__file__), "data", "camau_data.json")

if not os.path.exists(FAISS_PATH):
    raise FileNotFoundError(f"Không tìm thấy {FAISS_PATH}")
if not os.path.exists(JSON_PATH):
    raise FileNotFoundError(f"Không tìm thấy {JSON_PATH}")

index = faiss.read_index(FAISS_PATH)
with open(JSON_PATH, 'r', encoding='utf-8') as f:
    documents = json.load(f)
print(f"✅ Đã tải FAISS index: {index.ntotal} vectors, {len(documents)} đoạn văn bản.")

def get_system_prompt(language: str) -> str:
    if language == "en":
        return """You are "Ca Mau Guide", a professional, enthusiastic, and highly knowledgeable tour guide specializing in Ca Mau province, Vietnam.
Your mission is to advise on itineraries, local cuisine, attractions, and local culture.
- Always answer in English, be friendly, concise within 350 tokens, and helpful.
- Use Markdown to format your answers (bold key points, bullet points).
- Answer STRICTLY based on the provided context. If context lacks information, say you don't know and suggest asking another question about Ca Mau.
- Keep responses focused, no rambling."""
    else:
        return """Bạn là "Cà Mau Guide", hướng dẫn viên du lịch chuyên nghiệp, am hiểu tường tận về tỉnh Cà Mau.
Nhiệm vụ của bạn là tư vấn lịch trình, ẩm thực, địa điểm và văn hóa địa phương.
- Luôn trả lời bằng tiếng Việt, thân thiện, ngắn gọn trong 350 token tối đa, hữu ích.
- Dùng Markdown để định dạng câu trả lời (in đậm điểm nhấn, gạch đầu dòng).
- CHỈ trả lời dựa trên ngữ cảnh được cung cấp. Nếu ngữ cảnh không có thông tin, hãy nói bạn chưa có dữ liệu và gợi ý hỏi câu khác về Cà Mau.
- Không trả lời lan man, hãy chắt lọc thông tin trọng tâm."""

def get_camau_tour_response(user_message: str, language: str = "vi") -> str:
    # 1. Tạo query embedding bằng Voyage AI
    try:
        query_embed = vo_client.embed(
            [user_message],
            model="voyage-4-lite",
            input_type="query"
        )
        query_vec = np.array(query_embed.embeddings, dtype='float32')
    except Exception as e:
        print(f"Lỗi Voyage AI: {e}")
        return "Xin lỗi, hệ thống tìm kiếm thông tin đang gặp sự cố." if language == "vi" else "Sorry, the information retrieval system is experiencing issues."

    # 2. Tìm kiếm top 1 đoạn văn bản liên quan nhất (giảm kích thước)
    k = 1
    distances, indices = index.search(query_vec, k)
    contexts = []
    for idx in indices[0]:
        if idx != -1 and idx < len(documents):
            contexts.append(documents[idx]['text'])

    # Giới hạn độ dài mỗi context để không vượt quá TPM
    MAX_CONTEXT_CHARS = 800  # khoảng 200-250 token, đảm bảo tổng prompt an toàn
    short_contexts = []
    for ctx in contexts:
        if len(ctx) > MAX_CONTEXT_CHARS:
            short_contexts.append(ctx[:MAX_CONTEXT_CHARS] + "…")
        else:
            short_contexts.append(ctx)
            
    # Xử lý chuỗi context trống theo ngôn ngữ
    if not short_contexts:
        context_str = "Không tìm thấy thông tin liên quan." if language == "vi" else "No relevant information found."
    else:
        context_str = "\n---\n".join(short_contexts)

    # 3. Tạo prompt hoàn chỉnh
    system_prompt = get_system_prompt(language)
    
    # Điều chỉnh User Prompt theo ngôn ngữ
    if language == "en":
        user_prompt = f"""Reference context:
{context_str}

Tourist's question: {user_message}
Please answer based on the context above."""
    else:
        user_prompt = f"""Ngữ cảnh tham khảo:
{context_str}

Câu hỏi của du khách: {user_message}
Hãy trả lời dựa trên ngữ cảnh trên."""

    # 4. Gọi Groq
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.4,
            max_tokens=350,
            top_p=0.9,
            frequency_penalty=0.1,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        error_msg = str(e)
        # Xử lý lỗi vượt giới hạn token
        if "413" in error_msg or "rate_limit_exceeded" in error_msg:
            print(f"Lỗi Groq (rate limit): {e}")
            if language == "vi":
                return "Xin lỗi, câu hỏi của bạn cần quá nhiều thông tin. Vui lòng hỏi ngắn gọn hơn hoặc thử lại sau ít phút."
            else:
                return "Sorry, your question requires too much data. Please ask more concisely or try again later."
        else:
            print(f"Lỗi Groq: {e}")
            if language == "vi":
                return "Xin lỗi, trợ lý đang tạm thời bận. Vui lòng thử lại sau."
            else:
                return "Sorry, the assistant is temporarily busy. Please try again later."