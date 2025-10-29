# 📚 Bookshop Data Platform

Dự án **Bookshop Data Platform** là một nền tảng dữ liệu mẫu được xây dựng để minh họa kiến trúc hiện đại gồm:
- **Backend API** (Python / FastAPI)
- **Frontend UI** (Vite + React)
- **Hạ tầng** điều phối bằng **Docker Compose**
- Các module mở rộng: ETL, dbt, Airflow, và Great Expectations (cho data quality)

---

## 🚀 Cách chạy nhanh với Docker

### 1. Chuẩn bị môi trường
Cài Docker và Docker Compose:
```bash
sudo apt install docker docker-compose -y
```

### 2. Tạo file cấu hình môi trường
Sao chép file mẫu:
```bash
cp bookshop-data-platform/.env.example bookshop-data-platform/.env
```
Cập nhật các giá trị cần thiết (nếu có database, MinIO, v.v.).

### 3. Chạy toàn bộ hệ thống
Từ thư mục gốc:
```bash
cd bookshop-data-platform/infrastructure
docker compose up -d --build
```

### 4. Kiểm tra dịch vụ
| Thành phần | Cổng | Mô tả |
|-------------|------|-------|
| Frontend | http://localhost:5173 | Giao diện người dùng |
| Backend | http://localhost:8000 | API chính |
| Postgres / MinIO | Theo cấu hình `.env` | Dịch vụ dữ liệu |

---

## 🧑‍💻 Cách chạy thủ công (Developer mode)

### Backend
```bash
cd bookshop-data-platform/backend
python -m venv .venv
source .venv/bin/activate  # hoặc .venv\Scripts\activate trên Windows
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd bookshop-data-platform/frontend
npm install
npm run dev
```
Sau đó mở [http://localhost:5173](http://localhost:5173).

---

## 🧱 Cấu trúc thư mục

```
bookshop-data-platform/
├── backend/              # FastAPI backend
│   ├── Dockerfile
│   └── main.py
├── frontend/             # React + Vite frontend
│   ├── Dockerfile
│   └── package.json
├── config/               # Cấu hình dữ liệu, datasource
├── infrastructure/       # Docker Compose, setup môi trường
│   └── docker-compose.yml
├── transformations/      # dbt models, ETL pipeline
├── quality/              # Great Expectations
├── orchestrations/       # Airflow DAGs
└── tools/                # Tiện ích Python (như list_config.py)
```

---

## 🧩 Ghi chú

- Khi thay đổi source code, bạn có thể rebuild Docker containers:
  ```bash
  docker compose build
  docker compose up -d
  ```
- Kiểm tra logs:
  ```bash
  docker compose logs -f
  ```

---

## 🧠 Tác giả & Ghi chú

Dự án được khởi tạo nhằm mục đích học tập và trình diễn **data platform architecture** bao gồm ingest, transform, và quality layers.
