# url1 = 'https://www.xuexi.cn/d05cad69216e688d304bb91ef3aac4c6/9a3668c13f6e303932b5e0e100fc248b.html'  # 学习时评
# url2 = 'https://www.xuexi.cn/7097477a9643eacffe4cc101e4906fdb/9a3668c13f6e303932b5e0e100fc248b.html'  # 综合新闻
# url3 = 'https://www.xuexi.cn/98d5ae483720f701144e4dabf99a4a34/5957f69bffab66811b99940516ec8784.html'  # 重要新闻
# url = url1
# title_xpath = "//*[@id=\"root\"]/div/section/div/div/div/div/div[2]/section/div/div/div/div/div/div/div[1]/div"
# content_xpath = "//*[@id=\"root\"]/div/section/div/div/div/div/div[2]/section/div/div/div/div/div/div/div[3]/div[1]"
# title1_xpath = "//*[@id=\"Cd1smadng91s00\"]/p"
# content1_xpath = "//*[@id=\"Cl3caikxy44w00\"]"
# list_date_xpath = '//div/div/div[2]/span'
# list_xpath = "//*[@id=\"page-main\"]/section/div/div/div/div/div/section/div/div/div/div[1]/div/section/div/div/div/div/div/section/div/div/div/div/div[3]/section/div/div/div/div/div/section/div/div/div[1]/div/div"
# date_xpath = '//*[@id="page-main"]/section/div/div/div/div/div/section/div/div/div/div[1]/div/section/div/div/div/div/div/section/div/div/div/div/div[3]/section/div/div/div/div/div/section/div/div/div[1]/div/div/div/div/div[2]/span'
# sep_date = '2019-04-18'
name2paths = {
    "www.most.gov.cn":{
        "url": "https://www.most.gov.cn/index.html",
        "next_page_xpath": "//*[@id=\"page_jiansuo\"]/a/li[text()=\"下一页\"]",
        "search_xpath": "//*[@id=\"searchword\"]",
        "search_button_xpath": "//*[@id=\"header-title-search-btn\"]/a",
        "title_xpath": ["//*[@id=\"Title\"]","/html/body/div[4]/div/div[2]/div[1]","/html/body/table/tbody/tr[3]/td/p/font"],
        "content_xpath": ["//*[@id=\"Zoom\"]","//*[@id=\"Zoom\"]","//*[@id=\"Zoom2\"]"],
        "list_xpath": "//*[@id=\"content\"]/li/a",
        "date_xpath": "//*[@id=\"content\"]/li/p[1]",
        "end_xpath": "//*[@id=\"page_jiansuo\"]/a",
        "class_xpath": "//*[@id=\"content\"]/li/a/h2/i"
    }
}
