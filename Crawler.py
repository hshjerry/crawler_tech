import json
import sys
import argparse

from selenium import webdriver
import selenium.webdriver.support.ui as ui
from crawler_config import *

driver = webdriver.Chrome()


wait = ui.WebDriverWait(driver, 10)
exception_url_list = []
mode = 0


def crawl_spec(website,url=None):
    '''
    爬取特定网页的内容
    :param website: 网页名字
    :return: 标题和内容
    '''

    if url != None:
        driver.get(url)
    try:
        wait.until(lambda driver: driver.find_element_by_xpath(name2paths[website]["title_xpath"]))
        title = driver.find_element_by_xpath(name2paths[website]["title_xpath"]).text
        wait.until(lambda driver: driver.find_element_by_xpath(name2paths[website]["content_xpath"]))
        raw_content = driver.find_element_by_xpath(name2paths[website]["content_xpath"])
    except Exception as e:
        print("error:",driver.current_url)
        exception_url_list.append(driver.current_url)
        return "", ""

    content = raw_content.text

    return title, content


def crawl_list(website,url=None):
    '''
    爬取一个页面内列表每个页面的内容
    :param url:列表页面
    :return:数据列表
    '''
    crawl_res_list = []
    if url != None:
        driver.get(url)
        wait.until(lambda driver: driver.find_element_by_xpath(name2paths[website]["list_xpath"]))
    # 找到列表的每个元素
    elements = driver.find_elements_by_xpath(name2paths[website]["list_xpath"])
    for e in elements:
        e.click()
        # date = e.find_element_by_xpath(list_date_xpath).text
        driver.switch_to.window(driver.window_handles[-1])
        d = dict()
        # if date <= sep_date: mode = 1
        d['title'], d['content'] = crawl_spec(website)
        crawl_res_list.append(d)
        driver.close()
        driver.switch_to.window(driver.window_handles[-1])
    return crawl_res_list


def crawl_module(keyword,website,start=0, end=-1):
    crawl_res_list = []
    button_path = name2paths[website]["next_page_xpath"]
    driver.get(name2paths[website]["url"])
    driver.find_element_by_xpath(name2paths[website]["search_xpath"]).send_keys(keyword)
    driver.find_element_by_xpath(name2paths[website]["search_button_xpath"]).click()

    # 翻页至start
    if start > 0:
        for i in range(start):
            print(1)
            wait.until(lambda driver: driver.find_element_by_xpath(button_path))
            print(2)
            driver.find_element_by_xpath(button_path).click()
            print(3)
    # 开始爬取
    for i in range(start, end + 1):
        print("\r", int((i - start) / (end - start) * 100), "%", end="", flush=True)
        wait.until(lambda driver: driver.find_element_by_xpath(button_path))
        button = driver.find_element_by_xpath(button_path)
        crawl_res_list.extend(crawl_list(website))
        if i < end:
            button.click()
            # driver.switch_to.window(driver.window_handles[-1])
    data = {'data': crawl_res_list}
    with open(f'C:/Users/38908/PycharmProjects/pythonProject/dataset/crawl_data_{website}_{keyword}_{start}_{end}.json', "w", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False))
    if len(exception_url_list) > 0:
        with open(f'exception_{start}_{end}.json', "w", encoding="utf-8") as f:
            f.write(json.dumps(exception_url_list, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--keyword", help="指定爬取的关键词", type=str, default="", required=True)
    parser.add_argument("--website", help="指定爬取的网页", type=str, default="")
    parser.add_argument("--start", help="指定开始爬取的页码", type=int, default=0)
    parser.add_argument("--end", help="指定结束爬取的页码", type=int, default=0)
    args = parser.parse_args()
    crawl_module(args.keyword, args.website, args.start, args.end)
