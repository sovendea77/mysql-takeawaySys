
import pymysql

connection = pymysql.connect(
    host='localhost',         # MySQL Workbench 中的 Hostname
    user='sovendea',          # MySQL Workbench 中的 Username
    password='sovendea', # MySQL Workbench 中的 Password
    database='appDB', # MySQL Workbench 中的 Default Schema
    port=3306                 # MySQL Workbench 中的 Port
)
