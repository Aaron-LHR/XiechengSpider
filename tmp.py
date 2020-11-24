import requests
import json


if __name__ == "__main__":

    url = "https://flights.ctrip.com/itinerary/api/12808/products"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0",
        "Referer": "https://flights.ctrip.com/itinerary/oneway/bjs-sha?date=2019-07-18",
        "Content-Type": "application/json"
    }
    request_payload = {
        "flightWay": "Oneway",
        "classType": "ALL",
        "hasChild": False,
        "hasBaby": False,
        "searchIndex": 1,
        "token": "878606806e48f96c7842cd933e4a8a15",
        "date": "2020-11-25",
              "airportParams": [
            {"dcity": "BJS", "acity": "SHA", "dcityname": "北京", "acityname": "上海", "date": "2020-11-25"}
        ]
    }

    # post请求
    response = requests.post(url, data=json.dumps(request_payload), headers=headers).text
    # print(response)
    routeList = json.loads(response).get('data').get('routeList')
    print(type(routeList))
    # 依次读取每条信息
    for route in routeList:
        # 判断是否有信息，有时候没有会报错
        if len(route.get('legs')) == 1:
            legs = route.get('legs')
            flight = legs[0].get('flight')
            # 提取想要的信息
            # print(flight)
            airlineName = flight.get('airlineName')
            flightNumber = flight.get('flightNumber')
            departureDate = flight.get('departureDate')
            arrivalDate = flight.get('arrivalDate')
            departureCityName = flight.get('departureAirportInfo').get('cityName')
            departureAirportName = flight.get('departureAirportInfo').get('airportName')
            arrivalCityName = flight.get('arrivalAirportInfo').get('cityName')
            arrivalAirportName = flight.get('arrivalAirportInfo').get('airportName')

            print(airlineName, "\t",
                  flightNumber, "\t",
                  departureDate, "\t",
                  arrivalDate, "\t",
                  departureCityName, "\t",
                  departureAirportName, "\t",
                  arrivalCityName, "\t",
                  arrivalAirportName)
