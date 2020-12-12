# OLD VERSION ON AUG.2020

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
from selenium.webdriver.chrome.options import Options
chrome_options=Options()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
url = "https://www.cpppc.org:8082/inforpublic/homepage.html#/searchresult"

browser.get(url)
temp = input("项目名称：完成筛选后回车")
length_page = int(input("页面数量：完成后回车"))
browser.find_element_by_class_name("projectName")
proj_pack = []
keys = []
values = []

# 父循环体换页码
# rangeSet = browser.find_elements_by_class_name("ant-pagination")[0].text.split("\n")
# for i in # 页码单位
for i in range(length_page):
    ## 循环打开所有页面
    print(i+1)
    all_projects = browser.find_elements_by_class_name("projectName")
#    print(len(all_projects))
    for j in all_projects:
        j.click()
        ### 获取页面柄
        handles = browser.window_handles
    for i in range(len(handles)-1):

        browser.switch_to.window(handles[i+1])
        #### 基础数据获取
        time.sleep(0.5)
        name = browser.find_element_by_class_name("descTitle")
        keys.append("项目名称")
        values.append(name.text)
        basic_data_1 = browser.find_element_by_class_name("firstLine")
        for j in basic_data_1.find_elements_by_class_name("tableKey"):
            keys.append(j.text)
        for h in basic_data_1.find_elements_by_class_name("tableValue"):
            values.append(h.text)

        basic_data_2 = browser.find_element_by_class_name("sencondLine")
        for j in basic_data_2.find_elements_by_class_name("tableKey"):
            keys.append(j.text)
        for h in basic_data_2.find_elements_by_class_name("tableValue"):
            values.append(h.text)

        basic_data_3 = browser.find_element_by_class_name("threeLine")
        for j in basic_data_3.find_elements_by_class_name("tableKey"):
            keys.append(j.text)
        for h in basic_data_3.find_elements_by_class_name("tableValue"):
            values.append(h.text)
        all_tables = browser.find_elements_by_class_name("viewTable")
        all_tables_filter = all_tables[0].get_attribute("outerHTML")
        df = pd.read_html(all_tables_filter)[0]
        for i in range(len(df[0])):
            keys.append(list(df[0])[i])
            values.append(list(df[1])[i])
            keys.append(df.iloc[2,2])
            values.append(df.iloc[2,3])
        js="var q=document.documentElement.scrollTop=100000"  
        browser.execute_script(js)  
        try:
            table_caicheng = browser.find_elements_by_class_name("payTable")[-1].get_attribute("outerHTML")
            pd_caicheng = pd.read_html(table_caicheng)[0]
            pd_caicheng_i = pd_caicheng.copy()
            pd_caicheng_i["支出年度"].astype(int)
            pd_caicheng_j = pd_caicheng_i[pd_caicheng_i["支出年度"]>2019]
            keys.append("年均补贴")
            values.append(pd_caicheng["A-本项目一般公共预算支出数额（万元）"].mean())
            max_no = pd_caicheng_j["占比（%）"].idxmax()
            maxs = pd_caicheng_j.loc[max_no].to_frame().T
            names = list(maxs.columns)
            maxs_values = list(maxs.values[0])
            for i in range(len(names)):
                keys.append(names[i])
                values.append(maxs_values[i])
            proj_pack.append(dict(zip(keys, values)))

        except TypeError:
            try:
                current = browser.current_window_handle
                browser.switch_to.window(handles[0])
                browser.switch_to.window(current)
                time.sleep(3)
                browser.execute_script(js)
                browser.execute_script("var q=document.documentElement.scrollTop=0")
                browser.execute_script(js)
                time.sleep(3)
                print(name.text)
                table_caicheng = browser.find_elements_by_class_name("payTable")[-1].get_attribute("outerHTML")
                pd_caicheng = pd.read_html(table_caicheng)[0]
                pd_caicheng_i = pd_caicheng.copy()
                pd_caicheng_i["支出年度"].astype(int)
                pd_caicheng_j = pd_caicheng_i[pd_caicheng_i["支出年度"]>2019]
                keys.append("年均补贴")
                values.append(pd_caicheng["A-本项目一般公共预算支出数额（万元）"].mean())
                max_no = pd_caicheng_j["占比（%）"].idxmax()
                maxs = pd_caicheng_j.loc[max_no].to_frame().T
                names = list(maxs.columns)
                maxs_values = list(maxs.values[0])
                for i in range(len(names)):
                    keys.append(names[i])
                    values.append(maxs_values[i])
                proj_pack.append(dict(zip(keys, values)))
            except:
                pass
        continue
    for i in range(len(all_projects)):
        browser.switch_to.window(handles[i+1])
        browser.close()
    browser.switch_to.window(handles[0])
    browser.find_element_by_class_name("ant-pagination-next").click()
    time.sleep(2)
browser.quit()

full_v = pd.DataFrame(proj_pack)
outer_v = a.drop(columns=["项目示范级别/批次","合作范围","采购方式","A-本项目一般公共预算支出数额（万元）","B-本级已有管理库项目一般公共预算支出数额（万元）"])
outer_v["项目总投资"] = outer_v["项目总投资"].apply(lambda x: (x[:-2]))
outer_v["项目总投资"] = outer_v["项目总投资"].apply(lambda x: float(x.replace(",","")))

outer_v.to_excel("all_proj1.xlsx",index=False)
