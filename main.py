import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import os
from sqlalchemy import create_engine
import re

from data_preprocessing import normalize_salary, split_address, normalize_job_title
from config import mysql_host, mysql_port, mysql_database, mysql_user, mysql_password
from visualization import positionGraph, numberOfJobsByCity, techTrend
from database import engine


# Kiểm tra dữ liệu hợp lệ
try:
    df = pd.read_csv('data.csv')
except pd.errors.ParserError as e:
    raise ValueError(f"Tệp {'data.csv'} không đúng định dạng: {e}")
except Exception as e:
    raise RuntimeError(f"Lỗi không mong muốn khi đọc tệp CSV: {e}")



# Kiểm tra dữ liệu thiếu hoặc không hợp lệ
if df.isnull().values.any():
    raise ValueError("Dữ liệu chứa giá trị null!")


# Áp dụng hàm chuẩn hóa
df[['min_salary', 'max_salary', 'salary_unit']] = df['salary'].apply(
    lambda x: pd.Series(normalize_salary(x))
)

#Them cot district va city
df[['district', 'city']] = df['address'].apply(lambda x: pd.Series(split_address(x)))

#Chuan hoa job_title
df["normalized_job_title"] = df["job_title"].apply(normalize_job_title)

# Chuyển các cột về string
string_columns = ['job_title', 'company', 'salary', 'address', 'time', 
                  'link_description', 'salary_unit', 'district', 
                  'city', 'normalized_job_title']
for col in string_columns:
    df[col] = df[col].astype('string')

# Chuyển các cột về float
float_columns = ['min_salary', 'max_salary','salary']
for col in float_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Chuyển cột 'created_date' sang datetime
df['created_date'] = pd.to_datetime(df['created_date'], errors='coerce')


#Thực hiện tải dữ liệu
try:
    df.to_sql('jobs', con=engine, if_exists='replace', index=False)
    print("Dữ liệu đã được tải thành công vào cơ sở dữ liệu.")
except Exception as e:
    print(f"Lỗi trong quá trình tải dữ liệu: {e}")
finally:
    engine.dispose()
    print("Đã đóng kết nối cơ sở dữ liệu.")

#Xây dựng Error Handling
# Kiểm tra tệp tồn tại
filepath = "data.csv"
if not os.path.exists(filepath):
    raise FileNotFoundError(f"Tệp {filepath} không tồn tại!")

# Kiểm tra nếu cột 'min_salary', 'max_salary', và 'normalized_job_title' tồn tại trong DataFrame
if 'min_salary' not in df.columns or 'max_salary' not in df.columns or 'normalized_job_title' not in df.columns:
    raise ValueError("Các cột min_salary, max_salary hoặc normalized_job_title không tồn tại trong dữ liệu.")

# Xử lý khi các giá trị lương thiếu hoặc không hợp lệ
try:
    df['avg_salary'] = (df['min_salary'] + df['max_salary']) / 2
except Exception as e:
    print(f"Đã xảy ra lỗi khi tính toán lương trung bình: {e}")
    df['avg_salary'] = None

# Kiểm tra nếu 'avg_salary' có giá trị hợp lệ
if df['avg_salary'].isnull().all():
    raise ValueError("Không có dữ liệu lương trung bình hợp lệ để vẽ biểu đồ.")


# Tính mức lương trung bình cho từng vị trí
df['avg_salary'] = (df['min_salary'] + df['max_salary']) / 2
salary_by_position = df.groupby('normalized_job_title')['avg_salary'].mean().sort_values(ascending=False)

#Ve bieu do 
positionGraph(df)

#Ve bieu do phan bo vi tri lam viec theo thanh pho
numberOfJobsByCity(df)

#Ve bieu do xu huong cong nghe hot theo thoi gian
techTrend(df)
