import pymysql

# 连接数据库
db = pymysql.connect(host="localhost", user="root", password="0158", database="Test1", charset='utf8')
# 创建一个游标对象
cursor = db.cursor()
try:
    # 使用参数化查询防止 SQL 注入
    sql = "SELECT phone FROM customer WHERE username = %s"
    cursor.execute(sql, ("小张",))
    # 获取查询结果
    result = cursor.fetchone()
    if result:
        print(result[0])  # 打印查询到的 username
    else:
        print("没有找到对应的用户名")
finally:
    # 关闭游标和数据库连接
    cursor.close()
    db.close()
