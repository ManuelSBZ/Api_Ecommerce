# SQLALCHEMY_DATABASE_URI="mysql+pymysql://msb:qwe@localhost/db_8?charset=utf8mb4"
# SQLALCHEMY_DATABASE_URI="postgres+psycopg2://postgres:redsony10@localhost/db_8"
import os
SQLALCHEMY_DATABASE_URI=os.getenv("SQLALCHEMY_DATABASE_URI")
print(SQLALCHEMY_DATABASE_URI)
SECRET_KEY="SECRET_KEY_RIGHT_NOW"
DEBUG=True
SQLALCHEMY_TRACK_MODIFICATIONS=False
