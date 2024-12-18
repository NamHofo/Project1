
import os
from sqlalchemy import create_engine

# Đọc thông tin DB từ biến môi trường
mysql_host = os.getenv('DB_HOST')
mysql_port = os.getenv('DB_PORT')
mysql_database = os.getenv('DB_NAME')
mysql_user = os.getenv('DB_USER')
mysql_password = os.getenv('DB_PASS')