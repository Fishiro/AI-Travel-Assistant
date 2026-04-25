Hướng Dẫn Viên Ảo Cà Mau (Cà Mau Travel Chatbot)Dự án Chatbot AI tư vấn du lịch Cà Mau.Domain: huongdanvienaocamau.io.vnFrontend: HTML5, Tailwind CSS, Vanilla JS.Backend: Python 3.11 (FastAPI).Deployment: Vercel (Hỗ trợ Serverless Python & Static Frontend).Cấu trúc thư mục (Chuẩn Vercel Production)Để Vercel hiểu được dự án có cả Frontend tĩnh và Backend Python, chúng ta PHẢI tuân thủ cấu trúc sau:huongdanvienaocamau/
│
├── api/                    # (BẮT BUỘC) Thư mục chứa Backend Python cho Vercel
│   ├── __init__.py
│   ├── index.py            # Entry point của FastAPI (thay thế cho app.py cũ)
│   ├── core/               # Chứa cấu hình, security, API keys
│   ├── routers/            # Chia nhỏ các API (vd: chat.py, system.py)
│   └── services/           # Logic xử lý AI (kết nối Gemini/OpenAI, xử lý RAG...)
│
├── public/                 # Chứa các tài nguyên tĩnh (Hình ảnh, Font chữ, Favicon)
│   └── images/
│       └── camau-bg.jpg
│
├── index.html              # Trang chủ Frontend (Giao diện Chatbot)
├── styles.css              # File CSS tùy chỉnh (sau khi compile Tailwind)
├── app.js                  # Logic gọi API từ Frontend
│
├── vercel.json             # File cấu hình cực kỳ quan trọng để Vercel route đúng
├── requirements.txt        # Danh sách thư viện Python (fastapi, uvicorn, ...)
├── .env                    # Biến môi trường LOCAL (KHÔNG ĐƯA LÊN GITHUB)
├── .gitignore              # Các file bỏ qua khi commit git
└── README.md               # File tài liệu này
Chức năng của từng thành phần quan trọng:api/index.py: Vercel tự động tìm thư mục api để biến code Python thành Serverless APIs. Mọi request gửi đến /api/... sẽ được xử lý tại đây.index.html: Giao diện người dùng. Vercel sẽ tự động phục vụ file này ở trang chủ (/).vercel.json: Trái tim của hệ thống. Giúp "nối" domain của bạn, định tuyến (routing) requests từ Frontend sang Backend mà không bị lỗi CORS..env: Chứa API Key (như Google Gemini API, OpenAI API). Trên Vercel, chúng ta sẽ nhập tay các biến này trong Dashboard.Quy trình làm việc (Workflow)Code và test Frontend/Backend ở máy Local (máy tính của bạn).Khi mọi thứ hoạt động tốt -> git commit & git push lên GitHub.Vercel tự động nhận diện code mới trên GitHub, build lại và cập nhật lên huongdanvienaocamau.io.vn.