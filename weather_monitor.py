#!/usr/bin/python
# -*- coding:utf-8 -*-
#------------------------------------------------------------------------------------------
import sys, os, logging, socket, time, requests, datetime
import RPi.GPIO as GPIO
from waveshare_epd import epd2in7
from PIL import Image,ImageDraw,ImageFont
#------------------------------------------------------------------------------------------
API_KEY = ''
CITY_ID = 
VERBOSE = False
url = f"https://api.openweathermap.org/data/2.5/weather?id={CITY_ID}&appid={API_KEY}&units=metric&lang=ru"
#------------------------------------------------------------------------------------------
picdir = "pic"
libdir = "lib"
font = "PTSans.ttf"
if os.path.exists(libdir):
    sys.path.append(libdir)
#------------------------------------------------------------------------------------------
if VERBOSE:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.ERROR)
#------------------------------------------------------------------------------------------
font_small = ImageFont.truetype(f'{picdir}/fonts/{font}', 32)
font_big = ImageFont.truetype(f'{picdir}/fonts/{font}', 52)
font_clock = ImageFont.truetype(f'{picdir}/fonts/Ubuntu.ttf', 96)
font_rasp = ImageFont.truetype(f'{picdir}/fonts/Ubuntu.ttf', 24)
prev_temperature = 0.0
fisrt_start = 1
first_line, second_line, third_line, fourth_line = -6 , 54, 92, 130
padding_text_l, padding_text_s = 66, 62
#------------------------------------------------------------------------------------------
http_proxy  = "10.0.2.52:3128"
https_proxy = "10.0.2.52:3128"
proxies = { 
              "http"  : http_proxy, 
              "https" : https_proxy, 
            }
