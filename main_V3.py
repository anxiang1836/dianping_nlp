"""
main_V3：此版本的功能为:
    将重新进行整理过后的分词结果作为输入，加载word2vec，而后进行相似度计算

@Author by MaxMa 2019.05.27
"""
import gc

import caculate
import preprocess
import set_log

from excel_operate import excel_write as ew

if __name__ == '__main__':
    log = set_log.setting_log()
    # 店铺词谱
    store_dict = {}

    city_name = input("城市名称（拼音）:")
    trading_area = input("商圈名称（中文）:")
    threshold = input("相似度阈值：")

    # 4. 从数据库中读取两家店之间的相似度
    process = preprocess.DataPreProcess(cityname=city_name, trading_area=trading_area)
    similarity_list = process.select_similar_data()
    log.info('读取店铺间相似度完成！')

    # 5. 构建店铺的竞争关系(是HashMap存储的，key为店铺Url，Value为该店的竞争对手)
    global_opponent_net = caculate.restore_similar_dict_by_threshold(threshold=float(threshold),
                                                                     similar_list=similarity_list)
    # del similarity_list
    # gc.collect()
    log.info('店铺间竞争关系计算完成！')

    # 7.读取该商圈的detail数据
    detail_data_dic = {}
    # try:
    data = process.select_detail_data()
    for row in data:
        temp_list = []
        # 2.0. 读取数据库2个字段
        url = str(row[0])
        renjun = []  # 5个月的人均
        for i in range(1, 7):
            renjun.append(row[i])
        kouwei = []  # 5个月的口味
        for i in range(7, 13):
            kouwei.append(row[i])
        fuwu = []  # 5个月的服务
        for i in range(13, 19):
            fuwu.append(row[i])
        huanjing = []  # 5个月的环境
        for i in range(19, 25):
            huanjing.append(row[i])
        dianpingshu = []  # 5个月的点评数
        for i in range(25, 31):
            dianpingshu.append(row[i])
        dianpingpingfen = []  # 5个月的点评评分
        for i in range(31, 37):
            dianpingpingfen.append(row[i])
        caixi = str(row[37])

        temp_list.append(renjun)
        temp_list.append(kouwei)
        temp_list.append(fuwu)
        temp_list.append(huanjing)
        temp_list.append(dianpingshu)
        temp_list.append(dianpingpingfen)
        temp_list.append(caixi)
        detail_data_dic[url] = temp_list
    # except Exception as e:
    #    log.error(e)
    del process
    gc.collect()

    for month in range(6, 10):
        # 8. 判定在位企业还是新进入企业
        existed_stores, new_stores = caculate.judge_existed_or_new(detail_data_dic, month)

        # excel = ew.WriteExcel(file_name=city_name + trading_area + str(month) + '新进入企业')
        # excel.write_list(new_stores)

        # excel = ew.WriteExcel(file_name=city_name + trading_area + str(month) + '在位企业')
        # excel.write_list(existed_stores)
        # 9. 获取当月的竞争关系网络
        new_net_of_existed, new_net_of_new = caculate.get_current_competition_net(global_opponent_net, existed_stores,
                                                                                  new_stores)

        # 10. 获取上个月的在位企业网络规模
        scale_of_existed = caculate.get_late_month_scale(new_net_of_existed, new_stores)

        # 11. 获取新进入企业进入方式
        type_of_new_entrance = caculate.type_of_entrace(new_net_of_new, existed_stores, detail_data_dic, month)

        # 12. 整合在位企业的相关指标，做汇总表
        result_table = caculate.result_table_of_existed(new_net_of_existed, type_of_new_entrance,
                                                        scale_of_existed, detail_data_dic, month)

        # 13.将结果输出为excel
        excel = ew.WriteExcel(file_name=city_name + str(threshold) + trading_area + str(month) + '月_结果表')
        excel.write_final_result(result_table)
        log.info('最终结果表写入完成！')
