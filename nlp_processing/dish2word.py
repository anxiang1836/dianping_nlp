"""
dish2word的主要功能是：为菜品
@Author by MaxMa 2019.05.22

"""

import jieba


class CutWord:
    def __init__(self):
        # 加载自定义词典
        self.version = 1.0

    '''
        # 加载自定义词典
    def loading_dic(self):
        # jieba.load_userdict('/Users/maxma/Documents/nlp/chinese_dic/dict.txt.big')
        jieba.load_userdict('/Users/maxma/Documents/nlp/chinese_dic/BigDict-master/367w.dict.utf-8')
        print('jieba词典加载完成！')
    '''

    # 将菜名列表转化为词语列表
    def dict2words_dict(self, word_dict):
        new_dict = {}

        for key in word_dict:
            temp_list = []
            pending_list = word_dict[key]
            for dish in pending_list:
                result = jieba.cut(dish)
                for k in result:
                    if not temp_list.__contains__(k):
                        temp_list.append(k)
            new_dict[key] = temp_list

        return new_dict
