# -*- coding:UTF-8 -*-

import threading
from bs4 import BeautifulSoup


class Parser (threading.Thread):
    """
    解析器，用来解析Spider类传来的html页面
    """
    def __init__(self, html, date, flightsInformation):
        """
        接受来自Spider的传参并初始化
        :param html: 待解析的html页面
        :param date: 对应的日期
        :param flightsInformation: Spider类属性，用来存放解析好的航班信息
        """
        super().__init__()
        self.lowest = {"价格": 99999}
        self.html= html
        self.date = date
        self.flightsInformation = flightsInformation

    def run(self):
        """
        新线程执行函数，解析搜索结果页面的所有航班信息
        :return: 无返回，但是会向Spider类属性thread_list里添加解析结果
        """
        bs = BeautifulSoup(self.html, "html.parser")
        flights_div = bs.select("div[class='search_table_header']")
        flights_list = []
        for flight in flights_div:
            flights_list.append(self.__parseFlightInformation(flight))
        # print(len(flights_list))
        self.__output(flights_list)

    def __parseFlightInformation(self, flight):
        """
        解析单个航班信息
        :param flight: 单个航班对应的div标签
        :return: 返回解析好的单个航班信息
        """
        price = eval(self.__getPrice(flight))
        information = {
            "航空公司": self.__getCompany(flight),
            "航班号": self.__getNumber(flight),
            "飞机型号": self.__getModel(flight),
            "日期": self.date,
            "出发到达时间": self.__getTime(flight),
            "出发到达机场": self.__getAirport(flight),
            "到达准点率": self.__getPunctualityRate(flight),
            "价格": price
        }
        if price < self.lowest["价格"]:
            self.lowest = information
        return information

    def __getCompany(self, search_table_header):
        """
        解析航班的航空公司
        :param search_table_header: 单个航班对应的div标签
        :return: 航班的航空公司（字符串类型）
        """
        try:
            flightCompany = search_table_header.select("div[class='logo-item flight_logo']")[
                0].div.span.span.strong.get_text()
        except:
            flightCompany = ""
        return flightCompany.lstrip().rstrip().replace('\n', '').replace('\r', '')

    def __getNumber(self, search_table_header):
        """
        解析航班的航班号
        :param search_table_header: 单个航班对应的div标签
        :return: 航班的航班号（字符串类型）
        """
        try:
            flightNumber = search_table_header.select("div[class='logo-item flight_logo']")[0].div.span.span.span.string
        except:
            flightNumber = ""
        return flightNumber.lstrip().rstrip().replace('\n', '').replace('\r', '')

    def __getModel(self, search_table_header):
        """
        解析航班的飞机型号
        :param search_table_header: 单个航班对应的div标签
        :return: 航班的飞机型号（字符串类型）
        """
        try:
            model = search_table_header.select("span[class='direction_black_border low_text']")[0].string
        except:
            model = ""
        return model.lstrip().rstrip().replace('\n', '').replace('\r', '')

    def __getTime(self, search_table_header):
        """
        解析航班的出发到达时间
        :param search_table_header: 单个航班对应的div标签
        :return: 航班的出发到达时间（字符串类型）
        """
        try:
            time_box = search_table_header.select("div[class='time_box']")
            departureTime = time_box[0].strong.string.lstrip().rstrip().replace('\n', '').replace('\r', '')
            arrivalTime = time_box[1].strong.string.lstrip().rstrip().replace('\n', '').replace('\r', '')
            time = departureTime + " -> " + arrivalTime
        except:
            time = ""
        return time.lstrip().rstrip().replace('\n', '').replace('\r', '')

    def __getAirport(self, search_table_header):
        """
        解析航班的起飞降落机场
        :param search_table_header: 单个航班对应的div标签
        :return: 航班的起飞降落机场（字符串类型）
        """
        try:
            airport = search_table_header.select("div[class='airport']")
            departureAirport = airport[0].string.lstrip().rstrip().replace('\n', '').replace('\r', '')
            arrivalAirport = airport[1].string.lstrip().rstrip().replace('\n', '').replace('\r', '')
            airport = departureAirport + " -> " + arrivalAirport
        except:
            airport = ""
        return airport.lstrip().rstrip().replace('\n', '').replace('\r', '')

    def __getPunctualityRate(self, search_table_header):
        """
        解析航班的准点率
        :param search_table_header: 单个航班对应的div标签
        :return: 航班的准点率（字符串类型）
        """
        try:
            rate = search_table_header.select("span[class='direction_black_border']")[0].string
        except:
            rate = ""
        return rate.lstrip().rstrip().replace('\n', '').replace('\r', '')

    def __getPrice(self, search_table_header):
        """
        解析航班的价格
        :param search_table_header: 单个航班对应的div标签
        :return: 航班的价格（字符串类型）
        """
        try:
            price = search_table_header.select("span[class='base_price02']")[0].get_text()[1:]
        except:
            price = ""
        return price.lstrip().rstrip().replace('\n', '').replace('\r', '')

    def __output(self, flights_list):
        """
        将解析好的指定日期的所有航班信息添加至Spider的类属性thread_list里
        :param flights_list:
        :return:
        """
        if self.lowest["价格"] == 99999:
            dict = {
                "当天最低价格": "当前线路无航班信息",
                "当天所有航班信息": "当前线路无航班信息"
            }
        else:
            dict = {
                "当天最低价格": self.lowest,
                "当天所有航班信息": flights_list
            }
        self.flightsInformation[self.date] = dict
        # print(dict)