#------------------------------------------------------------------------------------------
GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#------------------------------------------------------------------------------------------
thunderstorm = [200, 201, 202, 210, 211, 212, 221, 230, 231, 232]
drizzle = [300, 301, 302, 310, 311, 312, 313, 314, 321]
rain = [500, 501, 502, 503, 504, 511, 520, 521, 522, 531]
snow = [600, 601, 602, 611, 612, 613, 615, 616, 620, 621, 622]
mist = [701, 711, 721, 731, 741, 751, 761, 762, 771, 781]
clear = [800]
clouds = [801, 802, 803, 804]
#------------------------------------------------------------------------------------------
schedule = {
    'lessons': [
        {'start': 8*60, 'end': 8*60+40, 'shift': 1},
        {'start': 8*60+45, 'end': 9*60+25, 'shift': 1},
        {'start': 9*60+35, 'end': 10*60+15, 'shift': 1},
        {'start': 10*60+25, 'end': 11*60+5, 'shift': 1},
        {'start': 11*60+15, 'end': 11*60+55, 'shift': 1},
        {'start': 12*60+5, 'end': 12*60+45, 'shift': 1},
        {'start': 12*60+50, 'end': 13*60+30, 'shift': 1},
        #---
        {'start': 13*60+40, 'end': 14*60+20, 'shift': 2},
        {'start': 14*60+30, 'end': 15*60+10, 'shift': 2},
        {'start': 15*60+20, 'end': 16*60+0, 'shift': 2},
        {'start': 16*60+10, 'end': 16*60+50, 'shift': 2},
        {'start': 16*60+55, 'end': 17*60+35, 'shift': 2},
        {'start': 17*60+40, 'end': 18*60+20, 'shift': 2},
        {'start': 18*60+25, 'end': 19*60+5, 'shift': 2},
    ],
    'breaks': [
        {'start': 8*60+40, 'end': 8*60+45},
        {'start': 9*60+25, 'end': 9*60+35},
        {'start': 10*60+15, 'end': 10*60+25},
        {'start': 11*60+5, 'end': 11*60+15},
        {'start': 11*60+55, 'end': 12*60+5},
        {'start': 12*60+45, 'end': 12*60+50},
        {'start': 13*60+30, 'end': 13*60+40},
        {'start': 14*60+20, 'end': 14*60+30},
        {'start': 15*60+10, 'end': 15*60+20},
        {'start': 16*60+0, 'end': 16*60+10},
        {'start': 16*60+50, 'end': 16*60+55}, 
        {'start': 17*60+35, 'end': 17*60+40},
        {'start': 18*60+20, 'end': 18*60+25},
    ]
}
#------------------------------------------------------------------------------------------
def rasp():
    clock = datetime.datetime.now()
    if VERBOSE:
        print(f'VERBOSE: Current time is{clock.hour}:{clock.minute}')
    if (clock.hour <= 13) or (clock.hour == 13 and clock.minute <= 32):
        if (clock.hour == 8 and clock.minute >= 0 and clock.minute <= 40):
            draw.text((6, 2), '>', font = font_rasp, fill = 0)
        draw.text((24, 2), '8:00 - 8:40', font = font_rasp, fill = 0)
        #---
        if (clock.hour == 8 and clock.minute >= 45) or (clock.hour == 9 and clock.minute <= 25):
            draw.text((6, 26), '>', font = font_rasp, fill = 0)
        draw.text((24, 26), '8:45 - 9:25', font = font_rasp, fill = 0)
        #---
        if (clock.hour == 9 and clock.minute >= 35) or (clock.hour == 10 and clock.minute <= 15):
            draw.text((6, 50), '>', font = font_rasp, fill = 0)
        draw.text((24, 50), '9:35 - 10:15', font = font_rasp, fill = 0)
        #---
        if (clock.hour == 10 and clock.minute >= 25) or (clock.hour == 11 and clock.minute <= 5):
            draw.text((6, 74), '>', font = font_rasp, fill = 0)
        draw.text((24, 74), '10:25 - 11:05', font = font_rasp, fill = 0)
        #---
        if (clock.hour == 11 and clock.minute >= 15 and clock.minute <= 55):
            draw.text((6, 98), '>', font = font_rasp, fill = 0)
        draw.text((24, 98), '11:15 - 11:55', font = font_rasp, fill = 0)
        #---
        if (clock.hour == 12 and clock.minute >= 5 and clock.minute <= 45):
            draw.text((6, 122), '>', font = font_rasp, fill = 0)
        draw.text((24, 122), '12:05 - 12:45', font = font_rasp, fill = 0)
        #---
        if (clock.hour == 12 and clock.minute >= 50) or (clock.hour == 13 and clock.minute <= 30):
            draw.text((6, 146), '>', font = font_rasp, fill = 0)
        draw.text((24, 146), '12:50 - 13:30', font = font_rasp, fill = 0)
        #---
    else:
        if (clock.hour == 13 and clock.minute >= 40) or (clock.hour == 14 and clock.minute <= 20):
            draw.text((6, 2), '>', font = font_rasp, fill = 0)
        draw.text((24, 2), '13:40 - 14:20', font = font_rasp, fill = 0)
        #---
        if (clock.hour == 14 and clock.minute >= 30) or (clock.hour == 15 and clock.minute <= 10):
            draw.text((6, 26), '>', font = font_rasp, fill = 0)
        draw.text((24, 26), '14:30 - 15:10', font = font_rasp, fill = 0)
        #---
        if (clock.hour == 15 and clock.minute >= 20) or (clock.hour == 16 and clock.minute == 0):
            draw.text((6, 50), '>', font = font_rasp, fill = 0)
        draw.text((24, 50), '15:20 - 16:00', font = font_rasp, fill = 0)
        #---
        if (clock.hour == 16 and clock.minute >= 10 and clock.minute <= 50):
            draw.text((6, 74), '>', font = font_rasp, fill = 0)
        draw.text((24, 74), '16:10 - 16:50', font = font_rasp, fill = 0)
        #---
        if (clock.hour == 16 and clock.minute >= 55) or (clock.hour == 17 and clock.minute <= 35):
            draw.text((6, 98), '>', font = font_rasp, fill = 0)
        draw.text((24, 98), '16:55 - 17:35', font = font_rasp, fill = 0)
        #---
        if (clock.hour == 17 and clock.minute >= 40) or (clock.hour == 18 and clock.minute <= 20):
            draw.text((6, 122), '>', font = font_rasp, fill = 0)
        draw.text((24, 122), '17:40 - 18:20', font = font_rasp, fill = 0)
        #---
        if (clock.hour == 18 and clock.minute >= 25) or (clock.hour == 19 and clock.minute <= 5):
            draw.text((6, 146), '>', font = font_rasp, fill = 0)
        draw.text((24, 146), '18:25 - 19:05', font = font_rasp, fill = 0)
        #---
    epd.display(epd.getbuffer(Himage))
