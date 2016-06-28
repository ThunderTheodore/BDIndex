# -*- coding: UTF-8 -*-
from baidu_index.crawler import BaiduCrawler
from baidu_index.img_recog import BaiduImgRecog

if __name__ == "__main__":
    bc = BaiduCrawler("baidu_account", "password")
    bc.login()
    keywords = ["baidu", "steam"]
    ts = (20160401, 20160430)
    for kw in keywords:
        bc.create_search_url(kw, begin_time=ts[0], end_time=ts[1])
        bc.go_to_page()
        graph = bc.capture_graph(save=False)
        time_span = bc.capture_time_span()
        scale = bc.capture_scale(save=False)

        bir = BaiduImgRecog()
        bir.import_data(graph, scale, time_span)
        result = bir.obtain_baidu_index()
        print "Keyword: %s;\nTime span: %d - %d" % (kw, ts[0], ts[1])
        for key in result:
            print key, result[key]
    bc.close()


