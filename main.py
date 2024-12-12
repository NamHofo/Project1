import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


# Kiểm tra dữ liệu hợp lệ
try:
    df = pd.read_csv('data.csv')
except pd.errors.ParserError as e:
    raise ValueError(f"Tệp {'data.csv'} không đúng định dạng: {e}")
except Exception as e:
    raise RuntimeError(f"Lỗi không mong muốn khi đọc tệp CSV: {e}")

import re

# Kiểm tra dữ liệu thiếu hoặc không hợp lệ
if df.isnull().values.any():
    raise ValueError("Dữ liệu chứa giá trị null!")



def normalize_salary(salary):

    if "thoả thuận" in salary.lower():
        return None, None, None
    

    elif "trên" in salary.lower():
        min_salary = int(re.search(r'\d+', salary).group())
        return min_salary, None, "VND"
    

    elif "tới" in salary.lower():
        max_salary = int(re.search(r'\d+', salary).group())
        return 0, max_salary, "VND"
    

    elif "-" in salary:
        match = re.findall(r'\d+', salary)
        if len(match) == 2:  # Đảm bảo có 2 số
            min_salary, max_salary = map(int, match)
            if( "$" in salary):
                return min_salary, max_salary, "USD"
            return min_salary, max_salary, "VND"
        else:
            return None, None, None 
    elif "$" in salary:
        match = re.findall(r'\d+', salary)
        if len(match) == 2:
            min_salary, max_salary = map(int, match)
            return min_salary, max_salary, "USD"
        else:
            return None, None, None  
    return None, None, None

# Áp dụng hàm chuẩn hóa
df[['min_salary', 'max_salary', 'salary_unit']] = df['salary'].apply(
    lambda x: pd.Series(normalize_salary(x))
)

def split_address(address):
    if ':' in address:
        parts = [part.strip() for part in address.split(':')]
    else:
        parts = [part.strip() for part in address.split(',')]

    if len(parts) == 1:
        return None, parts[0]

    if len(parts) == 2:
        district, city = parts[0], parts[1]
        return district, city

    return None, None



df[['district', 'city']] = df['address'].apply(lambda x: pd.Series(split_address(x)))

def normalize_job_title(job_title):
    title = job_title.lower()

    
    title = re.sub(r"(lương.*|từ \d+.*|(\d+ năm|năm kinh nghiệm).*|thu nhập từ.*|tới \d+.*|salary.*|code: \w+)", "", title, flags=re.IGNORECASE).strip()
    title = re.sub(r"[\(\)\[\]\{\}]", "", title)  
    title = re.sub(r"\s{2,}", " ", title)  

    if any(keyword in title for keyword in ["intern", "thực tập", "internship"]):
        return "Intern"
    
    if any(keyword in title for keyword in ["developer", "lập trình", "angular", "full-stack", "java", "python", "backend", "frontend"]):
        return "Developer"
    elif any(keyword in title for keyword in ["analyst", "business analyst", "data analyst", "intelligence", "ba"]):
        return "Analyst"
    elif any(keyword in title for keyword in ["support", "helpdesk", "infra", "technical support"]):
        return "IT Support"
    elif any(keyword in title for keyword in ["manager", "project manager", "product manager", "scrum", "quản lý"]):
        return "Manager"
    elif any(keyword in title for keyword in ["devops", "sre", "site reliability", "quản trị hệ thống"]):
        return "DevOps/SRE"
    elif any(keyword in title for keyword in ["secretary", "assistant"]):
        return "Secretary"
    elif any(keyword in title for keyword in ["engineer", "kỹ sư", "qa", "tester", "automation", "architect"]):
        return "Engineer"
    else:
        return "Other"


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


import os
from sqlalchemy import create_engine

# Đọc thông tin DB từ biến môi trường
mysql_host = os.getenv('DB_HOST')
mysql_port = os.getenv('DB_PORT')
mysql_database = os.getenv('DB_NAME')
mysql_user = os.getenv('DB_USER')
mysql_password = os.getenv('DB_PASS')

# Kiểm tra giá trị biến môi trường (có thể xoá trong production)
print("Database host:", mysql_host)
print("User:", mysql_user)
print("Password:", mysql_password)
print("Database name:", mysql_database)
print("Port:", mysql_port)  

# Kết nối tới cơ sở dữ liệu
engine = create_engine(f'mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}')



# Ví dụ thực hiện tải dữ liệu
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

# Vẽ biểu đồ
plt.figure(figsize=(10, 6))
salary_by_position.head(10).plot(kind='bar', color='skyblue')
plt.title('Top 10 Mức Lương Trung Bình Theo Vị Trí', fontsize=14)
plt.ylabel('Mức Lương Trung Bình', fontsize=12)
plt.xlabel('Vị Trí', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()


import seaborn as sns

# Đếm số lượng việc làm theo khu vực (district) và thành phố (city)
job_distribution = df.groupby(['city', 'district']).size().reset_index(name='job_count')

# Pivot bảng để tạo heatmap
heatmap_data = job_distribution.pivot(index='district', columns='city', values='job_count')

# Vẽ heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_data, annot=True, cmap='YlGnBu', cbar=True)
plt.title('Bản đồ nhiệt phân bố việc làm theo khu vực')
plt.xlabel('Thành phố')
plt.ylabel('Khu vực')
plt.show()

#Vẽ biểu đồ xu hướng công nghệ hot theo thời gian:
df['created_date'] = pd.to_datetime(df['created_date'])

tech_trend = df.groupby([df['created_date'].dt.to_period('M'), 'normalized_job_title']).size().reset_index(name='job_count')

tech_trend['created_date'] = tech_trend['created_date'].astype(str)

plt.figure(figsize=(14, 8))
sns.lineplot(data=tech_trend, x='created_date', y='job_count', hue='normalized_job_title', marker='o')
plt.title('Xu hướng công nghệ hot theo thời gian')
plt.xlabel('Thời gian')
plt.ylabel('Số lượng việc làm')
plt.xticks(rotation=45)
plt.legend(title='Công nghệ')
plt.show()
