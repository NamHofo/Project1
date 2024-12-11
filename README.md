# Phân Tích Dữ Liệu Tuyển Dụng

## Dự án này giúp phân tích dữ liệu tuyển dụng từ file CSV, chuẩn hóa dữ liệu, tính toán mức lương trung bình, và trực quan hóa kết quả thông qua biểu đồ. Dự án bao gồm các chức năng chính như:

## Chuẩn hóa dữ liệu lương và địa chỉ.
Xử lý dữ liệu thiếu và lỗi.
Tải dữ liệu vào cơ sở dữ liệu MySQL.
Vẽ biểu đồ minh họa thông tin như:
Top 10 mức lương trung bình theo vị trí.
Bản đồ nhiệt phân bố việc làm theo khu vực.
Xu hướng công nghệ theo thời gian.

## Tính năng chính
Chuẩn hóa cột lương (salary) để tạo ra các cột min_salary, max_salary, và salary_unit.
Tách địa chỉ thành district và city.
Chuẩn hóa tiêu đề công việc (job_title) thành các nhóm như Developer, Analyst, Manager, v.v.
Tính toán mức lương trung bình cho từng vị trí công việc.
Tải dữ liệu đã xử lý vào cơ sở dữ liệu MySQL.
Vẽ các biểu đồ trực quan như:
Biểu đồ cột: Mức lương trung bình theo vị trí công việc.
Heatmap: Phân bố công việc theo khu vực.
Biểu đồ đường: Xu hướng công nghệ theo thời gian.

## Cài đặt và Chạy dự án
Yêu cầu hệ thống
Python 3.10+
MySQL Database
Thư viện Python: pandas, numpy, matplotlib, seaborn, sqlalchemy, pymysql
Cài đặt thư viện
Cài đặt các thư viện cần thiết từ file requirements.txt:
pip install -r requirements.txt
Cấu hình cơ sở dữ liệu
Tạo một cơ sở dữ liệu MySQL và thêm thông tin cấu hình vào biến môi trường\n
export DB_HOST='your_mysql_host'

export DB_PORT='your_mysql_port'

export DB_NAME='your_database_name'

export DB_USER='your_username'

export DB_PASS='your_password'

## Chạy chương trình
Đặt file dữ liệu data.csv vào cùng thư mục với file code.
Chạy chương trình:

## Cấu trúc dữ liệu
Dự án xử lý file CSV với các cột sau:

job_title: Tiêu đề công việc.

company: Tên công ty.

salary: Mức lương hiển thị.

address: Địa chỉ công việc.

created_date: Ngày tạo.

link_description: Link mô tả công việc.

Sau khi chuẩn hóa, dữ liệu sẽ bao gồm thêm:
min_salary và max_salary: Mức lương tối thiểu và tối đa.

salary_unit: Đơn vị tiền tệ (VND hoặc USD).

district và city: Khu vực và thành phố.

normalized_job_title: Tiêu đề công việc đã được chuẩn hóa.

avg_salary: Mức lương trung bình.


## Trực quan hóa dữ liệu
1. Mức lương trung bình theo vị trí
Biểu đồ thanh hiển thị Top 10 vị trí công việc có mức lương trung bình cao nhất.
2. Phân bố công việc theo khu vực
Heatmap thể hiện số lượng việc làm theo khu vực (district) và thành phố (city).
3. Xu hướng công nghệ theo thời gian
Biểu đồ đường thể hiện xu hướng các công việc thuộc nhóm công nghệ theo thời gian

## Xử lý lỗi (Error Handling)
Chương trình đã bao gồm các bước xử lý lỗi:

Kiểm tra file CSV có tồn tại hay không.
Kiểm tra dữ liệu có chứa giá trị thiếu hoặc null.
Đảm bảo các cột quan trọng như min_salary, max_salary, normalized_job_title tồn tại.
Xử lý các lỗi khi tính toán lương trung bình hoặc kết nối cơ sở dữ liệu..

## Công nghệ sử dụng
Ngôn ngữ lập trình: Python
Thư viện: Pandas, NumPy, Matplotlib, Seaborn, SQLAlchemy
Cơ sở dữ liệu: MySQL
