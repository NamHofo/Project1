# Sử dụng image Python
FROM python:3.10

# Đặt thư mục làm việc trong container
WORKDIR /app

# Sao chép file vào container
COPY . /app

# Cài đặt các thư viện
RUN pip install --no-cache-dir -r requirements.txt

# Chạy chương trình
CMD ["python", "main.py"]
