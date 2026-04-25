from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from api.chatbot_logic import get_camau_tour_response

# Khởi tạo ứng dụng FastAPI
app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")

# Cho phép Frontend gọi API (Đã nâng cấp Bảo mật cho Production và Local)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://huongdanvienaocamau.io.vn",
        "https://www.huongdanvienaocamau.io.vn",
        "http://localhost:8000", 
        "http://127.0.0.1:8000",
        "http://127.0.0.1:5500", # Cho phép Live Server của VS Code
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cấu trúc dữ liệu nhận từ Frontend
class ChatRequest(BaseModel):
    message: str
    language: str = "vi"  # Thêm trường language để nhận ngôn ngữ từ giao diện

# Điểm cuối trang chủ (Tránh lỗi 404 khi người dùng mở thẳng link API)
@app.get("/")
async def root():
    return {
        "message": "API Backend Cà Mau Guide đang hoạt động tốt. Vui lòng sử dụng giao diện (Frontend) để tương tác với Chatbot."
    }

# Điểm cuối (Endpoint) chính của Chatbot
@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    # Gọi hàm xử lý AI từ file chatbot_logic.py
    ai_response = get_camau_tour_response(request.message, request.language)
    return {"response": ai_response}

# Điểm cuối để kiểm tra xem server có hoạt động không
@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "Backend Hướng dẫn viên Cà Mau đang chạy tốt!"}