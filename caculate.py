from utils import log_config
import numpy as np

log = log_config.setting_log()


# 重新存储竞争对手关系
def restore_similar_dict_by_threshold(threshold: float, similar_list: list):
    global_opponent_net = None  # type:dict{str,list[str]}
    for row in similar_list:
        # 从相似度的表中获取三元组【店铺1，店铺2，相似度】
        store1 = str(row[0])
        store2 = str(row[1])
        similar = float(row[2])

        global_opponent_net.setdefault(store1, None)
        global_opponent_net.setdefault(store2, None)

        '''
        # 给global_opponent_net的key赋初值，并设置其value为空list
        if not global_opponent_net.keys().__contains__(store1):
            global_opponent_net[store1] = []
        if not global_opponent_net.keys().__contains__(store2):
            global_opponent_net[store2] = []
        '''

        # 按照阈值对global_opponent_net的value进行赋值
        if (similar >= threshold) and (similar != 1):

            opponent_of_store1 = []
            opponent_of_store1.extend(global_opponent_net[store1])
            opponent_of_store2 = []
            opponent_of_store2.extend(global_opponent_net[store2])

            if not opponent_of_store1.__contains__(store2):
                opponent_of_store1.append(store2)
                global_opponent_net[store1] = opponent_of_store1
            if not opponent_of_store2.__contains__(store1):
                opponent_of_store2.append(store1)
                global_opponent_net[store2] = opponent_of_store2

    return global_opponent_net


# 计算网络指标
def net_indicator(similarity_dict):
    indicator_dict = {}
    for key in similarity_dict.keys():
        scale = similarity_dict[key].__len__()  # 网络规模
        indicator_dict[key] = scale
    return indicator_dict


# 判断是否为新进入企业or在位企业
# 输入：detail表读取出来的大表数据 and 当前判定的月份
# 输出：在位企业list and 新进入企业list
def judge_existed_or_new(detail_data_dic, current_month):
    # detail_data_dic的组成是：key=PageUrl，value=[renjun,kouwei,fuwu,huanjing,dianpingshu]
    existed_stores = []
    new_stores = []
    for pageurl in detail_data_dic.keys():
        renjun = detail_data_dic[pageurl][0]
        data_in_windows = []
        data_in_windows.append(renjun[current_month - 6])
        data_in_windows.append(renjun[current_month - 5])
        data_in_windows.append(renjun[current_month - 4])
        if (not is_null(data_in_windows[0])) and (not is_null(data_in_windows[1])) and (
                not is_null(data_in_windows[2])):
            existed_stores.append(pageurl)
        elif is_null(data_in_windows[0]) and (not is_null(data_in_windows[1])) and (not is_null(data_in_windows[2])):
            new_stores.append(pageurl)
    return existed_stores, new_stores


# 判断是否为空
def is_null(uchar):
    if uchar == '' or uchar == '##' or uchar == '0':
        return True
    else:
        return False


# 获取当前月份的竞争网络
# 输入：全局竞争网络 and 在位企业list and 新进入企业list and 当前月份
# 输出：当前月份竞争网络（在位企业的，新进入企业的）
def get_current_competition_net(net, existed_stores, new_stores):
    new_net_of_existed = {}
    new_net_of_new = {}
    for store in existed_stores:
        if net.keys().__contains__(store):
            templist = []
            templist.extend(net[store])
            for x in templist:
                if (not existed_stores.__contains__(x)) and (not new_stores.__contains__(x)):
                    templist.remove(x)
            new_net_of_existed[store] = templist

    for store in new_stores:
        if net.keys().__contains__(store):
            templist = []
            templist.extend(net[store])
            for x in templist:
                if (not existed_stores.__contains__(x)) or (new_stores.__contains__(x)):
                    templist.remove(x)
            new_net_of_new[store] = templist
    return new_net_of_existed, new_net_of_new


# 计算上一个月的竞争网络网络规模
# 输入：当前月的竞争网络（在位企业的），当前月的新进入企业list
# 输出：上一个月在位企业的网络规模
def get_late_month_scale(net_of_existed, new_stores):
    opponent_of_existed = {}
    for x in net_of_existed.keys():
        templist = []
        templist.extend(net_of_existed[x])
        for t in templist:
            if new_stores.__contains__(t):
                templist.remove(t)
        opponent_of_existed[x] = templist

    return net_indicator(opponent_of_existed)


