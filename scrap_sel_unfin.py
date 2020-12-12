# 初始化
import re
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
from selenium.webdriver.chrome.options import Options
chrome_options=Options()
chrome_options.add_argument('--headless')

# 加载页面处理
def excute():
    # 存储变量的内容
    text_inner = []
    LENGTH = int(input("Please input the length of page"))
    URL = "http://www.ccgp-guangxi.gov.cn/full/search.html?k=PPP%E5%92%A8%E8%AF%A2"
    XPATH_INFO = "/html/body/div[1]/div[1]/div[2]/div/ul/li[1]/div/ul/li[7]"
    XPATH_CONTRACT = "/html/body/div[1]/div[1]/div[2]/div/ul/li[7]/div/ul/li[3]"
    XPATH_DATE = "/html/body/div[1]/div[1]/div[2]/div/ul/li[11]/div/div[2]/ul/li[5]"
    # 启动浏览器
    browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
    get_page(browser,URL)
    direct_closed_deal(browser)
    # 处理下一页的问题
    for i in range(LENGTH):
        time.sleep(0.5)
        get_list(browser)
        switch_handle(browser)
        switch_page(browser)
    close_browser(browser)
    return text_inner
    
def get_page(brow,URL):
    brow.implicitly_wait(10)
    brow.get(URL)
    print("page is opened")
    
def direct_closed_deal(brow):
    brow.find_element_by_xpath(XPATH_INFO).click()
    time.sleep(0.1)
    brow.find_element_by_xpath(XPATH_CONTRACT).click()
    time.sleep(0.1)
    brow.find_element_by_xpath(XPATH_DATE).click()
    time.sleep(0.1)
    print("页面搜索完成")
    
def get_list(brow):
    time.sleep(2)
    link_lst = brow.find_elements_by_class_name("list")
    for i in range(len(link_lst)-2):
        link_lst[i].click()
    print("子区加载完成")

def switch_handle(brow):
    daddy_page = brow.current_window_handle
    all_handle = brow.window_handles
    all_handle.remove(daddy_page)
    for pages in all_handle:
        brow.switch_to.window(pages)
        print("本页面停留一秒")
        time.sleep(1)
        # TODO: 此处主要完成页面分析工作
        # function using
        single_page_operator(brow)
        brow.close()
        print("页面已关闭")
    brow.switch_to.window(daddy_page)
    print("回到父页面")
    #TODO： 跳入下一个页面

def switch_page(brow):
    brow.find_element_by_class_name("paginationjs-next").click()

def close_browser(brow):
    time.sleep(5)
    brow.quit()
    print("browser has been closed safely.")
    
# -----------------------------------------------------
# 单个页面内的文本挖掘 （核心内容，明天完成）

def single_page_operator(brow):
    into_frame(brow)
    # 文本挖掘内容
    collect_text(brow)
    
    out_frame(brow)

def into_frame(brow):
    # iframe利用switch_to.frame处理。
    brow.switch_to.frame(0)
    print("进入frame")

def out_frame(brow):
    brow.switch_to.default_content()
    print("退出frame")

def collect_text(brow):
    full_text = brow.find_element_by_class_name("view").text
    text_inner.append(full_text)


# REPL阶段
    
def re_filter():
  supplier_inner = []
  for str_re in text_inner:
      supplier_match = re.search("供应商.*：.*公司\n",str_re)
      supplier_match_2 = re.search("中标人：.*\n",str_re)
      supplier_match_3 = re.search("社会资本：.*\n",str_re)
      supplier_match_4 = re.search(".*公司",str_re)
      supplier_match_5 = re.search("单位名称：.*。",str_re)
      if supplier_match_2:
          supplier_position = supplier_match_2.span()
          supplier_inner.append(str_re[supplier_position[0]:supplier_position[1]-1])
          print(supplier_position)
      elif(supplier_match_3):
          supplier_position = supplier_match_3.span()
          supplier_inner.append(str_re[supplier_position[0]:supplier_position[1]-1])
          print(supplier_position)
      elif(supplier_match_5):
          supplier_position = supplier_match_5.span()
          supplier_inner.append(str_re[supplier_position[0]:supplier_position[1]])
      elif(supplier_match):
          supplier_position = supplier_match.span()
          supplier_inner.append(str_re[supplier_position[0]:supplier_position[1]-1])
          print(supplier_position)
      elif(supplier_match_4):
          supplier_position = supplier_match_4.span()
          supplier_inner.append("供应商名称："+str_re[supplier_position[0]+1:supplier_position[1]])
      else:
          supplier_inner.append(text_inner.index(str_re))
  for (i,j) in enumerate(supplier_inner):
      print(i,j)
