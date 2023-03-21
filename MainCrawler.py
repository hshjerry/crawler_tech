import json
import subprocess
import time
import argparse


def mainCrawler(head, tail, step):
    # 主爬虫过程,定义起止页码,步长
    process_list = []
    pos_list = []
    keywords = ['区域规划']
    websites = ['www.most.gov.cn']
    for keyword in keywords:
        for website in websites:
            for i in range(head, tail, step):
                start = i
                end = i + step - 1
                if end > tail:
                    end = tail
                process = subprocess.Popen(f'python Crawler.py --start {start} --end {end} --keyword {keyword} --website {website}', shell=True,
                                           start_new_session=True)
                process_list.append(process)
                pos_list.append([start, end])
            for p in process_list:
                while p.poll() is None:
                    time.sleep(1)
                p.communicate()
    # for i in range(head, tail, step):
    #     start = i
    #     end = i + step - 1
    #     if end > tail:
    #         end = tail
    #     process = subprocess.Popen(f'python Crawler.py --start {start} --end {end}', shell=True,
    #                                start_new_session=True)
    #     process_list.append(process)
    #     pos_list.append([start, end])
    # for p in process_list:
    #     while p.poll() is None:
    #         time.sleep(1)
    #     p.communicate()


def merge_data(head, tail, step):
    # 整合爬取结果为一个文件
    pos_list = []
    crawl_res_list = []
    for i in range(head, tail, step):
        start = i
        end = i + step - 1
        if end > tail:
            end = tail
        pos_list.append([start, end])
    for pos in pos_list:
        start, end = pos
        data_list = json.load(open(f'dataset/crawl_data_{start}_{end}.json', encoding="utf-8"))['data']
        crawl_res_list.extend(data_list)
        data = {'data': crawl_res_list}
        with open(f'dataset/crawl_data_raw.json', "w", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--head", help="指定开始爬取的页码", type=int, default=0)
    parser.add_argument("--tail", help="指定结束爬取的页码", type=int, default=3)
    parser.add_argument("--step", help="指定页码步长", type=int, default=1)
    args = parser.parse_args()
    head = args.head
    tail = args.tail
    step = args.step
    mainCrawler(head, tail, step)
    # merge_data(head, tail, step)
