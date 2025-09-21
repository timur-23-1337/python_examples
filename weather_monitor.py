#!/usr/bin/python
# -*- coding:utf-8 -*-
#------------------------------------------------------------------------------------------
import sys, os, logging, socket, time, requests
from waveshare_epd import epd2in7
from PIL import Image,ImageDraw,ImageFont
#------------------------------------------------------------------------------------------
API_KEY = ''
CITY_ID = 
url = f"http://api.openweathermap.org/data/2.5/weather?id={CITY_ID}&appid={API_KEY}&units=metric&lang=ru"
#------------------------------------------------------------------------------------------
picdir = "pic"
libdir = "lib"
font = "PTSans.ttf"
if os.path.exists(libdir):
    sys.path.append(libdir)
#------------------------------------------------------------------------------------------
logging.basicConfig(level=logging.ERROR)
#------------------------------------------------------------------------------------------
font_small = ImageFont.truetype(f'{picdir}/fonts/{font}', 32)
font_big = ImageFont.truetype(f'{picdir}/fonts/{font}', 52)
prev_temperature = 0.0
fisrt_start = 1
first_line = -6
second_line = 54
third_line = 92
fourth_line = 130
padding_text_l = 66
padding_text_s = 62
#------------------------------------------------------------------------------------------
thunderstorm = [200, 201, 202, 210, 211, 212, 221, 230, 231, 232]
drizzle = [300, 301, 302, 310, 311, 312, 313, 314, 321]
rain = [500, 501, 502, 503, 504, 511, 520, 521, 522, 531]
snow = [600, 601, 602, 611, 612, 613, 615, 616, 620, 621, 622]
mist = [701, 711, 721, 731, 741, 751, 761, 762, 771, 781]
clear = [800]
clouds = [801, 802, 803, 804]
#------------------------------------------------------------------------------------------
def internet():
    try:
        socket.setdefaulttimeout(3)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
        return True
    except socket.error as ex:
        return False
#------------------------------------------------------------------------------------------
epd = epd2in7.EPD()
Himage = Image.new('1', (epd.height, epd.width), 255)
draw = ImageDraw.Draw(Himage)
#------------------------------------------------------------------------------------------
try:
    while True:
        epd.init()
        epd.Clear(0xFF)
        Himage = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(Himage)
        response = requests.get(url)
        data = response.json()
        #------------------------------------------------------------------------------------------
        if internet() == False:
            Himage.paste(Image.open(os.path.join(picdir, 'no_wifi.bmp')), (6,2))
            Himage.paste(Image.open(os.path.join(picdir, 'none.bmp')), (22,58))
            Himage.paste(Image.open(os.path.join(picdir, 'none.bmp')), (22,96))
            Himage.paste(Image.open(os.path.join(picdir, 'none.bmp')), (22,134))
            draw.text((padding_text_l, first_line), 'Error:', font = font_big, fill = 0)
            draw.text((padding_text_s, second_line), 'No Wi-Fi', font = font_small, fill = 0) 
            draw.text((padding_text_s, third_line), 'connection', font = font_small, fill = 0) 
            draw.text((padding_text_s, fourth_line), 'available', font = font_small, fill = 0) 
            epd.display(epd.getbuffer(Himage))
            epd.sleep()
            time.sleep(60)
        #---
        if response.status_code == 200:
            weather_id = data['weather'][0]['id']
            weather_icon = data['weather'][0]['icon']
            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
        else:
            Himage.paste(Image.open(os.path.join(picdir, 'error.bmp')), (6,2))
            Himage.paste(Image.open(os.path.join(picdir, 'none.bmp')), (22,58))
            Himage.paste(Image.open(os.path.join(picdir, 'none.bmp')), (22,96))
            Himage.paste(Image.open(os.path.join(picdir, 'none.bmp')), (22,134))
            draw.text((padding_text_l, first_line), 'Error:', font = font_big, fill = 0)
            draw.text((padding_text_s, second_line), 'Got bad', font = font_small, fill = 0) 
            draw.text((padding_text_s, third_line), 'response', font = font_small, fill = 0) 
            draw.text((padding_text_s, fourth_line), f'code: {response.status_code}', font = font_small, fill = 0) 
            epd.display(epd.getbuffer(Himage))
            epd.sleep()
            time.sleep(60)
        #------------------------------------------------------------------------------------------
        if weather_id in thunderstorm:
            draw.text((padding_text_l, first_line), 'Гроза', font = font_big, fill = 0)
        elif weather_id in drizzle:
            draw.text((padding_text_l, first_line), 'Морось', font = font_big, fill = 0)
        elif weather_id in rain:
            draw.text((padding_text_l, first_line), 'Дождь', font = font_big, fill = 0)
        elif weather_id in snow:
            draw.text((padding_text_l, first_line), 'Снег', font = font_big, fill = 0)
        elif weather_id in mist:
            draw.text((padding_text_l, first_line), 'Туман', font = font_big, fill = 0)
        elif weather_id in clear:
            draw.text((padding_text_l, first_line), 'Ясно', font = font_big, fill = 0)
        elif weather_id in clouds:
            draw.text((padding_text_l, first_line), 'Облач.', font = font_big, fill = 0)
        else:
            draw.text((padding_text_l, first_line), 'ERROR', font = font_big, fill = 0)
        #---
        if os.path.isfile(f'{picdir}/{weather_icon}.bmp'):
            Himage.paste(Image.open(os.path.join(picdir, f'{weather_icon}.bmp')), (6,2))
        else:
            Himage.paste(Image.open(os.path.join(picdir, 'error.bmp')), (6,2))
        #------------------------------------------------------------------------------------------
        if fisrt_start == 1:
            fisrt_start = 0
            prev_temperature = temperature
        #---
        if prev_temperature < temperature:
            Himage.paste(Image.open(os.path.join(picdir, 'temp_up.bmp')), (22,58))
        elif prev_temperature > temperature:
            Himage.paste(Image.open(os.path.join(picdir, 'temp_down.bmp')), (22,58))
        else: 
            Himage.paste(Image.open(os.path.join(picdir, 'temp.bmp')), (22,58))
        #---
        Himage.paste(Image.open(os.path.join(picdir, 'wind.bmp')), (22,96))
        #---
        if humidity < 30:
            Himage.paste(Image.open(os.path.join(picdir, 'humidity_low.bmp')), (22,134))
        elif humidity > 60:
            Himage.paste(Image.open(os.path.join(picdir, 'humidity_high.bmp')), (22,134))
        else:
            Himage.paste(Image.open(os.path.join(picdir, 'humidity_mid.bmp')), (22,134))
        #------------------------------------------------------------------------------------------
        prev_temperature = temperature
        draw.text((padding_text_s, second_line), f'{temperature} °С', font = font_small, fill = 0) 
        draw.text((padding_text_s, third_line), f'{wind_speed} м/с', font = font_small, fill = 0) 
        draw.text((padding_text_s, fourth_line), f'{humidity}%', font = font_small, fill = 0) 
        #------------------------------------------------------------------------------------------
        epd.display(epd.getbuffer(Himage))
        epd.sleep()
        time.sleep(600)
        #------------------------------------------------------------------------------------------  
except IOError as e:
    logging.info(e)
