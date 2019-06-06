import xlsxwriter


class WriteExcel:
    def __init__(self, file_name='demo', file_path=''):
        # 创建Excel文件，并制定文件名和路径
        self.workbook = xlsxwriter.Workbook(file_path + file_name + '.xlsx')
        # 创建新的worksheet
        self.worksheet = self.workbook.add_worksheet()

    # words_dic为-字典，key-店铺url，value-该店铺的分词后列表
    def write_dish_words(self, words_dic):
        store_urls = words_dic.keys()
        count = 0
        for s in store_urls:
            self.worksheet.write(count, 0, s)
            words_list = words_dic[s]
            temp_words = ''
            for w in words_list:
                temp_words += w + ','
            self.worksheet.write(count, 1, temp_words)
            count += 1
        self.workbook.close()

    def write_list(self,list_x):
        count = 0
        for x in list_x:
            self.worksheet.write(count,0,x)
            count += 1
        self.workbook.close()

    # 将店铺的相似度写入到excel。
    # similarity_dic中每个元素均为一个三元组，为：[店铺1，店铺2，相似度]
    def write_store_similar(self, similarity_dic):
        count = 0
        for l in similarity_dic:
            self.worksheet.write(count, 0, l[0])
            self.worksheet.write(count, 1, get_num(l[1]))
            self.worksheet.write(count, 2, l[2])
            count += 1
        self.workbook.close()

    # 将最终结果写入到excel中
    def write_final_result(self, result_table):
        title = 0
        self.worksheet.write(title, 0, 'PageUrl')
        self.worksheet.write(title, 1, '价格进入数量')
        self.worksheet.write(title, 2, '质量进入数量')
        self.worksheet.write(title, 3, '网络规模')
        self.worksheet.write(title, 4, '人均1')
        self.worksheet.write(title, 5, '人均2')
        self.worksheet.write(title, 6, '人均3')
        self.worksheet.write(title, 7, '口味1')
        self.worksheet.write(title, 8, '口味2')
        self.worksheet.write(title, 9, '口味3')
        self.worksheet.write(title, 10, '服务1')
        self.worksheet.write(title, 11, '服务2')
        self.worksheet.write(title, 12, '服务3')
        self.worksheet.write(title, 13, '环境1')
        self.worksheet.write(title, 14, '环境2')
        self.worksheet.write(title, 15, '环境3')
        self.worksheet.write(title, 16, '点评数1')
        self.worksheet.write(title, 17, '点评数2')
        self.worksheet.write(title, 18, '点评数3')
        self.worksheet.write(title, 19, '点评评分1')
        self.worksheet.write(title, 20, '点评评分2')
        self.worksheet.write(title, 21, '点评评分3')
        self.worksheet.write(title, 22, '菜系')

        content = 1
        for pageUrl in result_table.keys():
            temp_list = result_table[pageUrl]
            self.worksheet.write(content, 0, pageUrl)

            for i in range(0, 3):
                self.worksheet.write(content, i + 1, temp_list[i])

            for i in range(0, 6):
                for j in range(0, 3):
                    self.worksheet.write(content, 4 + i * 3 + j, temp_list[i + 3][j])
            self.worksheet.write(content, 22, temp_list[9])

            content += 1
        self.workbook.close()


# 只取url的数字部分
def get_num(str):
    result = ''
    for c in str:
        if c.isdigit():
            result += c
    return result
