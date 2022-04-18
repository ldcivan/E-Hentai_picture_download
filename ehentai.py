# coding=gbk
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
import time
import re
import os


indexUrl = input("請輸入作品網址|Please Enter the Adress of the Artwork：") or 'https://e-hentai.org/g/928151/e8de7d62e1/'
option = FirefoxOptions()
driver = webdriver.Firefox()
#driver = webdriver.Chrome()
driver.implicitly_wait(10)




def getPage(pageNow):
    # 获取当前URL的HTML页面
    htmlNow = driver.page_source
    #print(htmlNow)
    # 使用lxml库的xpath查找script元素的内容（提前观察前程无忧搜索结果页面源代码的结构，可以发现岗位列表在script中）
    imgNow = re.search('<img id="img" src="(.+?)"', htmlNow)
    if(pageNow <=10):
        pageNow = '00' + str(pageNow)
    elif(pageNow <=100):
        pageNow = '0' + str(pageNow)
    print(imgNow[1])
    name = imgNow[1].split('/')[-1]
    print(name)
    driver.find_element_by_xpath('//body/div/div/a/img[1]').screenshot('%s%s_%s.png' % (filename, pageNow, name))
    #screen_shot(imgNow[1], filename + name + '.png')
    #a = requests.get(url=imgNow[1], headers=HEADERS, verify=False)
    #f = open('/image/'+name, 'wb')
    #f.write(a.content)
    #f.close()  # 将图片保存为name

def mkdir(s):  # 创建文件夹
    isExists = os.path.exists(s)  # 判断是否创建了文件夹
    if not isExists:
        os.makedirs(s)  # 创建文件夹
        print("創建文件夾'%s'，文件會被保存於此|Have created '%s', pictures will be saved here." % (s, s))
    else:
        print("已經有'%s'文件夾，文件會被保存於此|'%s' already exists, pictures will be saved here." % (s, s))

def screen_shot(url,name):
    # 使用webdirver.PhantomJS()方法新建一个phantomjs的对象，这里会使用到phantomjs.exe，环境变量path中找不到phantomjs.exe，则会报错

    # 使用get()方法，打开指定页面。注意这里是phantomjs是无界面的，所以不会有任何页面显示
    driver.get(url)
    # 设置phantomjs浏览器全屏显示
    driver.maximize_window()
    # 使用save_screenshot将浏览器正文部分截图，即使正文本分无法一页显示完全，save_screenshot也可以完全截图
    driver.find_element_by_xpath('//body/img[1]').screenshot(name)
    # 关闭phantomjs浏览器，不要忽略了这一步，否则你会在任务浏览器中发现许多任务
    driver.close()


# 跳转至目标城市网页

driver.get(indexUrl)
# 点击搜索，网页跳转至搜索结果页面
time.sleep(1)
mainhtml = driver.page_source
firstpage = re.search('no-repeat"><a href="(.+?)"><img alt=', mainhtml)
artwork = re.search('<h1 id="gn">(.+?)</h1>', mainhtml)
artworkName = artwork[1]
filename = "./"+ artworkName +"/"
mkdir(filename)
# 等待1秒
time.sleep(1)
print(firstpage[1])
driver.get(firstpage[1])


# 定义根据页面的index获取页面职位列表的函数

# 获取当前URL的HTML页面
time.sleep(1)
html = driver.page_source
#print(html)

total_page_str = re.search('/ <span>(.+?)</span>', html)
# 正则表达式获取搜索结果总页数,可以匹配1位数，两位数，三位数，四位数，五位数，可以涵盖所有可能性了
total_page = int(total_page_str[1])
print("共 %s 页" %total_page)

for pageNow in range(1,total_page+1):
#for pageNow in range(1, 501):
    print("正在爬取 %s 页，共 %s 页" %(pageNow, total_page))
    time.sleep(5)
    getPage(pageNow)
    driver.find_elements_by_tag_name('a')[2].click()

driver.quit()
