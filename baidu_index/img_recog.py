# -*- coding: UTF-8 -*-
import re
import pytesseract
from datetime import timedelta
from PIL import Image
from tool_funcs import time2str


class BaiduImgRecog:
    def __init__(self):
        self.graph = None
        self.scale = None
        self.time_span = None
        self.pixel_list = []  # 记录曲线像素结果
        self.scale_floor = 0  # y坐标最小值
        self.pixel_y = 0.0  # 一个像素对应多少y值
        self.days = 0  # x轴的天数
        self.x_pixel = 0.0  # 一天（x轴）对应多少像素
        self.result = {}  # 存放结果 每日的百度指数

    def import_data(self, graph, scale, time_span):
        self.graph = graph
        self.scale = scale
        self.time_span = time_span
        self.pixel_list = []
        self.result = {}

    def obtain_baidu_index(self):
        self.__recog_graph()
        self.__recog_scale()
        self.__recog_time_span()
        self.__compute_index()
        return self.result

    def __recog_graph(self):
        img_width = self.graph.size[0]
        img_height = self.graph.size[1]
        for w in range(0, img_width):
            count = 0  # 记录曲线高度（像素）
            for h in range(img_height - 1, -1, -1):
                temp_pix = self.graph.getpixel((w, h))
                if temp_pix[0] < 70 and sum(temp_pix[1:3]) < 520:
                    self.pixel_list.append(count)
                    break
                elif h == 0:
                    self.pixel_list.append(0)
                    break
                count += 1
        print "Successfully recognized graph..."

    def __recog_scale(self):
        img_scale = self.__find_img_bottom_right_corner(self.scale)
        # 放大图像 增强识别效果
        img_scale = img_scale.resize((200, 120), Image.ANTIALIAS)
        scale_str = pytesseract.image_to_string(img_scale)
        temp = self.__extract_ordinate_scale(scale_str)
        self.scale_floor = temp[0]
        self.pixel_y = temp[1]*7.0/(self.graph.size[1]-1)
        print "Successfully recognized scale..."

    def __recog_time_span(self):
        self.days = (self.time_span[1]-self.time_span[0]).days
        self.x_pixel = float(self.graph.size[0]-1)/self.days
        self.days += 1
        print "Successfully recognized time span..."

    def __compute_index(self):
        begin_day = self.time_span[0]
        for d in range(0, self.days):
            d_str = time2str(begin_day+timedelta(d))
            self.result[d_str] = int(self.pixel_list[int(d*self.x_pixel)]*self.pixel_y+self.scale_floor)

    @staticmethod
    def __find_img_bottom_right_corner(img, new_w=100, new_h=60):
        width = img.size[0]
        height = img.size[1]
        w = 0
        h = 0
        while h < height and img.getpixel((w, h))[3] != 0:
            h += 2
        h -= 2
        while w < width and img.getpixel((w, h))[3] != 0:
            w += 2
        return img.crop((w - new_w, h - new_h, w, h))

    @staticmethod
    def __extract_ordinate_scale(scale):
        scale = re.sub(" |,|\.", "", scale)
        scale = scale.split("\n")
        try:
            scale.remove("")
        except ValueError:
            pass
        floor = int(scale[-1])
        interval = int(scale[-2]) - floor
        floor -= interval
        return floor, interval

