"""
words2vector的主要功能是：为菜品的分词后的结果转化为vector
@Author by MaxMa 2019.05.22

"""

import gensim


class WordsDict2Vec:
    def __init__(self):
        self.model = gensim.models.Word2Vec.load(
            '/Users/maxma/Documents/nlp/word2vec_trained/baike_26g_news_13g_novel_229g.model')
        print('word2vec模型加载完成！')

    # 将词汇转化为vector
    # words_dic为-字典，key-店铺url，value-该店铺的分词后列表
    def trans2vector(self, words_dic):
        vector_dic = {}
        for key in words_dic:
            # 该店铺的分词列表
            words_list = words_dic[key]
            # 该店铺的词向量列表
            vector_list = []
            for words in words_list:
                w = self.model.wv[words]
                vector_list.append(w)
            vector_dic[key] = vector_list
        return vector_dic

    # 计算两家店之间的产品相似度
    # words_dic为-字典，key-店铺url，value-该店铺的分词后列表
    def similar_of_store(self, words_dic):
        # 总的结果列表
        similar_result_list = []
        store_list = words_dic.keys()

        # 计算第i家店和第j家店产品分词后的平均相似度
        for si in store_list:
            for sj in store_list:
                # 第i家店的产品分词列表
                store_i_word_list = []
                store_i_word_list.extend(words_dic[si])
                # 第j家店的产品分词列表
                store_j_word_list = []
                store_j_word_list.extend(words_dic[sj])

                # 用少的去和多的进行比较
                if store_j_word_list.__len__() < store_i_word_list.__len__():
                    # 交换两个list
                    exchange_list(store_i_word_list, store_j_word_list)

                sum_up = 0.0
                for w_i in store_i_word_list:
                    # 相似度分值列表
                    score_temp = {}

                    for w_j in store_j_word_list:
                        try:
                            score = self.model.similarity(w_i, w_j)
                        # 出现不存在的word2vec中不存在的词
                        except KeyError:
                            # 如果2个词完全一样
                            if str(w_i) == str(w_j):
                                score = 1.0
                            # 如果2个词不完全一样
                            else:
                                score = 0.0
                        score_temp[w_j] = score

                    # 找到score_temp中最大的相似度值
                    max_score_word = ''
                    highest_score = 0.0
                    for k in score_temp.keys():
                        if score_temp[k] > highest_score:
                            highest_score = score_temp[k]
                            max_score_word = k

                    sum_up += highest_score
                    if store_j_word_list.__contains__(max_score_word):

                        print('原始列表:', end='')
                        print(store_j_word_list, end='')
                        print('   |   要移除的数据:', end='')
                        print(max_score_word, end='')
                        print('  |  比较词为：' + w_i, end='')
                        print('  |  相似度为：', end='')
                        print(highest_score)

                        store_j_word_list.remove(max_score_word)

                average = sum_up / store_i_word_list.__len__()
                # 结果表示为:[第i家店，第j家店，产品相似度]
                temp_list = [si, sj, average]
                similar_result_list.append(temp_list)
        return similar_result_list


def exchange_list(list1, list2):
    tmp = []
    tmp.extend(list1)
    list1.clear()
    list1.extend(list2)
    list2.clear()
    list2.extend(tmp)
