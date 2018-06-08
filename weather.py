from requests import get
from enum import IntEnum
import requests
from bs4 import BeautifulSoup

SK_PLANET_APP_KEY = "a8beed5d-0a6e-470a-ac7d-1926c874c1b3"


class Stations(IntEnum):

    def __str__(self):
        return "{}".format(self.value)

    서울 = 108
    김포공항 = 110
    인천 = 112
    인천공항 = 113
    인천연수 = 512
    송도 = 631

def get_weather(station_name, get_alert_info=True):
    try:
        station_id = Stations[station_name]
        req_params = {
            'version': 2, 'stnid': station_id}
        req_header = {
            'Accept': "application/json",
            'Content-Type': "application/json; charset=UTF-8",
            'Accept-Encoding': "gzip, deflate, sdch",
            'appKey': SK_PLANET_APP_KEY
        }
        req = get("https://api2.sktelecom.com/weather/current/minutely",
                  params=req_params, headers=req_header)
        resp = req.json()
        try:
            if not resp.get("result").get("code") == 9200:
                return resp.get("result").get("message")
        except Exception as e:
            return resp.get("error").get("message")

        info = resp.get("weather").get("minutely")[0]
        result_string = "{} 날씨는 현재 {} \n현재온도 {}℃\n최고온도 {}℃\n최저온도 {}℃{}\n" \
                        "바람: {}\n강수중: {}\n강수량(현재): {}{}".format(
            get_station_name(resp),
            info.get("sky").get("name"),
            info.get("temperature").get("tc"),
            info.get("temperature").get("tmax"),
            info.get("temperature").get("tmin"),
            " 습도: {}% ".format(info.get("humidity")) \
                if info.get("humidity")
            else " ",
            get_wind(info),
            # get_wind_direction(info.get("wind").get("wdir")),
            # " 기압: {}hPa ".format(info.get("pressure").get("surface")) \
            #     if info.get("pressure").get("surface") \
            #     else " ",
            get_precipitation(info.get("precipitation")),
            info.get("rain").get("sinceOntime") \
                if info.get("precipitation").get("type") == "1" or \
                   info.get("precipitation").get("type") == "0" \
                else info.get("precipitation").get("sinceOntime"),
            "mm" \
                if info.get("precipitation").get("type") == "1" or \
                   info.get("precipitation").get("type") == "0" \
                else "cm"
        )
        if get_alert_info:
            if resp.get("common").get("alertYn") == "Y":
                result_string += get_alert(*get_station_coord(resp))
            if resp.get("common").get("stormYn") == "Y":
                result_string += get_typhoon(*get_station_coord(resp))
        print(result_string)
        return result_string
    except Exception as e:
        print("에러가 발생하였습니다.", e)


def get_station_coord(resp):
    station = resp.get("weather").get("minutely")[0].get("station")
    return station.get("latitude"), station.get("longitude")


def get_station_name(resp):
    station = resp.get("weather").get("minutely")[0].get("station")
    return "{}".format(station.get("name"))


def get_wind_direction(degree):
    degree = float(degree)
    if degree >= 348.75 or degree < 11.25:
        return "N"
    elif degree >= 11.25 or degree < 33.75:
        return "NNE"
    elif degree >= 33.75 or degree < 56.25:
        return "NE"
    elif degree >= 56.25 or degree < 78.75:
        return "ENE"
    elif degree >= 78.75 or degree < 101.25:
        return "E"
    elif degree >= 101.25 or degree < 123.75:
        return "ESE"
    elif degree >= 123.75 or degree < 146.25:
        return "SE"
    elif degree >= 146.25 or degree < 168.75:
        return "SSE"
    elif degree >= 168.75 or degree < 191.25:
        return "S"
    elif degree >= 191.25 or degree < 213.75:
        return "SSW"
    elif degree >= 213.75 or degree < 236.25:
        return "SW"
    elif degree >= 236.25 or degree < 258.75:
        return "WSW"
    elif degree >= 258.75 or degree < 281.25:
        return "W"
    elif degree >= 281.25 or degree < 303.75:
        return "WNW"
    elif degree >= 303.75 or degree < 326.25:
        return "NW"
    elif degree >= 326.25 or degree < 348.75:
        return "NNW"
    else:
        return "WTF"

