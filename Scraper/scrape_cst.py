import requests
from bs4 import BeautifulSoup
import urllib.parse
import json
import os
import logging
import re
from utils import extract_name_initials


def get_index():
    """
    从教师列表页面提取教师主页链接
    """

    # URL
    url = "https://cst.bit.edu.cn/szdw/jsml/index.htm"

    # 发送HTTP请求
    response = requests.get(url)
    response.encoding = 'utf-8'  # 设置编码以防止中文乱码

    # 设置文件路径
    base_path = "cst"

    # 检查HTTP请求是否成功
    if response.status_code == 200:
        # 解析HTML文档
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找所有教师信息的<div>标签
        teacher_sections = soup.find_all('div', class_='content row')

        for section in teacher_sections:

            # 初始化一个字典来存储数据
            data = {}

            # 初始化一个列表来存储数据
            teachers = []

            # 获取导师类别
            mentor_type = section.find('div', class_='sub_page_title fs20').text.strip()
            if "博士生导师" in mentor_type:
                mentor_type = "博士生导师"
                file_path = base_path + "/bssds"

            elif "硕士生导师" in mentor_type:
                mentor_type = "硕士生导师"
                file_path = base_path + "/sssds"
            
            os.makedirs(file_path, exist_ok=True)

            # 查找所有教师列表项
            teacher_list = section.find('div', class_='sub_list001 ul-inline effect effect2 h_transY').find_all('li')
            
            for teacher in teacher_list:
                # 提取链接和姓名
                link_tag = teacher.find('a')
                href = link_tag['href']
                name = teacher.find('div', class_='title fs20').text.strip()
                
                # 构建完整的URL
                full_url = urllib.parse.urljoin(url, href)
                
                # 将信息存储到列表中
                teachers.append({
                    'name': name,
                    'url': full_url
                })
        
            # 将数据写入JSON文件
            data[mentor_type] = teachers
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
    
    os.makedirs(path, exist_ok=True)

    # 发送请求并解析HTML
    response = requests.get(url)
    response.encoding = 'utf-8'
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        data = {}
        # 定位教师信息
        teacher_info = soup.find('div', class_='article fs16')


        # 提取姓名
        try:
            name_span = teacher_info.find('span', style="font-size:28px")
            if name_span:
                name_elem = name_span.text
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
            subject_span = teacher_info.find(string="所在学科")
            if subject_span:
                subject_elem = subject_span.find_next('p').text
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
            title_span = teacher_info.find('span', style="font-size:20px")
            if title_span:
                title_elem = title_span.text
                if title_elem and title_elem.strip():
                    title = title_elem.strip()
                else:
                    title = None
            else:
                title = None
        except (AttributeError, TypeError):
            title = None
            logging.warning(f"Failed to extract title for a teacher")

        phone = None
        email = None
        location = None
        info_tags = teacher_info.find_all('span', style="font-size:16px")
        for tag in info_tags:
            info = tag.get_text()

            # 提取联系电话
            if "办公电话：" in info:
                try:
                    phone_elem = info.replace("办公电话：", "")
                    if phone_elem and phone_elem.strip():
                        phone = phone_elem.strip()
                    else:
                        phone = None
                except (AttributeError, TypeError):
                    phone = None
                    logging.warning(f"Failed to extract phone for a teacher")

            # 提取邮箱
            elif "电子邮件：" in info:
                try:
                    email_elem = info.replace("电子邮件：", "")
                    if email_elem and email_elem.strip():
                        email = email_elem.strip()
                    else:
                        email = None
                except (AttributeError, TypeError):
                    email = None
                    logging.warning(f"Failed to extract email for a teacher")
            
            # 提取通信地址
            elif "办公地点：" in info:
                try:
                    location_elem = info.replace("办公地点：", "")
                    if location_elem and location_elem.strip():
                        location = location_elem.strip()
                    else:
                        location = None
                except (AttributeError, TypeError):
                    location = None

        # 下载教师头像图片
        # 提取图片URL并下载图片
        img_src = teacher_info.find("img")["src"]
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
            'address': location,
        }

        # 打印提取的信息
        print(f"姓名：{name}")
        print(f"所在学科：{subject}")
        print(f"职称：{title}")
        print(f"联系电话：{phone}")
        print(f"E-mail：{email}")
        print(f"通信地址：{location}")
        print("---")

        # 提取教师详细信息
        details = []
        for header in teacher_info.find_all('h1', style=lambda value: value and 'font-size:32px' in value):
            title = header.get_text(strip=True)
            content = []
            for sibling in header.next_siblings:
                if sibling.name == 'h1':
                    break  # 如果遇到下一个<h1>标签，停止收集内容
                if sibling.name == 'p' and sibling.get_text(strip=True):  # 过滤掉空的<p>标签
                    content.append(sibling.get_text(strip=True)+'\n')
            details.append({'title': title, 'content': content})
        data['details'] = details

        print(os.path.join(path, 'profile.json'))
        with open(os.path.join(path, 'profile.json'), 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)


def get_info():
    """
    从教师主页提取信息
    设置好传输路径
    """
    
    dir_path = ["cst/bssds", "cst/sssds"]

    for base_path in dir_path:
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
    # scrape_teacher("https://ac.bit.edu.cn/szdw/dsmd/sssds/znxxclykz/55ef50a33bdf4fd49b5a2b09547e96e9.htm", "ac/sssds/znxxclykz/daili/")