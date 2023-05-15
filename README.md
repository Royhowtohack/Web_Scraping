## Python 网络爬虫案例，抓取https://www.cdggzy.com/ 网站中标信息


``` markdown
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
```
