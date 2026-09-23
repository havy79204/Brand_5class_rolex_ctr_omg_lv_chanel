# Brand 5-Class Luxury Authentication & Classification System

An advanced AI-powered backend system and API designed for multi-class luxury product authentication and classification (specifically targeting categories like Rolex, Cartier, Omega, Louis Vuitton, Chanel, etc.). Built with FastAPI, PyTorch, and customized computer vision toolkits.

---

## 🌟 1. Giới thiệu dự án (Project Introduction)

**Brand 5-Class** là một hệ thống backend thông minh ứng dụng Trí tuệ Nhân tạo (AI) và Thị giác máy tính (Computer Vision) nhằm tự động hóa quy trình phân loại và kiểm định hàng hiệu cao cấp (Luxury Products). 

Trong bối cảnh thị trường hàng giả ngày càng tinh vi, dự án ra đời nhằm cung cấp một giải pháp công nghệ mạnh mẽ cho các bên thứ ba, cửa hàng ký gửi hoặc nền tảng thương mại điện tử để xác thực nhanh chóng các thương hiệu đồng hồ và túi xách xa xỉ hàng đầu thế giới (như **Rolex, Cartier, Omega, Louis Vuitton, Chanel**). Hệ thống đóng vai trò như một API trung gian chịu trách nhiệm xử lý hình ảnh, trích xuất đặc trưng hình ảnh bằng các mô hình deep learning chuyên sâu và trả kết quả đánh giá độ chính xác cao.

---

## ⚙️ 2. Các tính năng chính (Key Features)

* **Multi-class Brand Classification:** Phân loại chính xác các dòng sản phẩm thuộc 5 nhóm thương hiệu lớn.
* **AI-Driven Authentication:** Sử dụng các mạng nơ-ron tiên tiến (như TResNet, Custom CLIP, YOLO backbone kết hợp PEFT/Transformers) để phát hiện các chi tiết vi mô, chất liệu và độ hoàn thiện của sản phẩm.
* **Smart Device Fallback:** Tự động nhận diện phần cứng (`CUDA` nếu có GPU NVIDIA hoặc tối ưu hóa chạy `cpu` mượt mà trên máy cá nhân không có card rời).
* **Modular Architecture:** Tách biệt rõ ràng giữa tầng API (`lux-authen-api`), tầng xử lý lõi AI (`raiki-sdk`) và các tiện ích mạng neural tùy chỉnh (`tresnet-utils-main`).

---

## 🏗️ 3. Cấu trúc thư mục dự án (Project Architecture & Structure)

```text
Brand_5class/
├── lux-authen-api/        # FastAPI backend service, routers, & endpoint handlers
├── raiki-sdk/             # Core AI pipeline, preprocessing, and model service SDK
├── tresnet-utils-main/    # Custom network layers, factory functions, & architecture utilities
├── .gitignore             # Git ignore rules
└── README.md              # Project documentation
🛠️ 4. Yêu cầu hệ thống & Chuẩn bị (Prerequisites)
Python Version: Python 3.10 (Khuyến nghị sử dụng để tương thích tốt nhất với PyTorch và các gói extension).

Package Manager: uv (Công cụ quản lý gói siêu tốc).

Các bước clone dự án về máy:
Bash
git clone [https://github.com/havy79204/Brand_5class_rolex_ctr_omg_lv_chanel.git](https://github.com/havy79204/Brand_5class_rolex_ctr_omg_lv_chanel.git)
cd Brand_5class_rolex_ctr_omg_lv_chanel
📦 5. Hướng dẫn cài đặt chi tiết (Step-by-Step Installation)
Thực hiện lần lượt các lệnh sau bên trong môi trường terminal (PowerShell trên Windows hoặc Terminal trên Linux/macOS):

Bước 1: Tạo và kích hoạt môi trường ảo (Virtual Environment)
Bash
uv venv --python 3.10 .venv
# Kích hoạt trên Windows (PowerShell):
.venv\Scripts\activate
# Kích hoạt trên Linux/macOS:
source .venv/bin/activate
Bước 2: Cài đặt công cụ biên dịch cơ bản
Bash
uv pip install --upgrade cmake
Bước 3: Cài đặt các thư viện nội bộ (Local SDKs & Utilities)
Bash
uv pip install -e ./tresnet-utils-main
uv pip install -e ./raiki-sdk
Bước 4: Cài đặt các gói phụ thuộc API chính
Bash
uv pip install -r lux-authen-api/requirements.txt
Bước 5: Cài đặt hệ sinh thái AI Model Dependencies
Bash
uv pip install "transformers>=4.56,<5" "peft==0.18.0" websockets==15.0.1 clip==0.2.0
Bước 6: Cài đặt Inplace ABN (Custom Extension)
Bash
uv pip install git+[https://github.com/mapillary/inplace_abn.git@v1.1.0](https://github.com/mapillary/inplace_abn.git@v1.1.0) --no-build-isolation
⚙️ 6. Cấu hình môi trường (Configuration)
Di chuyển vào thư mục API:

Bash
cd lux-authen-api
Tạo file cấu hình .env từ file mẫu:

Sao chép nội dung từ env.example và lưu thành file .env.

Hệ thống sẽ tự động cấu hình thiết bị chạy (device) dựa trên phần cứng thực tế của máy tính (tự động nhận diện GPU hoặc chuyển về CPU an toàn).

▶️ 7. Cách vận hành dự án (Running the Application)
Đảm bảo bạn đang ở thư mục lux-authen-api và môi trường ảo (.venv) đã được kích hoạt.

Khởi chạy máy chủ FastAPI:

Bash
python main.py
(Hoặc sử dụng lệnh Uvicorn trực tiếp: uvicorn main:app --host 0.0.0.0 --port 8000 --reload)

Kiểm tra hệ thống:

Mở trình duyệt web và truy cập vào tài liệu API tương tác (Swagger UI): http://localhost:8000/docs

Sử dụng các endpoint có sẵn để gửi ảnh sản phẩm và nhận kết quả phân loại từ mô hình AI.
