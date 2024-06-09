import requests
from bs4 import BeautifulSoup
import urllib.parse
import json
import os
import logging
from utils import extract_name_initials, get_file_path


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

def get_index():
    # 目标URL
    url = 'https://cs.bit.edu.cn/szdw/jsml/index.htm'

    os.makedirs('cs', exist_ok=True)

    # 发送HTTP请求
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'  # 设置编码以防止中文乱码

    # 初始化一个字典来存储数据
    data = {}

    # 检查HTTP请求是否成功
    if response.status_code == 200:
        # 解析HTML文档
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找所有包含教师主页链接的<div>标签
        teacher_divs = soup.find_all('div', class_='teacher')
        
        # 基础URL，用于拼接相对路径
        base_url = url
        
        print(f"{base_url}")
        # 遍历每个<div>标签，提取其中的链接
        for teacher_div in teacher_divs:
            # 获取类别标题
            title = teacher_div.find('h4').text.strip()
            if title not in ["院士","国家级高层次人才","博士生导师","硕士生导师"]:
                break
            # 初始化类别列表
            if title not in data:
                data[title] = []
            
            # 查找所有<li>标签中的<a>标签
            links = teacher_div.find_all('a', href=True)
            
            # 存储教师姓名和链接
            for link in links:
                name = link.text.strip()
                href = link['href']
                full_url = urllib.parse.urljoin(base_url, href)
                data[title].append({"name": name, "url": full_url})
        
        # 将数据写入JSON文件
        with open('cs/cs_teachers_index.json', 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")


def scrape_teacher(url, path):


    if not os.path.exists(path):
        os.makedirs(path)
    # 发送请求并解析HTML
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        data = {}
        # 定位教师信息
        teacher_divs = soup.find_all("div", class_="xq_teacher")

        # 遍历每个教师信息
        for teacher_div in teacher_divs:
            # 提取姓名
            try:
                name_span = teacher_div.find("span", string="姓名：")
                if name_span:
                    name_elem = name_span.find_next_sibling(string=True)
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
                subject_span = teacher_div.find("span", string="所在学科：")
                if subject_span:
                    subject_elem = subject_span.find_next_sibling(string=True)
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
                title_span = teacher_div.find("span", string="职称：")
                if title_span:
                    title_elem = title_span.find_next_sibling(string=True)
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
                phone_span = teacher_div.find("span", string="联系电话：")
                if phone_span:
                    phone_elem = phone_span.find_next_sibling(string=True)
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
                email_span = teacher_div.find("span", string="E-mail：")
                if email_span:
                    email_elem = email_span.find_next_sibling(string=True)
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
                address_span = teacher_div.find("span", string="通信地址：")
                if address_span:
                    address_elem = address_span.find_next_sibling()
                    if address_elem and address_elem.text.strip():
                        address = address_elem.text.strip()
                    else:
                        address = None
                else:
                    address = None
            except (AttributeError, TypeError):
                address = None
                logging.warning(f"Failed to extract address for a teacher")

            # 下载教师头像图片
            img_src = teacher_div.find("img")["src"]
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

            teacher_info = {}
            teacher_info["name"] = name
            teacher_info["subject"] = subject
            teacher_info["professional_title"] = title
            teacher_info["tel"] = phone
            teacher_info["email"] = email
            teacher_info["address"] = address

            data["info"] = teacher_info

            # 打印提取的信息
            print(f"姓名：{name}")
            print(f"所在学科：{subject}")
            print(f"职称：{title}")
            print(f"联系电话：{phone}")
            print(f"E-mail：{email}")
            print(f"通信地址：{address}")
            print("---")

        teacher_details = []
        for div in soup.find_all('div', class_='con01_t'):
            result = {}
            title = div.find('h4').text.strip()
            result["title"] = title
            content = '\n'.join([p.text.strip() for p in div.find_all('p')])
            if content.strip() == "":
                content = None
            result["content"] = content
            teacher_details.append(result)
        
        data["details"] = teacher_details
        print(os.path.join(path, 'profile.json'))
        with open(os.path.join(path, 'profile.json'), 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)


def get_info():
    with open('cs/cs_teachers_index.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    os.makedirs('cs', exist_ok=True)
    for _, teachers in data.items():
        for teacher in teachers:
            base_path = os.path.dirname(get_file_path(teacher['url'], school_name="cs", directory_level=-2))
            file_path = base_path + '/' + extract_name_initials(teacher['name'])
            print(f"  {teacher['name']}: {file_path}")
            scrape_teacher(teacher['url'], file_path)
        print()


if __name__ == '__main__':
    get_index()
    get_info()
    # scrape_teacher("https://cs.bit.edu.cn/szdw/jsml/js/sf/index.htm", "cs/js/sf")