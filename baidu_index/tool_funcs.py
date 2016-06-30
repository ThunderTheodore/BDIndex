# -*- coding: UTF-8 -*-
import datetime


def time2str(t):
    return t.strftime("%Y-%m-%d")


def str2time(s):
    return datetime.datetime.strptime(s, "%Y-%m-%d").date()


def end_of_month(date):
    one_day = datetime.timedelta(days=1)
    y, m = divmod(date.month, 12)
    return datetime.date(date.year+y, m+1, 1)-one_day
