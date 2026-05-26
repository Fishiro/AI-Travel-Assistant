# 🦀 Cà Mau AI Tour Guide

**Trợ lý ảo du lịch Cà Mau** - Hỏi đáp thông minh về địa điểm, ẩm thực, văn hóa tỉnh Cà Mau bằng Tiếng Việt và Tiếng Anh, sử dụng công nghệ RAG (Retrieval-Augmented Generation) hoàn toàn miễn phí.

🌐 **Website:** [huongdanvienaocamau.io.vn](https://huongdanvienaocamau.io.vn)

---

## 🧠 Kiến trúc hệ thống

| Thành phần | Công nghệ | Nhiệm vụ |
|-----------|----------|----------|
| **Bộ não (LLM)** | [Groq Cloud](https://groq.com) (Llama 3.1 8B) | Sinh câu trả lời tự nhiên từ ngữ cảnh |
| **Tìm kiếm tri thức** | [FAISS](https://github.com/facebookresearch/faiss) (chạy trên backend) | Lưu trữ và truy xuất vector ngữ nghĩa |
| **Embedding** | [Voyage AI](https://www.voyageai.com) (`voyage-4-lite`) | Chuyển văn bản thành vector 1024 chiều |
| **Backend API** | [FastAPI](https://fastapi.tiangolo.com) + [Render](https://render.com) | Xử lý logic RAG, gọi các API AI |
| **Frontend** | HTML/CSS/JS + [Tailwind CSS](https://tailwindcss.com) + [Vercel](https://vercel.com) | Giao diện người dùng đẹp, responsive |
| **Dữ liệu** | File CSV/Excel → FAISS index + JSON | Tri thức về Cà Mau |

> Tất cả đều chạy trên các gói **miễn phí** (Render Free, Vercel Hobby, Groq Developer, Voyage AI Tier 1).

---

## 📁 Cấu trúc thư mục

```
huongdanviendulichcamau_refractor/
├── api/                        # Backend (FastAPI)
│   ├── data/                   # Dữ liệu đã index
│   │   ├── camau.faiss         # FAISS index
│   │   └── camau_data.json     # Metadata văn bản
│   ├── chatbot_logic.py        # Hàm RAG chính (embed + search + LLM)
│   ├── index.py                # Entry point cho FastAPI
│   └── __init__.py
├── public/                     # Frontend
│   ├── index.html              # Giao diện chatbot
│   └── resource/               # Ảnh, icon
├── rag_data_input/             # Dữ liệu thô (CSV/Excel)
├── faiss_d1024_maker.py        # Script tạo FAISS index
├── requirements.txt            # Thư viện Python
├── vercel.json                 # Cấu hình deploy Vercel
├── .env                        # Biến môi trường (KHÔNG commit)
└── README.md                   # File này
```

---

## 🚀 Cài đặt và chạy local

### Yêu cầu

- Python 3.10+
- [Git](https://git-scm.com/)
- Tài khoản và API key:
  - [Groq Cloud](https://console.groq.com) (lấy `GROQ_API_KEY`)
  - [Voyage AI](https://dash.voyageai.com) (lấy `VOYAGE_API_KEY`, cần thêm phương thức thanh toán để có rate limit cao hơn)

### 1. Clone repository

```bash
git clone https://github.com/Fishiro/AI-Travel-Assistant.git
cd AI-Travel-Assistant
```

### 2. Cài đặt môi trường ảo và thư viện

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Cấu hình biến môi trường

Tạo file `.env` trong thư mục gốc và thêm:

```
GROQ_API_KEY=gsk_...
VOYAGE_API_KEY=voy_...
```

### 4. Tạo FAISS index từ dữ liệu thô

```bash
python faiss_d1024_maker.py
```

File `camau.faiss` và `camau_data.json` sẽ được tạo trong `api/data/`.

### 5. Chạy backend

```bash
uvicorn api.index:app --reload --port 8000
```

Mở trình duyệt: `http://127.0.0.1:8000/api/health` → thấy `{"status":"ok"}` là thành công.

### 6. Mở frontend

Mở file `public/index.html` bằng Live Server (VS Code) hoặc trực tiếp.  
Chatbot sẽ gọi API tới `http://127.0.0.1:8000`.

---

## ☁️ Triển khai production

### Backend (Render)

1. Push code lên GitHub.
2. Trên [Render Dashboard](https://dashboard.render.com), chọn **New Web Service**.
3. Kết nối repository, chọn branch `main`.
4. Cấu hình:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn api.index:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free (512 MB RAM)
5. Thêm Environment Variables: `GROQ_API_KEY`, `VOYAGE_API_KEY`.
6. Deploy và kiểm tra `https://<tên-service>.onrender.com/api/health`.

### Frontend (Vercel)

1. Trên [Vercel](https://vercel.com), import repository.
2. Đảm bảo file `vercel.json` đã có cấu hình rewrite:
   ```json
   {
     "rewrites": [
       { "source": "/api/chat", "destination": "https://ca-mau-ai-backend.onrender.com/api/chat" },
       { "source": "/api/health", "destination": "https://ca-mau-ai-backend.onrender.com/api/health" },
       { "source": "/(.*)", "destination": "/public/$1" }
     ]
   }
   ```
3. Deploy. Truy cập domain Vercel (hoặc domain riêng) để dùng.

### Keep-alive (chống ngủ)

Dùng [UptimeRobot](https://uptimerobot.com) tạo HTTP monitor trỏ đến `https://<tên-service>.onrender.com/api/health`, ping mỗi 5 phút để backend không bị spin down.

---

## 🛠 Công nghệ chính

- **FastAPI** – Web framework Python
- **FAISS** – Vector search library (của Meta)
- **Groq** – LLM inference API (miễn phí với hạn mức cao)
- **Voyage AI** – Embedding API (200M token miễn phí)
- **Tailwind CSS** – Utility-first CSS framework
- **Marked.js** – Render Markdown sang HTML

---

## ✨ Tính năng nổi bật

- Trả lời dựa trên dữ liệu thực tế về Cà Mau (RAG)
- Giao diện đẹp, hỗ trợ Tiếng Việt và Tiếng Anh
- Tự động kiểm tra trạng thái server (chấm xanh/đỏ)
- Chống spam (giới hạn 1 câu hỏi mỗi 2 giây)
- Hỗ trợ Markdown trong câu trả lời

---

## 👨‍💻 Tác giả

**Nguyễn Dư Quí**  
Sinh viên Trường Cao Đẳng Cộng Đồng Cà Mau  
📧 [nguyenduquicm1@gmail.com](mailto:nguyenduquicm1@gmail.com)  
📞 Zalo: 0942 655 776

Dự án phi lợi nhuận, rất mong nhận được sự tài trợ để duy trì API và máy chủ.

---

## 📝 Giấy phép

Dự án mã nguồn mở theo giấy phép MIT. Vui lòng giữ tên tác giả khi sử dụng lại.

---

*Cảm ơn bạn đã ghé thăm! Chúc bạn có chuyến đi Cà Mau thật thú vị.*
