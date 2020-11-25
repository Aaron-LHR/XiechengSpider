# -*- coding:UTF-8 -*-

import threading
from bs4 import BeautifulSoup


class Parser (threading.Thread):
    def __init__(self, html, date, flightsInformation):
        super().__init__()
        self.lowest = {"价格": 99999}
        self.html= html
        self.date = date
        self.flightsInformation = flightsInformation

    def run(self):
        bs = BeautifulSoup(self.html, "html.parser")
        flights_div = bs.select("div[class='search_table_header']")
        flights_list = []
        for flight in flights_div:
            flights_list.append(self.__parseFlightInformation(flight))
        # print(len(flights_list))
        self.__output(flights_list)

    def __parseFlightInformation(self, flight):
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
        try:
            flightCompany = search_table_header.select("div[class='logo-item flight_logo']")[
                0].div.span.span.strong.get_text()
        except:
            flightCompany = ""
        return flightCompany.lstrip().rstrip().replace('\n', '').replace('\r', '')

    def __getNumber(self, search_table_header):
        try:
            flightNumber = search_table_header.select("div[class='logo-item flight_logo']")[0].div.span.span.span.string
        except:
            flightNumber = ""
        return flightNumber.lstrip().rstrip().replace('\n', '').replace('\r', '')

    def __getModel(self, search_table_header):
        try:
            model = search_table_header.select("span[class='direction_black_border low_text']")[0].string
        except:
            model = ""
        return model.lstrip().rstrip().replace('\n', '').replace('\r', '')

    def __getTime(self, search_table_header):
        try:
            time_box = search_table_header.select("div[class='time_box']")
            departureTime = time_box[0].strong.string.lstrip().rstrip().replace('\n', '').replace('\r', '')
            arrivalTime = time_box[1].strong.string.lstrip().rstrip().replace('\n', '').replace('\r', '')
            time = departureTime + " -> " + arrivalTime
        except:
            time = ""
        return time.lstrip().rstrip().replace('\n', '').replace('\r', '')

    def __getAirport(self, search_table_header):
        try:
            airport = search_table_header.select("div[class='airport']")
            departureAirport = airport[0].string.lstrip().rstrip().replace('\n', '').replace('\r', '')
            arrivalAirport = airport[1].string.lstrip().rstrip().replace('\n', '').replace('\r', '')
            airport = departureAirport + " -> " + arrivalAirport
        except:
            airport = ""
        return airport.lstrip().rstrip().replace('\n', '').replace('\r', '')

    def __getPunctualityRate(self, search_table_header):
        try:
            rate = search_table_header.select("span[class='direction_black_border']")[0].string
        except:
            rate = ""
        return rate.lstrip().rstrip().replace('\n', '').replace('\r', '')

    def __getPrice(self, search_table_header):
        try:
            price = search_table_header.select("span[class='base_price02']")[0].get_text()[1:]
        except:
            price = ""
        return price.lstrip().rstrip().replace('\n', '').replace('\r', '')

    def __output(self, flights_list):
        # print("您搜索的" + time + "从" + placeOfDeparture + "出发到" + placeOfArrival + "的航班信息如下")
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