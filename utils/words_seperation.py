"""
主要功能：将string切分为word_list
@Author by MaxMa 2019.05.22
"""

import jieba
from typing import List, Dict


class CutWord:
    def __init__(self):
        self.version = 1.0
        self.dictionary = './jieba_dictionary/367w.dict.utf-8'

    '''
    # 加载自定义词典
    def loading_dic(self):
        # jieba.load_userdict(self.dictionary)
    '''

    # 将[菜名]分词为词列表
    @staticmethod
    def dishname_to_wordslist(dish_name: str) -> List[str]:
        words_list = jieba.cut(dish_name)
        return words_list

    # 将{店铺url-[菜名列表]}进行分词，分词为{店铺url-[词列表]}
    @staticmethod
    def storesdishes_to_wordsdict(storesdishes_dict: Dict[str, List[str]]) -> Dict[str, List[str]]:
        wordsdict = {}  # type:Dict[str, List[str]]

        for pageUrl in storesdishes_dict:
            temp_list = None  # type:list[str]
            disheslist = storesdishes_dict[pageUrl]
            for dish in disheslist:
                result = jieba.cut(dish)
                for k in result:
                    if not temp_list.__contains__(k):
                        temp_list.append(k)
            wordsdict[pageUrl] = temp_list

        return wordsdict
