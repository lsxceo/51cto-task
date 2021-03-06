#!/usr/bin/env Python
# -*- coding:utf-8 -*-
# create_event.py
# author: lishixiang


"""
把一段简单的格式化语句解析拆解，返回一个列表
('time', 'thing', @'people')
对的示例：（今天晚上8点半看电影@小周；18号早上8点10分赶火车；明天晚上5点50分吃火锅@小王）
错误示例：（今天晚上8点30看电影  ‘少了一个分’）
"""

from datetime import date
from datetime import time
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import dateutil.rrule


class Create_event:
    """创建一个事件的类"""
    def __init__(self, event):
        "初始化类并设置属性"
        self.event = event
        self.datelist = ['今天', '明天', '后天']
        # 简单区分时间凌晨（>0:00-<5:00）;早上（5:00-<8:00）；上午（8:00-<11:00）；中午（11:00-<13:00）；下午（13:00-<18：00）；晚上（18:00-<24:00）
        self.timelist = ['凌晨', '早上', '上午', '中午', '下午', '晚上']
        self.hourlist = ['点半', '点']
        self.split_list = []
        self.split_main()
        self.new_list = self.format_list()

    def convert_to_date(self, datemessage):
        "把'今天','明天','后天'转换成具体的日期"
        if datemessage == '今天':
            day = date.today()
        elif datemessage == '明天':
            day = date.today() + timedelta(days=1)
        elif datemessage == '后天':
            day = date.today() + timedelta(days=2)
        return day

    def find_date(self):
        "把字符串解析拆分，先找出日期"
        if self.event[:2] == '下周':
            weekdaylist = {
                '一': 'MO',
                '二': 'TU',
                '三': 'WE',
                '四': 'TH',
                '五': 'FR',
                '六': 'SA',
                '天': 'SU',
                '日': 'SU'
            }
            weekday = weekdaylist[self.event[2:3]]
            date = datetime.now() + relativedelta(weekday=getattr(dateutil.rrule, weekday)(+1))
            date_ = date.strftime('%Y-%m-%d')
            self.event = self.event[3:]
        elif self.event[:3] == '下个月':
            day = self.event[3:self.event.find('号')]
            date = datetime.now() + relativedelta(months=+1, day=int(day))
            date_ = date.strftime('%Y-%m-%d')
            self.event = self.event[self.event.find('号'):]
        else:
            try_find_day = self.event[:2]
            if try_find_day in self.datelist:
                datemessage = try_find_day
                date_ = self.convert_to_date(datemessage)  # 调用函数计算出日期
                self.event = self.event[2:]  
            else:
                day = self.event[:self.event.find('号')]
                date_ = datetime.date.today().replace(day=int(day))
                self.event = self.event[self.event.find('号') + 1:]
        self.split_list.append(date_)

    def find_frame(self):
        "找出时间段"
        for i in self.timelist:
            if i in self.event:
                time_frame = i
                self.event = self.event[self.event.find(i) + len(i):]
        self.split_list.append(time_frame)

    def find_hour(self):
        "找出小时,1点半算成1点30分,直接根据前面函数的时区转换成24小时制"
        for i in self.hourlist:
            if i in self.event:
                if i == '点半':
                    hour = int(self.event[:self.event.find(i)])
                    self.event = '30分' + self.event[self.event.find(i) + len(i):]
                else:
                    hour = int(self.event[:self.event.find(i)])
                    self.event = self.event[self.event.find(i) + len(i):]

        if self.split_list[-1] == '中午':
            if hour < 11:
                hour += 12
        elif self.split_list[-1] == '下午' or self.split_list[-1] == '晚上':
            hour += 12
        self.split_list.append(hour)

    def find_minute(self):
        "找出几分钟"
        try:
            minute = int(self.event[:self.event.find('分')])
            self.event = self.event[self.event.find('分') + 1:]
        except Exception:
            minute = 0
        self.split_list.append(minute)

    def find_thing(self):
        "找出事件"
        self.event = self.event.split('@')
        thing = self.event.pop(0)
        self.split_list.append(thing)

    def find_people(self):
        "找出@的人，如果没人就加一个我"
        if self.event == []:
            people = ['我']
        else:
            people = self.event
        self.split_list.append(people)

    def format_list(self):
        "把事件格式化，并添加到列表中"
        new_list = []
        date = self.split_list[0]
        time_ = time(self.split_list[2], self.split_list[3])
        new_list.append(f'{date} {time_}')
        new_list.append(self.split_list[4])
        # if len(self.split_list[5]) == 1:
        #     at_people = '@' + self.split_list[5][0]
        # else:
        #     at_people = '@' + '@'.join(self.split_list[5])
        # new_list.append(at_people)
        new_list.append(self.split_list[5])
        return new_list
        # return f'{date} {time_} {self.split_list[4]}{at_people}'

    def split_main(self):
        "主要的操作程序"
        self.find_date()
        self.find_frame()
        self.find_hour()
        self.find_minute()
        self.find_thing()
        self.find_people()


def main():
    "测试程序"
    event = '下周六下午6点吃火锅@小李@小王'
    thing = Create_event(event)
    # print(thing.split_list)
    print('下周六', thing.format_thing())


if __name__ == "__main__":
    main()