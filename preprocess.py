from utils import mysql_connect, log_config

log = log_config.setting_log()


class DataPreProcess:
    def __init__(self, db_name='TuiJianCai', cityname='', trading_area=''):
        self.db_name = db_name
        self.cityname = cityname
        self.trading_area = trading_area
        self.db = mysql_connect.Connection(db_name=self.db_name)

    # 创建总的PageUrl表（包含店铺的PageUrl,菜系,经度,纬度）
    def sum_pageurl(self):
        sql_statement = 'CREATE TABLE ' + self.cityname + '_' + self.trading_area + '_PageUrl_index ' + \
                        '(SELECT DISTINCT a.PageUrl,a.`经度`,a.`维度` from (' + \
                        'SELECT PageUrl,`经度`,`维度` FROM ' + self.cityname + '_201805 WHERE `商圈` like \'' + \
                        self.trading_area + '\' UNION ' + \
                        'SELECT PageUrl,`经度`,`维度` FROM ' + self.cityname + '_201806 WHERE `商圈` like \'' + \
                        self.trading_area + '\' UNION ' + \
                        'SELECT PageUrl,`经度`,`维度` FROM ' + self.cityname + '_201807 WHERE `商圈` like \'' + \
                        self.trading_area + '\' UNION ' + \
                        'SELECT PageUrl,`经度`,`维度` FROM ' + self.cityname + '_201808 WHERE `商圈` like \'' + \
                        self.trading_area + '\' UNION ' + \
                        'SELECT PageUrl,`经度`,`维度` FROM ' + self.cityname + '_201809 WHERE `商圈` like \'' + \
                        self.trading_area + '\' UNION ' + \
                        'SELECT PageUrl,`经度`,`维度` FROM ' + self.cityname + '_201810 WHERE `商圈` like \'' + \
                        self.trading_area + '\')a)'
        try:
            self.db.run_create_sql(sql_statement)
            log.info('创建sum_PageUrl表完成！')
        except Exception as e:
            log.error('无法执行SQL语句！' + sql_statement)
            log.info(e)

    # 查询指定商圈的菜名信息（包含该店铺的PageUrl,菜名）
    def select_dishes_list(self):
        sql_statement = 'SELECT DISTINCT `商家链接`,`菜名` FROM tuijiancai_shanghai WHERE `商家链接` in ' + \
                        '(SELECT DISTINCT PageUrl FROM ' + self.cityname + '_' + self.trading_area + '_PageUrl_index'
        try:
            data = self.db.run_create_sql(sql_statement)
            return data
        except Exception as e:
            log.error('无法执行SQL语句！' + sql_statement)
            log.info(e)

    # 读取原始各月份数据
    def create_detail_data(self):
        sql_statement = 'CREATE TABLE ' + self.cityname + '_' + self.trading_area + '_detail_Data ' + \
                        '''
                        (SELECT a.PageUrl as PageUrl,
                        b.`人均消费` as `人均1`,c.`人均消费` as `人均2`,d.`人均消费` as `人均3`,
                        e.`人均消费` as `人均4`,f.`人均消费` as `人均5`,g.`人均消费` as `人均6`,
                        b.`口味` as `口味1`,c.`口味` as `口味2`,d.`口味` as `口味3`,
                        e.`口味` as `口味4`,f.`口味` as `口味5`,g.`口味` as `口味6`,
                        b.`服务` as `服务1`,c.`服务` as `服务2`,d.`服务` as `服务3`,
                        e.`服务` as `服务4`,f.`服务` as `服务5`,g.`服务` as `服务6`,
                        b.`环境` as `环境1`,c.`环境` as `环境2`,d.`环境` as `环境3`,
                        e.`环境` as `环境4`,f.`环境` as `环境5`,g.`环境` as `环境6`,
                        b.`全部点评` as `全部点评1`,c.`全部点评` as `全部点评2`,d.`全部点评` as `全部点评3`,
                        e.`全部点评` as `全部点评4`,f.`全部点评` as `全部点评5`,g.`全部点评` as `全部点评6`
                        ''' + \
                        'from ' + self.cityname + '_' + self.trading_area + '_sumPageUrl a ' + \
                        'LEFT JOIN ' + self.cityname + '_201805 b ON a.PageUrl = b.PageUrl' + \
                        'LEFT JOIN ' + self.cityname + '_201805 c ON a.PageUrl = c.PageUrl' + \
                        'LEFT JOIN ' + self.cityname + '_201805 d ON a.PageUrl = d.PageUrl' + \
                        'LEFT JOIN ' + self.cityname + '_201805 e ON a.PageUrl = e.PageUrl' + \
                        'LEFT JOIN ' + self.cityname + '_201805 f ON a.PageUrl = f.PageUrl' + \
                        'LEFT JOIN ' + self.cityname + '_201805 b ON a.PageUrl = g.PageUrl)'
        try:
            self.db.run_create_sql(sql_statement)
            log.info('创建total表完成！')
        except Exception as e:
            log.error('无法执行SQL语句！' + sql_statement)
            log.info(e)

    # 获取到店铺间的相似度表
    def select_similar_data(self):
        result_list = []
        sql_statement = 'SELECT * FROM ' + self.trading_area + '_相似度'
        try:
            data = self.db.run_select_sql(sql_statement)
            for row in data:
                temp = []
                temp.append(row[0])
                temp.append('http://www.dianping.com/shop/' + row[1])
                temp.append(row[2])
                result_list.append(temp)
        except Exception as e:
            log.error('无法执行SQL语句！' + sql_statement)
            log.info(e)
        # self.db.disconnect()
        return result_list

    # 查询detail数据表
    def select_detail_data(self):
        sql_statement = 'SELECT * FROM ' + self.cityname + '_' + self.trading_area + '_detail_Data'
        #try:
        data = self.db.run_select_sql(sql_statement)
        #except Exception as e:
            #log.error('无法执行SQL语句！' + sql_statement)
            #log.info(e)
        return data

    # 补全数据
    def fill_one_data(self, data_list):
        for index in [1, data_list.__len__() - 1]:
            # for data in data_list[1,data_list.__len__() -1]:
            # 当前数值为0或null
            if is_null_zero(data_list[index]):
                # 当前数值的前面和后面都不为空：
                if (not is_null_zero(data_list[index - 1])) and (not is_null_zero(data_list[index + 1])):
                    # 取前后值的均值
                    data_list[index] = (data_list[index - 1] + data_list[index + 1]) / 2
        return data_list

    def fill_two_data(data_list):
        # TODO 我实在是没想好这部分的程序应该怎么写
        return 0


# 补全数据
def is_null_zero(data):
    if data.__len() == 0 or data == 0:
        return True
    else:
        return False
