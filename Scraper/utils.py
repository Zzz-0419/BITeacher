import os
import pypinyin
import urllib.parse

def extract_name_initials(name):
    """
    提取姓名的拼音字母
    :param name: 姓名
    """
    # 检查是否为中文名
    if all(ord(char) >= 0x4E00 and ord(char) <= 0x9FA5 for char in name):

        # 获取姓和名的拼音
        surname_pinyin = pypinyin.lazy_pinyin(name)
        
        # 拼接拼音字母
        initials = ''.join(surname_pinyin)
        
        return initials.lower()
    else:
        # 如果不是中文名,则返回原名
        return name.lower()



def get_file_path(url, school_name, directory_level=-2):
    """
    从URL中提取文件路径
    :param url: URL
    :param directory_level: 从 URL.path 的哪一级目录开始提取
    :param school_name: 学院名称
    """
    file_path = school_name
    url_path = urllib.parse.urlparse(url).path
    url_path = os.path.dirname(url_path)
    slash_indices = [i for i, c in enumerate(url_path) if c == '/']
    file_path += url_path[slash_indices[directory_level]:]
    # print(slash_indices)
    # print(file_path)
    return file_path