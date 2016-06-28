# -*- coding: UTF-8 -*-
import datetime


def time2str(t):
    return t.strftime("%Y-%m-%d")


def str2time(s):
    return datetime.datetime.strptime(s, "%Y-%m-%d").date()
