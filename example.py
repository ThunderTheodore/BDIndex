# -*- coding: UTF-8 -*-
"""
抓取“苹果”从2012-01-01到2015-12-31每天的百度指数
"""

from baidu_index.crawler import BaiduCrawler
from baidu_index.img_recog import BaiduImgRecog
from baidu_index.tool_funcs import end_of_month
from selenium.common.exceptions import NoSuchElementException
import datetime

if __name__ == "__main__":
    bc = BaiduCrawler("baidu_account", "password")
    bc.login()
    bir = BaiduImgRecog()
    kw = u"苹果"

    for y in range(2012, 2016):
        for m in range(1, 13):
            dt1 = datetime.date(y, m, 1)
            dt2 = end_of_month(dt1)
            bc.create_search_url(kw, begin_time=int(dt1.strftime("%Y%m%d")),
                                 end_time=int(dt2.strftime("%Y%m%d")))
            try:
                graph = bc.capture_graph(save=False)
            except NoSuchElementException:
                print "refreshing page..."
                graph = bc.capture_graph(save=False)
            time_span = bc.capture_time_span()
            scale = bc.capture_scale(save=False)
            
            bir.import_data(graph, scale, time_span)
            try:
                result = bir.obtain_baidu_index()
            except IndexError:
                print "refreshing page..."
                bc.go_to_page()
                scale = bc.capture_scale(save=False)
                bir.import_data(graph, scale, time_span)
                result = bir.obtain_baidu_index()
            
            print "Keyword: %s" % kw
            for key in result:
                print key, result[key]
    bc.close()



