import pymysql

# 打开数据库连接
db = pymysql.connect(
    "mysql.datahunter.cn",  # 数据库主机地址
    "test",                 # 数据库用户名
    "Dh!7Test8",            # 数据库密码
    "test",                 # 数据库名
)

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# SQL语句
sql = "SELECT * FROM lina03"

# 执行SQL语句
cursor.execute(sql)

# 获取所有记录列表
result = cursor.fetchall()

# 循环输出结果
for x in result:
    print(x[0])

# 关闭数据库连接
db.close()
