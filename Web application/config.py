from dotenv import load_dotenv
import os

load_dotenv()

class Config:

    MYSQL_HOST = 'localhost'
    MYSQL_PORT = 3306
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_DB = 'anj'
    DB = 'anj.sqlite3'
    
    #https://stackoverflow.com/questions/37058567/configure-flask-mail-to-use-gmail
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD') #app password