#------------------------------------------------------------------------------------------
def init_display():
    if VERBOSE:
        print("VERBOSE: Display initialized")
    epd.init()
    epd.Clear(0xFF)
    global Himage
    global draw
    Himage = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(Himage)
#------------------------------------------------------------------------------------------
def internet():
    try:
        socket.setdefaulttimeout(3)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("ya.ru", 443))
        if VERBOSE:
            print("VERBOSE: Internet connection is available")
        return True
    except socket.error as ex:
        if VERBOSE:
            print("VERBOSE: Internet connection is unavailable")
        return False
#------------------------------------------------------------------------------------------
def get_current_event():
    now = datetime.datetime.now()
    current_minutes = now.hour * 60 + now.minute
    #---
    for lesson in schedule['lessons']:
        if lesson['start'] <= current_minutes < lesson['end']:
            return {
                'type': 'lesson',
                'shift': lesson['shift'],
                'end_time': lesson['end'],
                'number': schedule['lessons'].index(lesson) + 1
            }
    #---
    for break_time in schedule['breaks']:
        if break_time['start'] <= current_minutes < break_time['end']:
            return {
                'type': 'break',
                'end_time': break_time['end']
            }
    return {'type': 'offtime'}
#------------------------------------------------------------------------------------------
def desk_clock():
    clock = time.strftime("%H:%M")
    current_time = datetime.datetime.now()
    event = get_current_event()
    #---
    if event['type'] == 'lesson':
        number = event['number']
        end_time = event['end_time']
        left = end_time - (current_time.hour * 60 + current_time.minute)
        hour = end_time // 60
        minute = end_time % 60
        #---
        if number > 8:
            number = number - 7
        draw.text((10, 0), f'Сейчас {number} урок', font = font_small, fill = 0)
        #---
        if minute == 0:
            draw.text((10, 102), f'Конец в {hour}:00', font = font_small, fill = 0)
        else:
            draw.text((10, 102), f'Конец в {hour}:{minute}', font = font_small, fill = 0)
        #---
        draw.text((10, 134), f'Осталось {left} мин.', font = font_small, fill = 0)
    #---
    elif event['type'] == 'break':
        end_time = event['end_time']
        left = end_time - (current_time.hour * 60 + current_time.minute)
        hour = end_time // 60
        minute = end_time % 60
        draw.text((10, 0), 'Сейчас перемена', font = font_small, fill = 0)
        #---
        if minute == 0:
            draw.text((10, 102), f'Конец в {hour}:00', font = font_small, fill = 0)
        else:
            draw.text((10, 102), f'Конец в {hour}:{minute}', font = font_small, fill = 0)
        #---
        draw.text((10, 134), f'Осталось {left} мин.', font = font_small, fill = 0)
    #---
    else:
        draw.text((10, 16), 'Занятий нет', font = font_small, fill = 0)
    #---
    draw.text((8, 22), f'{clock}', font = font_clock, fill = 0)
    if VERBOSE:
        print("VERBOSE: Current event data is: ", get_current_event())
    epd.display(epd.getbuffer(Himage))
