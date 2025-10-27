FROM python:3.10-slim

# Đặt thư mục làm việc bên trong container
WORKDIR /app

# Cài đặt các dependency hệ thống cần thiết cho Airflow và các thư viện nặng
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    libssl-dev \
    libffi-dev \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy file requirements vào container và cài đặt trước để tận dụng cache build
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ mã nguồn vào container
COPY . .

# Đặt biến môi trường giúp Python in log ngay lập tức (không buffer)
ENV PYTHONUNBUFFERED=1

# Lệnh mặc định khi container khởi động
CMD ["python", "tools/list_config.py"]
