"""
1. 导入所需的库，包括selenium、beautifulsoup4、requests、csv、os和time。
2. 定义`create_csv_if_not_exists`函数，用于在不存在时创建一个CSV文件并写入表头。
3. 定义`get_data_from_url`函数，从给定的URL中获取招标信息，并将其作为字典返回。
4. 定义`read_existing_data`函数，用于读取现有CSV文件中的数据并返回一个包含所有行的列表。
5. 设置selenium的WebDriver，指定Chrome浏览器的驱动路径。
6. 使用WebDriver打开指定的网站。
7. 在网站上查找并点击“中标结果公示”按钮。
8. 等待页面加载，然后获取页面HTML。
9. 使用beautifulsoup4解析页面HTML，提取包含招标信息链接的元素。
10. 构造招标信息页面的URL列表。
11. 检查并创建CSV文件（如果不存在）。
12. 读取现有的CSV数据。
13. 遍历招标信息页面的URL列表，从每个页面获取招标信息，并将新信息添加到CSV文件中（仅添加不存在于现有数据中的新信息）。
14. 关闭浏览器。

"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import csv
import time
import os


# 创建CSV文件，如果不存在
def create_csv_if_not_exists(filename):
    if not os.path.exists(filename):
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['中标通知书发出日期', '招标人', '中标单位', '中标价']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            print(f"Created {filename} file.")


# 从给定的网址中获取数据
def get_data_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'class': 'tabList'})

    rows = table.find_all('tr')
    data = {}
    for row in rows:
        cells = row.find_all(['th', 'td'])
        for i in range(0, len(cells), 2):
            key = cells[i].text.strip()
            value = cells[i + 1].text.strip()
            data[key] = value

    return data


# 读取现有的CSV数据
def read_existing_data():
    existing_data = []
    with open('result.csv', 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        for row in reader:
            existing_data.append(row)
    return existing_data


# 设置WebDriver
service = Service(executable_path="/Users/mr.mou/Code/web_scraping/chromedriver")
driver = webdriver.Chrome(service=service)

# 打开网站
driver.get('https://www.cdggzy.com/site/JSGC/List.aspx')

# 查找并点击“中标结果公示”按钮
try:
    button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'option') and contains(text(), '中标结果公示')]"))
    )
    driver.execute_script("arguments[0].click();", button)
except Exception as e:
    print("Error: ", e)

# 等待页面加载
time.sleep(5)

# 获取页面HTML
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# 获取链接
links = soup.select('#contentlist .infotitle a')
urls = [link['href'] for link in links]

# 检查并创建CSV文件（如果不存在）
create_csv_if_not_exists('result.csv')

# 读取现有数据
existing_data = read_existing_data()

# 将新数据写入CSV文件，仅添加不存在的新信息
with open('result.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['中标通知书发出日期', '招标人', '中标单位', '中标价']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for url in urls:
        data = get_data_from_url(url)
        new_row = [data.get('中标通知书发出日期', 'N/A'), data['招标人'], data['中标单位'], data['中标价']]

        # 检查新行是否已存在于现有数据中，如果不存在，则将其添加到CSV文件中
        if new_row not in existing_data:
            writer.writerow({'中标通知书发出日期': new_row[0], '招标人': new_row[1], '中标单位': new_row[2], '中标价': new_row[3]})
            print(f"Data from {url} saved to result.csv")

# 关闭浏览器
driver.quit()


