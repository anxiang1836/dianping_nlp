import pymysql


class DBConnect:
    def __init__(self, usr_ip='localhost', usr_port=3306, usr_name='root', usr_psd='12345678', charset='utf8',
                 db_name='TESTDB'):
        self.ip = usr_ip
        self.port = usr_port
        self.name = usr_name
        self.password = usr_psd
        self.charset = charset
        self.db_name = db_name
        # 与MySql服务器建立连接
        self.connection = pymysql.connect(host=self.ip, port=self.port, user=self.name, passwd=self.password,
                                          db=self.db_name,
                                          charset=self.charset)
        self.cursor = self.connection.cursor()

    # 与mysql断开连接
    def disconnect(self):
        self.connection.close()

    # 执行查询sql语句
    def run_select_sql(self, sql_statement):
        self.cursor.execute(sql_statement)
        return self.cursor.fetchall()


    # 执行建表sql语句
    def run_create_sql(self, sql_statement):
        self.cursor.execute(sql_statement)
