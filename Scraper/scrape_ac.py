import requests
from bs4 import BeautifulSoup
import urllib.parse
import json
import os
import logging
import re
from utils import extract_name_initials, get_file_path

# 目标URL
url_list = ['https://ac.bit.edu.cn/szdw/dsmd/bssds/index.htm',
            'https://ac.bit.edu.cn/szdw/dsmd/sssds/kzllykzgc/index.htm',
            'https://ac.bit.edu.cn/szdw/dsmd/sssds/dhzdykz/index.htm',
            'https://ac.bit.edu.cn/szdw/dsmd/sssds/mssbyznxt/index.htm',
            'https://ac.bit.edu.cn/szdw/dsmd/sssds/zngzyydkz/index.htm',
            'https://ac.bit.edu.cn/szdw/dsmd/sssds/znxxclykz/index.htm',
            'https://ac.bit.edu.cn/szdw/dsmd/sssds/dqgcykz/index.htm',
            'https://ac.bit.edu.cn/szdw/dsmd/qyjckxyjyds/index.htm'
            ]

def get_index():
    """
    从教师列表页面提取教师主页链接
    """
    for url in url_list:
        # 发送HTTP请求
        response = requests.get(url)
        response.encoding = 'utf-8'  # 设置编码以防止中文乱码

        # 初始化一个字典来存储数据
        data = {}

        # 创建对应文件夹
        file_path = get_file_path(url, school_name="ac", directory_level=2)
        os.makedirs(file_path, exist_ok=True)

        # 检查HTTP请求是否成功
        if response.status_code == 200:
            # 解析HTML文档
            soup = BeautifulSoup(response.text, 'html.parser')
            
                # 查找包含教师主页链接的<div>标签
            article_list = soup.find('div', class_='articleList01')
            list_title = article_list.find('div', class_='listTitle01')
            title = list_title.find('h2').text.strip()
            
            # 初始化类别列表
            data[title] = []
            
            # 查找所有<li>标签中的<a>标签
            list_items = article_list.find_all('li')
            
            # 基础URL，用于拼接相对路径
            base_url = urllib.parse.urljoin(url, '.')
            
            # 存储教师姓名和链接
            for item in list_items:
                link = item.find('a', href=True)
                if not link:
                    continue
                name = link.text.strip()
                href = link['href']
                full_url = urllib.parse.urljoin(base_url, href)
                data[title].append({"name": name, "url": full_url})
            
            # 将数据写入JSON文件
            with open(file_path+'/teachers_index.json', 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")


def scrape_teacher(url, path):
    """
    从教师主页提取信息
    :param url: 教师主页URL
    :param path: 保存文件的路径
    """
    if not os.path.exists(path):
        os.makedirs(path)
    # 发送请求并解析HTML
    response = requests.get(url)
    response.encoding = 'utf-8'
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        data = {}
        # 定位教师信息
        teacher_info = soup.find('div', class_='teacherInfo')


        # 提取姓名
        try:
            name_span = teacher_info.find('td', string=re.compile(r'姓\s*名：'))
            if name_span:
                name_elem = name_span.find_next_sibling('td').text
                if name_elem and name_elem.strip():
                    name = name_elem.strip()
                else:
                    name = None
            else:
                name = None
        except (AttributeError, TypeError):
            name = None
            logging.warning(f"Failed to extract name for a teacher")

        # 没有姓名的话就跳过
        if not name:
            logging.warning(f"Failed to extract teacher info. Skipping...")
            return

        # 提取所在学科
        try:
            subject_span = teacher_info.find('td', string=re.compile(r"学科方向：|所在学科："))
            if subject_span:
                subject_elem = subject_span.find_next_sibling('td').text
                if subject_elem and subject_elem.strip():
                    subject = subject_elem.strip()
                else:
                    subject = None
            else:
                subject = None
        except (AttributeError, TypeError):
            subject = None
            logging.warning(f"Failed to extract subject for a teacher")



        # 提取职称
        try:
            title_span = teacher_info.find('td', string=re.compile(r'职\s*称：'))
            if title_span:
                title_elem = title_span.find_next_sibling('td').text
                if title_elem and title_elem.strip():
                    title = title_elem.strip()
                else:
                    title = None
            else:
                title = None
        except (AttributeError, TypeError):
            title = None
            logging.warning(f"Failed to extract title for a teacher")

        # 提取联系电话
        try:
            phone_span = teacher_info.find('td', string=re.compile(r'联系方式：'))
            if phone_span:
                phone_elem = phone_span.find_next_sibling('td').text
                if phone_elem and phone_elem.strip():
                    phone = phone_elem.strip()
                else:
                    phone = None
            else:
                phone = None
        except (AttributeError, TypeError):
            phone = None
            logging.warning(f"Failed to extract phone for a teacher")

        # 提取邮箱
        try:
            email_span = teacher_info.find('td', string=re.compile(r'电子邮件：|E-mail\s*：'))
            if email_span:
                email_elem = email_span.find_next_sibling('td').text
                if email_elem and email_elem.strip():
                    email = email_elem.strip()
                else:
                    email = None
            else:
                email = None
        except (AttributeError, TypeError):
            email = None
            logging.warning(f"Failed to extract email for a teacher")


        # 提取通信地址
        try:
            address_span = teacher_info.find('td', string=re.compile(r'办公地点：'))
            if address_span:
                address_elem = address_span.find_next_sibling('td').text
                if address_elem and address_elem.strip():
                    address = address_elem.strip()
                else:
                    address = None
            else:
                address = None
        except (AttributeError, TypeError):
            address = None
            logging.warning(f"Failed to extract address for a teacher")

        # 下载教师头像图片
        # 提取图片URL并下载图片
        img_tag = teacher_info.find('p', class_='img').find('img')
        img_src = img_tag['src']
        if img_src and img_src.strip():
            img_url = urllib.parse.urljoin(url, img_src)
            img_name = os.path.basename(img_src)
            img_path = os.path.join(path, img_name)
            with open(img_path, "wb") as f:
                img_response = requests.get(img_url)
                f.write(img_response.content)
            print(f"图片已保存至：{img_path}")
        else:
            logging.warning(f"Failed to extract image for a teacher")

        # 将信息存储到字典中
        data['info'] = {
            'name': name,
            'subject': subject,
            'professional_title': title,
            'tel' : phone,
            'email': email,
            'address': address,
        }

        # 打印提取的信息
        print(f"姓名：{name}")
        print(f"所在学科：{subject}")
        print(f"职称：{title}")
        print(f"联系电话：{phone}")
        print(f"E-mail：{email}")
        print(f"通信地址：{address}")
        print("---")

        # 提取教师详细信息
        details = []
        con_teacher = soup.find('div', class_='con_teacher')
        for section in con_teacher.find_all('div', class_='con01_t'):
            if section.find('h3') is not None:
                title = section.find('h3').text.strip()
            content = ' '.join(p.text.strip()+'\n' for p in section.find_all('p'))
            if content.strip() == "":
                content = None
            details.append({
                'title': title,
                'content': content
            })
        data['details'] = details

        print(os.path.join(path, 'profile.json'))
        with open(os.path.join(path, 'profile.json'), 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)


def get_info():
    """
    从教师主页提取信息
    设置好传输路径
    """
    for url in url_list:
        base_path = get_file_path(url, school_name="ac",directory_level=2)
        with open(base_path+'/teachers_index.json', 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        for _, teachers in data.items():
            for teacher in teachers:
                file_path = base_path + '/' + extract_name_initials(teacher['name'])
                print(f"  {teacher['name']}: {file_path}")
                scrape_teacher(teacher['url'], file_path)
            print()

        

if __name__ == '__main__':
    get_index()
    get_info()
    # scrape_teacher("https://ac.bit.edu.cn/szdw/dsmd/bssds/a41c4ee8706848aeba948a520da82a93.htm", "ac/bssds/wangmeiling")