"""
main_V2：此版本的功能为，将重新进行整理过后的分词结果作为输入，加载word2vec，而后进行相似度计算

@Author by MaxMa 2019.05.20
"""

from utils import mysql_connect
from nlp_processing import dish2word as d2w, words2vector as ws2v
from excel_operate import excel_write as ew

if __name__ == '__main__':
    # 店铺词谱
    store_dict = {}

    # 0.创建sql连接
    db = mysql_connect.Connection(db_name='TuiJianCai')
    # 1.执行sql语句
    sql_statement = 'select * from `外滩_分词修正`'
    data = db.run_select_sql(sql_statement)
    # 2.读取数据
    try:
        for row in data:
            # 2.0. 读取数据库2个字段
            url = str(row[0])
            dish_name = str(row[2])

            # 2.1. 将重新整理过后的数据读入到数据结构中
            dish_name.replace('\'', '')
            each_words_list = []
            temp_word = ''
            for uchar in dish_name:
                if uchar != ',':
                    temp_word += uchar
                else:
                    if not temp_word.isspace():
                        each_words_list.append(temp_word)
                    temp_word = ''

            '''
            # 因为最后一个词之后没有‘,’所以跳出循环后再把最后一个temp_word加入到each_words_list中
            if not temp_word.isspace():
                each_words_list.append(temp_word)
            '''

            store_dict[url] = each_words_list

    except Exception as e:
        print(e)
    # 3.释放sql连接
    db.disconnect()
    print('1.数据库读取完成！')

    '''
     # 4.0 加载词典
    cut_process = d2w.CutWord()
    # 4.1 将菜品分词
    new_dict = cut_process.dict2words_dict(store_dict)
    print('2.菜品分词完成！')
    '''

    # 5. 计算两家店之间的相似度
    ws = ws2v.WordsDict2Vec()
    # similarity_store = ws.similar_of_store(new_dict)
    similarity_list = ws.similar_of_store(store_dict)
    print('3.相似度比较完成！')

    # 6. 将结果写入excel
    excel = ew.WriteExcel(file_name='上海_外滩_店铺相似度')
    excel.write_store_similar(similarity_list)
    print('4. 店铺相似度写入excel完成！')




