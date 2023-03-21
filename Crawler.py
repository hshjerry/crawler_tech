import json
import sys
import argparse
from time import sleep

from selenium import webdriver
import selenium.webdriver.support.ui as ui
from crawler_config import *

driver = webdriver.Chrome()


wait = ui.WebDriverWait(driver, 3)
exception_url_list = []
mode = 0


def crawl_spec(website,url=None,c='新闻'):
    '''
    爬取特定网页的内容
    :param website: 网页名字
    :return: 标题和内容
    '''

    if url != None:
        driver.get(url)
    title = ""
    content = ""
    #todo: 根据c选择i
    for i in range(len(name2paths[website]["title_xpath"])):

        try:
            wait.until(lambda driver: driver.find_element('xpath', name2paths[website]["title_xpath"][i]))
            title = driver.find_element('xpath', name2paths[website]["title_xpath"][i]).text
            wait.until(lambda driver: driver.find_element('xpath', name2paths[website]["content_xpath"][i]))
            content = driver.find_element('xpath', name2paths[website]["content_xpath"][i]).text
            break
        except:
            continue
    if title == "":
        print("error",driver.current_url)
        exception_url_list.append(driver.current_url)

    return title, content, driver.current_url


def crawl_list(website,url=None):
    '''
    爬取一个页面内列表每个页面的内容
    :param url:列表页面
    :return:数据列表
    '''
    crawl_res_list = []
    sleep(1)
    if url != None:
        driver.get(url)
        wait.until(lambda driver: driver.find_element('xpath', name2paths[website]["list_xpath"]))
    # 找到列表的每个元素
    elements = driver.find_elements('xpath', name2paths[website]["list_xpath"])
    dates = driver.find_elements('xpath', name2paths[website]["date_xpath"])
    classes = driver.find_elements('xpath', name2paths[website]["class_xpath"])
    for i in range(len(elements)):
        e = elements[i]
        date = dates[i]
        c = classes[i]
        d = dict()
        d['date'] = date.text
        d['class'] = c.text
        e.click()
        # date = e.find_element('xpath', list_date_xpath).text
        driver.switch_to.window(driver.window_handles[-1])

        # if date <= sep_date: mode = 1
        d['title'], d['content'], d['url'] = crawl_spec(website,c=d['class'])
        crawl_res_list.append(d)
        driver.close()
        driver.switch_to.window(driver.window_handles[-1])
    return crawl_res_list


def crawl_module(keyword,website,start=0, end=-1):
    crawl_res_list = []
    button_path = name2paths[website]["next_page_xpath"]
    driver.get(name2paths[website]["url"])
    driver.find_element('xpath', name2paths[website]["search_xpath"]).send_keys(keyword)
    driver.find_element('xpath', name2paths[website]["search_button_xpath"]).click()
    driver.switch_to.window(driver.window_handles[-1])
    #
    if end==-1:
        sleep(1)
        wait.until(lambda driver: driver.find_elements('xpath', name2paths[website]["end_xpath"]))
        end = int(driver.find_elements('xpath', name2paths[website]["end_xpath"])[3].text)-1

    # 翻页至start
    if start > 0:
        for i in range(start):
            print(1)
            wait.until(lambda driver: driver.find_element('xpath', button_path))
            print(2)
            driver.find_element('xpath', button_path).click()
            print(3)
    # 开始爬取
    for i in range(start, end + 1):
        print("\r", int((i - start) / (end - start) * 100), "%", end="", flush=True)

        crawl_res_list.extend(crawl_list(website))
        if i < end:
            driver.switch_to.window(driver.window_handles[-1])

            sleep(1)
            wait.until(lambda driver: driver.find_element('xpath', button_path))
            driver.find_element('xpath', button_path).click()


            #
    data = {'data': crawl_res_list}
    with open(f'dataset/crawl_data_{website}_{keyword}_{start}_{end}.json', "w", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False))
    if len(exception_url_list) > 0:
        with open(f'exception_{start}_{end}.json', "w", encoding="utf-8") as f:
            f.write(json.dumps(exception_url_list, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--keyword", help="指定爬取的关键词", type=str, default="区域规划")
    parser.add_argument("--website", help="指定爬取的网页", type=str, default="www.most.gov.cn")
    parser.add_argument("--start", help="指定开始爬取的页码", type=int, default=0)
    parser.add_argument("--end", help="指定结束爬取的页码", type=int, default=-1)
    args = parser.parse_args()
    crawl_module(args.keyword, args.website, args.start, args.end)