# 计算新进入企业的进入方式
# 输入：当前月的竞争网络（新进入企业的）and 在位企业 and detail数据表 and 当前月份
# detail_data_dic的组成是：key=PageUrl，value=[renjun,kouwei,fuwu,huanjing,dianpingshu]
# 输出：进入的方式，key=PageUrl，value=[价格进入，价格显现，质量进入，质量显现]
def type_of_entrace(net_of_new, existed_stores, detail_data_dic, month):
    entrace_of_new = {}
    for s in net_of_new.keys():  # s是新进入企业
        value = [0, 0, 0, 0]
        s_data = detail_data_dic[s]
        s_price = float(s_data[0][month - 5])
        s_quality = (float(s_data[1][month - 5]) + float(s_data[2][month - 5]) + float(s_data[3][month - 5])) / 3
        opponent_list = net_of_new[s]
        p_count = 0
        p_price_list = []
        p_quality_list = []
        for p in opponent_list:  # p是在位企业
            if existed_stores.__contains__(p):
                p_count += 1
                p_data = detail_data_dic[p]

                p_price = float(p_data[0][month - 5])
                p_quality = (float(p_data[1][month - 5]) + float(p_data[2][month - 5]) + float(
                    p_data[3][month - 5])) / 3
                p_price_list.append(p_price)
                p_quality_list.append(p_quality)

        if p_count != 0:
            p_avg_price = np.mean(p_price_list)
            p_avg_quality = np.mean(p_quality_list)

            # 价格显现的判定
            p_std_price = np.std(p_price_list, ddof=1)
            p_std_quality = np.std(p_quality_list, ddof=1)

            if s_price < p_avg_price:  # 价格进入
                value[0] = 1
            if s_price < p_avg_price - 1.96 * p_std_price:  # 价格显现
                value[1] = 1
            if s_quality > p_avg_quality:  # 质量进入
                value[2] = 1
            if s_quality > p_avg_quality + 1.96 * p_std_quality:  # 质量显现
                value[3] = 1
        entrace_of_new[s] = value
    return entrace_of_new


# 计算得出在位企业的相关信息数据
# 输入：当前月份的竞争网络（在位企业的） and 新进入企业的进入方式 and 在位企业上个月的网络规模 and detail数据表 and 当前月份
def result_table_of_existed(net_of_existed, entrace_of_new, scale_of_existed, detail_data_dic,
                            month):
    result_dict = {}
    for existed_store in net_of_existed.keys():
        temp_list = []
        price_entrance = 0
        quality_entrance = 0
        if net_of_existed.keys().__contains__(existed_store):
            opponent_of_existed = net_of_existed[existed_store]
            for p in opponent_of_existed:
                if entrace_of_new.keys().__contains__(p):
                    value = entrace_of_new[p]
                    if value[1] == 1:
                        price_entrance += 1
                    if value[3] == 1:
                        quality_entrance += 1
        temp_list.append(price_entrance)  # 价格进入数量
        temp_list.append(quality_entrance)  # 质量进入数量
        temp_list.append(scale_of_existed[existed_store])  # 网络规模
        detail_data = detail_data_dic[existed_store]
        for i in range(0, 6):
            temp_list.append(detail_data[i][month - 6:month - 3])
        temp_list.append(detail_data[6])
        '''
        temp_list[3] = detail_data[0][month - 6:month - 3] # 3个月的人均消费
        temp_list[4] = detail_data[1][month - 6:month - 3] # 3个月的口味
        temp_list[5] = detail_data[2][month - 6:month - 3] # 3个月的服务
        temp_list[6] = detail_data[3][month - 6:month - 3] # 3个月的环境
        temp_list[7] = detail_data[4][month - 6:month - 3] # 3个月的全部点评数
        temp_list[8] = detail_data[5][month - 6:month - 3] # 3个月的点评评分
        '''
        result_dict[existed_store] = temp_list
    return result_dict
