"""
main_V0：此版本的功能为，选出在某一地区的某一商圈的所有店及数据，并存入到excel中

@Author by MaxMa 2019.05.27
"""

from utils import log_config
import preprocess
from excel_operate import excel_write as ew

log = log_config.setting_log()

if __name__ == '__main__':
    # 0.从用户输入获取
    db_name = input("欲连接的数据库名（默认为TuiJianCai）: ")
    city_name = input("城市名称（拼音）:")
    trading_area = input("商圈名称（中文）:")

    # 1.生成在XX商圈的所有店铺的sumPageUrl表
    process = preprocess.DataPreProcess(db_name=db_name, cityname=city_name, trading_area=trading_area)
    process.sum_pageurl()

    # 店铺词谱
    store_dishes_dict = {}

    data = process.select_dishes_list()
    # 2.查询相应商圈的推荐菜数据
    try:
        for row in data:
            dish_list = []  # 菜品列表

            # 2.0. 读取数据库2个字段
            url = str(row[0])
            dish_name = str(row[1])

            if url in store_dishes_dict.keys():
                dish_list = store_dishes_dict.get(url)
                dish_list.append(dish_name)
                store_dishes_dict[url] = dish_list
            else:
                dish_list.append(dish_name)
                store_dishes_dict[url] = dish_list

    except Exception as e:
        print(e)
    log.info('1.数据库读取数据完成！')

    # 3. 将结果写入到excel
    excel = ew.WriteExcel(file_name=city_name + trading_area + '_菜名')
    excel.write_dish_words(store_dishes_dict)

    log.info('2.《PageUrl-菜名表》写入到excel完成！')
