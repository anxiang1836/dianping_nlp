"""
main_V1：此版本的功能为，将爬取的数据，除掉非中文，然后进行分词，并存入到excel中

@Author by MaxMa 2019.05.20
"""

from db_connect import connection
from nlp_processing import dish2word as d2w
from nlp_processing import pure_dishes as pd
from excel_operate import excel_write as ew
import set_log

log = set_log.setting_log()

if __name__ == '__main__':
    # 店铺词谱
    store_dict = {}

    city_name = input("城市名称（拼音）:")
    trading_area = input("商圈名称（中文）:")

    # 0.创建sql连接
    db = connection.DBConnect(db_name='TuiJianCai')
    # 1.执行sql语句
    sql_statement = 'SELECT DISTINCT PageUrl,菜名 from ' + city_name + trading_area + ' where 菜名 is not null'
    data = db.run_select_sql(sql_statement)
    # 2.读取数据
    try:
        for row in data:
            dish_list = []  # 菜品列表

            # 2.0. 读取数据库2个字段
            url = str(row[0])
            dish_name = str(row[1])
            # 2.1. 菜名降噪，删除非中文字符
            pending = pd.PureName(name=dish_name)
            new_name = pending.del_not_chinese()
            # 2.2. 存入dict中
            if url in store_dict.keys():
                dish_list = store_dict.get(url)
                dish_list.append(new_name)
                store_dict[url] = dish_list
            else:
                dish_list.append(new_name)
                store_dict[url] = dish_list

    except Exception as e:
        print(e)
    # 3.释放sql连接
    db.disconnect()
    log.info('1.数据库读取完成！')

    # 4.0 加载词典
    cut_process = d2w.CutWord()
    new_dict = cut_process.dict2words_dict(store_dict)
    log.info('2.菜品分词完成！')

    # 5. 将结果写入到excel
    excel = ew.WriteExcel(file_name=city_name + trading_area + '_分词')
    excel.write_dish_words(new_dict)

    log.info('3.写入到excel完成！')
