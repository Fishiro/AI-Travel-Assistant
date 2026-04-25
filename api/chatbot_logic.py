import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load file .env ở môi trường local
load_dotenv()

# Khởi tạo client theo chuẩn SDK mới
client = genai.Client()

def get_system_prompt(language: str) -> str:
    if language == "en":
        return """You are "Ca Mau Guide", a professional, enthusiastic, and highly knowledgeable tour guide specializing in Ca Mau province, Vietnam.
Your mission is to advise on itineraries, local cuisine, attractions (Dat Mui, U Minh Ha forest, Hon Da Bac...), and local culture.
- Always answer in English, be friendly, concise, and helpful.
- Use Markdown to format your answers beautifully (bold key points, use bullet points).
- If the user asks off-topic questions, politely decline and steer the conversation back to Ca Mau tourism.
- Keep your responses strictly focused and concise. Avoid rambling to save user's time."""
    else:
        return """Bạn là "Cà Mau Guide", một hướng dẫn viên du lịch chuyên nghiệp, nhiệt tình và am hiểu tường tận về tỉnh Cà Mau, Việt Nam.
Nhiệm vụ của bạn là tư vấn lịch trình, ẩm thực (cua Cà Mau, cá thòi lòi, lẩu mắm...), địa điểm (Đất Mũi, rừng U Minh Hạ, hòn Đá Bạc...), và văn hóa địa phương.
- Luôn trả lời bằng tiếng Việt, thân thiện, ngắn gọn và hữu ích.
- Dùng Markdown để định dạng câu trả lời (in đậm điểm nhấn, dùng gạch đầu dòng).
- Nếu người dùng hỏi các vấn đề ngoài lề (không liên quan du lịch Cà Mau), hãy khéo léo từ chối và lái câu chuyện về du lịch Cà Mau.
- KHÔNG trả lời dài dòng lan man. Hãy chắt lọc thông tin trọng tâm nhất để tư vấn nhanh gọn cho du khách."""

def get_camau_tour_response(user_message: str, language: str = "vi") -> str:
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=get_system_prompt(language),
                temperature=0.7, 
                max_output_tokens=800, # GIỚI HẠN: Tối đa 800 token cho mỗi câu trả lời (chống sinh văn bản thừa)
            )
        )
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        # Báo lỗi tùy theo ngôn ngữ để UX tốt hơn
        if language == "en":
            return "Sorry, the Ca Mau tourism assistant is currently overloaded. Please try again in the next day!"
        return "Xin lỗi bạn, hiện tại trợ lý du lịch Cà Mau đang bị quá tải. Bạn vui lòng thử lại sau ngày mai nhé!"