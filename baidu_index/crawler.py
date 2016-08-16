# -*- coding: UTF-8 -*-
import time
import StringIO
import urllib
from tool_funcs import str2time
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException


class BaiduCrawler:
    def __init__(self, account, password):
        self.account = account
        self.password = password
        self.url_bdi = ""
        self.graph = None  # 曲线图
        self.scale_img = None  # y坐标刻度
        self.time_span = None  # x坐标范围
        # phantomjs+selenium
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.resourceTimeout"] = 5000
        dcap["phantomjs.page.settings.loadImages"] = True
        dcap["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us)"
            " AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50")
        self.driver = webdriver.PhantomJS(desired_capabilities=dcap,
                                          service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])

    def close(self):
        self.driver.quit()

    def create_search_url(self, keyword, begin_time=-1, end_time=-1, tp="trend", area=0):
        keyword = urllib.quote(keyword.encode("gbk"))
        self.url_bdi = "http://index.baidu.com/?tpl=" + tp + "&area=" + str(area) + "&word=" + keyword
        if begin_time != -1 and end_time != -1:
            self.url_bdi += "&time=" + str(begin_time) + "%7C" + str(end_time)
        return self.url_bdi

    def login(self):
        # bdi represents baidu index
        self.driver.get("http://index.baidu.com/?tpl=trend&word=baidu")
        self.driver.maximize_window()
        # login
        try:
            self.driver.find_element_by_name("userName").send_keys(self.account)
            self.driver.find_element_by_name("password").send_keys(self.password)
            self.driver.find_element_by_id("TANGRAM_12__submit").click()
            while True:
                time.sleep(1)
                try:
                    self.driver.find_element_by_id("select-countrycode")
                    print "Login successfully..."
                    break
                except NoSuchElementException:
                    pass
                try:
                    vc = self.driver.find_element_by_name("verifyCode")
                    self.driver.save_screenshot('./login.png')
                    verify_code = raw_input("Please check out the login.png and input the verification code!\n")
                    vc.send_keys(verify_code)
                    self.driver.find_element_by_id("TANGRAM_12__submit").click()
                except NoSuchElementException:
                    print "Login successfully..."
                    break
                except WebDriverException:
                    print "Wrong verification code!"
        except NoSuchElementException:
            print "Login page has changed\n...Please contact author..."

    def go_to_page(self):
        self.driver.get(self.url_bdi)
        time.sleep(1)

    def capture_graph(self, save=False, save_path="./graph.png"):
        self.driver.get(self.url_bdi)
        time.sleep(1)
        data = self.driver.get_screenshot_as_png()
        entire_page = Image.open(StringIO.StringIO(data))
        img_element = self.driver.find_element_by_css_selector("rect[style=\"opacity: 0; \"]")
        location = img_element.location  # find the location
        size = img_element.size
        crop_rect = (int(location['x']), int(location['y']), int(location['x'] + size['width']),
                     int(location['y'] + size['height']))
        self.graph = entire_page.crop(crop_rect)
        if save:
            self.graph.save(save_path)
        print "Successfully captured graph..."
        return self.graph

    def capture_scale(self, save=False, save_path="./scale.png"):
        img_element = self.driver.find_element_by_id("trendYimg")
        url_scale = img_element.get_attribute("src")
        self.driver.get(url_scale)
        data = self.driver.get_screenshot_as_png()
        self.scale_img = Image.open(StringIO.StringIO(data))
        if save:
            self.scale_img.save(save_path)
        print "Successfully captured scale..."
        return self.scale_img

    def capture_time_span(self):
        try:
            time_span = self.driver.find_element_by_xpath("//div[@id=\"trend-wrap\"]/*/span[2]")
        except NoSuchElementException:
            print "Capture_time_span should be applied before capture_scale!"
            return None
        strs = time_span.text.split(" ")
        self.time_span = (str2time(strs[0]), str2time(strs[2]))
        print "Successfully captured time span..."
        return self.time_span
