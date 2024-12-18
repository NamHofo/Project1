import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Vẽ biểu đồ

def positionGraph(df):
    plt.figure(figsize=(10, 6))
    salary_by_position = df.groupby('normalized_job_title')['avg_salary'].mean().sort_values(ascending=False)
    plt.title('Top 10 Mức Lương Trung Bình Theo Vị Trí', fontsize=14)
    plt.ylabel('Mức Lương Trung Bình', fontsize=12)
    plt.xlabel('Vị Trí', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()


def numberOfJobsByCity(df):
    job_distribution = df.groupby(['city', 'district']).size().reset_index(name='job_count')
    heatmap_data = job_distribution.pivot(index='district', columns='city', values='job_count')
    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_data, annot=True, cmap='YlGnBu', cbar=True)
    plt.title('Bản đồ nhiệt phân bố việc làm theo khu vực')
    plt.xlabel('Thành phố')
    plt.ylabel('Khu vực')
    plt.show()



#Vẽ biểu đồ xu hướng công nghệ hot theo thời gian:

def techTrend(df):
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
