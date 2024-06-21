import pymysql

# 连接参数
mysql_server_ip = "127.0.0.1"
mysql_port = 3306  # 默认端口
mysql_database = "dgxt"
mysql_user = "root"
mysql_password = "16816899abc!!"

# 创建连接
connection = pymysql.connect(
    host=mysql_server_ip,
    port=mysql_port,
    user=mysql_user,
    password=mysql_password,
    db=mysql_database,
    charset='utf8mb4',  # 设置字符集，可根据实际情况调整
)

try:
    with connection.cursor() as cursor:

        # SQL 插入语句
        insert_query = """
            INSERT INTO dgxt (num, jh) VALUES (%s, %s)
        """

        # 构建插入数据列表
        insert_data = [(num, 0) for num in range(1, 54)]

        # 执行批量插入
        cursor.executemany(insert_query, insert_data)

    # 提交事务
    connection.commit()

except Exception as e:
    print(f"An error occurred: {e}")
    # 如果发生错误，回滚事务
    connection.rollback()

finally:
    # 关闭连接
    connection.close()