def get_wind(info):
    wind = float(info.get("wind").get("wspd"))
    if 0.0 < wind < 1.5 : return "약함"
    elif 1.5 < wind < 7.9 : return "중간"
    elif 7.9 < wind < 15 : return "강함"
    else : return "태풍"
    return wind

def get_precipitation(precipitation_info):
    if precipitation_info.get("type") == "0":
        return "아니오"
    elif precipitation_info.get("type") == "1":
        return "네(비)"
    elif precipitation_info.get("type") == "2":
        return "네(진눈깨비)"
    elif precipitation_info.get("type") == "3":
        return "네(눈)"


def get_alert(lat, lng):
    try:
        req_params = {
            'version': 2, 'lat': lat, 'lon': lng}
        req_header = {
            'Accept': "application/json",
            'Content-Type': "application/json; charset=UTF-8",
            'Accept-Encoding': "gzip, deflate, sdch",
            'appKey': SK_PLANET_APP_KEY
        }
        req = get("https://api2.sktelecom.com/weather/severe/alert",
                  params=req_params, headers=req_header)

        resp = req.json()
        try:
            if not resp.get("result").get("code") == 9200:
                return " 특보 에러: " + resp.get("result").get("message")
        except Exception as e:
            return " 특보 에러: " + resp.get("error").get("message")

        info_list = resp.get("weather").get("alert")
        result_string = " 특보 :"
        if len(info_list) == 0:
            return ""
        for info in info_list:
            string = " ({})발효시간: {}, 지역: {} 특보내용: {} 비고: {}".format(
                info_list.index(info) + 1,
                info.get("timeRelease"),
                info.get("areaName"),
                info.get("alert60").get("t1"),
                info.get("alert60").get("other")
            )
            print(string)
            result_string += string
        return result_string
    except Exception as e:
        print(e)
        return " 날씨특보를 가져오는데 실패하였습니다."


def get_typhoon(lat, lng):
    try:
        req_params = {
            'version': 1, 'lat': lat, 'lon': lng}
        req_header = {
            'Accept': "application/json",
            'Accept-Encoding': "gzip, deflate, sdch",
            'appKey': SK_PLANET_APP_KEY
        }
        req = get("https://api2.sktelecom.com/weather/severe/storm",
                  params=req_params, headers=req_header)
        resp = req.json()

        try:
            if not resp.get("result").get("code") == 9200:
                return " 특보 에러: " + resp.get("result").get("message")
        except Exception as e:
            return " 특보 에러: " + resp.get("error").get("message")

        info_list = resp.get("weather").get("alert")
        if len(info_list) == 0:
            return ""
        result_string = " 태풍정보 :"
        for info in info_list:
            string = " ({})태풍 제{}호({}) 태풍 등급: {} 현재 위치: {} 중심기압: {}hPa 최대풍속: {}m/s".format(
                info_list.index(info) + 1,
                info.get("number"),
                info.get("nameKor"),
                info.get("status").get("level"),
                info.get("status").get("loc"),
                info.get("status").get("ps"),
                info.get("status").get("ws")
            )
            result_string += string
        return result_string
    except Exception as e:
        print(e)
        return " 태풍정보를 가져오는데 실패하였습니다."

def getDust():
    url = 'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty?serviceKey=bLmQ%2B7Tm65ViZCRhNV9kg6wcAgOlFzB8lLHRTriGsaNWiujBUPh6X%2FvWm2zxPYc0urKxg7EpSZVDhbUUIYTrWw%3D%3D&numOfRows=10&pageSize=10&pageNo=1&startPage=1&stationName=%EC%86%A1%EB%8F%84&dataTerm=DAILY&ver=1.3'
    response = requests.get(url)
    soup = BeautifulSoup(response.content.decode('utf-8', 'replace'), 'html.parser')
    root = soup.find("item")
    air_grade = (root.find("pm10grade").text)
    air_value = (root.find("pm10value").text)
    air_quality = ""
    if air_grade == "1": air_quality = "좋음"
    elif air_grade == "2": air_quality = "보통"
    elif air_grade == "3": air_quality = "나쁨"
    elif air_grade == "4": air_quality = "매우 나쁨"
    return "\n미세먼지 수치 : " + str(air_value) + " (" + str(air_quality) + ") " + "입니다."



nowWeather = get_weather("송도")