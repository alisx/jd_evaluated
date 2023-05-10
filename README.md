## 京东订单评价程序

基于 Python 技术上的一篇文章里提到的程序改编而来，仅限于爬虫的学习之用。

### 功能

1. 自动查找待平均记录，完成平均（支持一个订单多个商品的情况）
2. 自动完成追评
3. 自动完成服务评价

### 依赖

- Python3.6+
- requests
  `pip install requests`
- BeautifulSoup
  `pip install BeautifulSoup4`

### 使用

1. 登陆京东网站，查看评价页，提取某个 Post 请求的 cookie 值
2. 进入 src 文件夹，打开 main.py 代码文件，用提取的 cookie 值，替换变量 cookie 的值：

   ```python
   cookie = '__jdu ... 26.1683600056' # 替换提取的 cookie
   ```

3. 运行 `python main.py`

如果一切正常，执行完成后会自动结束;

执行目录下会生成一个 `index.html` 文件，为评价页 html 脚本，可以用于测试。