#------------------------------------------------------------------------------------------
def waiting():
    if VERBOSE:
        print("VERBOSE: Display is now sleeping")
    start_time = time.time()
    while True:
        time.sleep(0.1)
        if time.time() - start_time <= 600:
            #---
            if GPIO.input(5) == GPIO.LOW:
                if VERBOSE:
                    print("VERBOSE: Key 1 is pressed")
                break
            #---
            elif GPIO.input(6) == GPIO.LOW:
                if VERBOSE:
                    print("VERBOSE: Key 2 is pressed")
                init_display()
                desk_clock()
                epd.sleep()
                time.sleep(10)
                break
            #---
            elif GPIO.input(13) == GPIO.LOW:
                if VERBOSE:
                    print("VERBOSE: Key 3 is pressed")
                init_display()
                rasp()
                epd.sleep()
                time.sleep(10)
                break
            #---
            elif GPIO.input(19) == GPIO.LOW:
                if VERBOSE:
                    print("VERBOSE: Key 4 is pressed")
                clock = time.strftime("%H:%M")
                init_display()
                Himage.paste(Image.open(os.path.join(picdir, 'error.bmp')), (6,2))
                Himage.paste(Image.open(os.path.join(picdir, 'none.bmp')), (22,58))
                Himage.paste(Image.open(os.path.join(picdir, 'none.bmp')), (22,96))
                Himage.paste(Image.open(os.path.join(picdir, 'none.bmp')), (22,134))
                draw.text((padding_text_l, first_line), 'Exit:', font = font_big, fill = 0)
                draw.text((padding_text_s, second_line), 'Program', font = font_small, fill = 0) 
                draw.text((padding_text_s, third_line), "ended it's job", font = font_small, fill = 0) 
                draw.text((padding_text_s, fourth_line), f'at {clock}', font = font_small, fill = 0) 
                epd.display(epd.getbuffer(Himage))
                epd.sleep()
                quit()
        else:
            break
#------------------------------------------------------------------------------------------
epd = epd2in7.EPD()
Himage = Image.new('1', (epd.height, epd.width), 255)
draw = ImageDraw.Draw(Himage)
#------------------------------------------------------------------------------------------
try:
    while True:
        init_display()
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
            waiting()
            continue
        #---
        try:
            response = requests.get(url)
            data = response.json()
            if response.status_code == 200:
                weather_id = data['weather'][0]['id']
                weather_icon = data['weather'][0]['icon']
                temperature = data['main']['temp']
                humidity = data['main']['humidity']
                wind_speed = data['wind']['speed']
            else:
                if VERBOSE:
                    print("VERBOSE: There was an unknown error")
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
                waiting()
                continue
        except OSError as e:
            if VERBOSE:
                print("VERBOSE: There was an OSError")
            Himage.paste(Image.open(os.path.join(picdir, 'error.bmp')), (6,2))
            Himage.paste(Image.open(os.path.join(picdir, 'none.bmp')), (22,58))
            Himage.paste(Image.open(os.path.join(picdir, 'none.bmp')), (22,96))
            Himage.paste(Image.open(os.path.join(picdir, 'none.bmp')), (22,134))
            draw.text((padding_text_l, first_line), 'Error:', font = font_big, fill = 0)
            draw.text((padding_text_s, second_line), 'Got OSError', font = font_small, fill = 0) 
            draw.text((padding_text_s, third_line), 'exception!', font = font_small, fill = 0) 
            draw.text((padding_text_s, fourth_line), '', font = font_small, fill = 0) 
            epd.display(epd.getbuffer(Himage))
            epd.sleep()
            waiting()
            continue
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
            if VERBOSE:
                print(f'VERBOSE: Weather icon is not found for icon id: {weather_icon}')
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
        waiting()
        #------------------------------------------------------------------------------------------  
except IOError as e:
    if VERBOSE:
        print("VERBOSE: Cleanup GPIO")
    #logging.info(e)
finally:
    if VERBOSE:
        print("VERBOSE: Cleanup GPIO")
    GPIO.cleanup()
