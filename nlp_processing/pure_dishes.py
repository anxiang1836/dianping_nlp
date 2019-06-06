"""
pure_dishes的主要功能是：为菜品进行降噪
@Author by MaxMa 2019.05.22

"""

# 判断是否为汉字
def is_chinese(char):
    if char >= '\u4e00' and char <= '\u9fa5':
        return True
    else:
        return False


# 判断字符是否非汉字，数字和英文字符
def is_other(uchar):
    if not (is_chinese(uchar) or uchar.isdigit() or uchar.isalpha()):
        return True
    else:
        return False


class PureName:
    def __init__(self, name):
        self.name = name

    # 将菜名中非中文字符剔除
    def del_not_chinese(self):
        new_name = ''
        for c in self.name:
            if is_chinese(c):
                new_name += c
            else:
                new_name += ''
        return new_name
