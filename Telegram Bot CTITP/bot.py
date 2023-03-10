import config
#import requests
#import json
import time
import telebot
import random
#import base64
from telebot import types
#import smtplib
import pandas as pd
from telebot import types
from datetime import date
import re

v_phone = ''
v_lastname = ''
v_firstname = ''
v_step = ''

NUM_RE = re.compile(r".*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*")


bot = telebot.TeleBot(config.token)
users = [230946227]
hideBoard = types.ReplyKeyboardRemove()

file1 = '/usr/src/app/dockerdata/contact.xlsx'
xlsx = pd.ExcelFile(file1)
df1 = xlsx.parse('contact')

#file2 = '/usr/src/app/dockerdata/salarycalendar.xlsx'
#xlsx2 = pd.ExcelFile(file2)
#df2 = xlsx2.parse('calendar')


    

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
#
#
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
def userid_list():
    dff = pd.read_csv("/usr/src/app/dockerdata/ids.log", sep=";", header=0)
    dff = dff['ID']
    dff = dff.tolist()
    return dff
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
#
#
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
# help
# function to handle the /help command
@bot.message_handler(commands=['help'], func=lambda message: message.from_user.id in userid_list())
def fn_main_help(message):
    print('6' + ' | message.from_user.id = ' + str(message.from_user.id) + ' | message.chat.id = ' + str(message.chat.id) + ' | message.text = ' + str(message.text))
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(1)
    
    bot.send_message(message.chat.id, '?? ?????????????? ?? ???????????????? ????????????. ???????? ???? ?????????????? ???????????? ?????? ???????????????????????? ??????????????????, ???? ?????????????????????? ???????????? ?? ??????????????????.', reply_markup=hideBoard)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
#
#
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
# start
# function to handle the /start command
@bot.message_handler(commands=['start'])
def fn_main_start(message):
    print('10' + ' | message.from_user.id = ' + str(message.from_user.id) + ' | message.chat.id = ' + str(message.chat.id) + ' | message.text = ' + str(message.text))
    mes = f'????????????. ?? ?????????????????????????? ?????? ???????????????? ??????????.'
    bot.send_message(message.chat.id,mes, parse_mode='html')
    phone_btn = telebot.types.ReplyKeyboardMarkup(True, True)
    phone_btn.add(types.KeyboardButton(text='?????????????????? ??????????????', request_contact=True))
    msg = bot.send_message(message.chat.id, '?????????? ???????????? *?????????????????? ??????????????* ???? ????????', parse_mode='Markdown',
                           reply_markup=phone_btn)
    bot.register_next_step_handler(msg, start_4)
    
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

def start_4(message):
    time.sleep(1)
    #print(message)
    if (message.contact is not None and message.from_user.id == message.contact.user_id):
        bot.send_message(message.chat.id, '???????????????? ???????????? ...', reply_markup=hideBoard)
        time.sleep(3)
        start_access(message, message.contact.phone_number)           
    else:
        bot.send_message(message.chat.id, '???? ???????????????? ???? ???????? ?????????????? ????', reply_markup=hideBoard)
        
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
def start_access(message, phone):
    NUM_RE = re.compile(r".*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*")
    df1["Phone"] = df1["Phone"].apply(str)
    df1["Phone"] = df1["Phone"].apply(lambda x: "+7" + ''.join(NUM_RE.match(x).groups()))
    adf1 = df1["Phone"]
    adf1 = adf1.tolist()
    print(adf1)
    func=lambda phone: phone in adf1
    ph = lambda x: "+7" + ''.join(NUM_RE.match(x).groups())
    if not(func(ph(phone))):
        bot.send_message(message.chat.id,'?? ?????? ?????? ?????????????? ?????? ???????????? ????????????????????', reply_markup=hideBoard)
    else:
        start_5(message, message.contact.phone_number)
        
def start_5(message, phone):
    d1 = {'ID': [message.from_user.id], 'phone': [phone]}
    df = pd.DataFrame(d1)
    df.to_csv("/usr/src/app/dockerdata/ids.log", sep=";", mode='a', header=False)
    bot.send_message(message.chat.id, '???? ???????????????????????????????? ?? ??????????????', reply_markup=hideBoard)
    
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
#
#
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
# help
# function to handle the /contact command
@bot.message_handler(commands=['contact'], func=lambda message: message.from_user.id in userid_list())
def fn_main_contact(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton("??? ????????????")
    markup.add(btn1)
    msg = bot.send_message(message.chat.id, "???????? ???????????? ???? ??????????????, e-mail, ???????????????????? ?? ???????????????? ????????????????. ?????????????? ???????? ?? ???????????????????????? ????????????, ?? ?????????? ?????????????????? ????????????????????, ???????????? ?????? Ivanov@gp.ru, ???????????? ???????? ?? ???????? ?????????????? ?? ???????????????????? ???????????? (????????????, ????????????, ??????????????)", reply_markup=markup)
    bot.register_next_step_handler(msg, fn3, '', '', '')
        
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
def fn3(message, v_phone, v_firstname, v_lastname):
    if (message.text == "??? ????????????"):
        bot.send_message(message.chat.id, '?????????? ???????? ?? ???????????? ?????? ????', parse_mode='html', reply_markup=hideBoard)
    elif (message.text == "?????????????????? ??????????????"):
        bot.send_contact(message.chat.id, phone_number=v_phone, first_name=v_firstname,last_name=v_lastname, reply_markup=hideBoard)
    elif (message.text == "?????????? ??????"):
        fn_main_contact(message)
    elif (message.text == "??????????????"):
        bot.send_message(message.chat.id, '?????????????????? ????', parse_mode='html', reply_markup=hideBoard)
    elif (message.text == "????"):
        fn_main_contact(message)
    else:
        fn_contact_find(message)
    #elif v_step == 2:
    #    fn_contact_find(message)
    #elif v_step == 1:
    #    bot.send_message(message.chat.id, '????????????, ?? ???????? ???? ??????????. ???????? ??????, ?? ???????? ???????? /help', parse_mode='html')
        
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
def fn_contact_find(message):
    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton("?????????????????? ??????????????")
    btn2 = types.KeyboardButton("?????????? ??????")
    btn3 = types.KeyboardButton("??????????????")
    markup1.add(btn1, btn2, btn3)

    markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn4 = types.KeyboardButton("????")
    btn5 = types.KeyboardButton("??? ????????????")
    markup2.add(btn4, btn5)

    f1 = ''
    flag = 0 # 1 - email 2 phone 3 Surname
    mess = message.text.strip().lower()

    messphone = mess.replace("+", "").replace("(", "").replace(")", "").replace("-", "").replace(" ", "")

    v_phone = '' 
    v_lastname = ''
    v_firstname = ''

    if "@" in mess:
        flag = 1
        for i in df1['Email']:
            if i.lower().strip() == mess:
                f1 = i
    elif messphone.isdigit():
        NUM_RE = re.compile(r".*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*")
        ph = lambda x: "+7" + ''.join(NUM_RE.match(x).groups())
        messphone = ph(messphone)
        flag = 2
        for i in df1['Phone'].apply(str).apply(lambda x: "+7" + ''.join(NUM_RE.match(x).groups())):
            if i == messphone:
                f1 = i
    elif mess.isalpha():
        flag = 3
        for i in df1['Surname']:
            if i.strip().lower() == mess:
                f1 = i
    if f1 == '' and flag == 0:
        msg = bot.send_message(message.chat.id, f'?? ???? ???????? ?????????? ?????????????? ???? ?????????????? <b>{message.text}</b>. ???????????? <b> {message.text}</b> ???? ?????????? ???? email, ?????????????? ?????? ?????????????? ??? ???????????????? ?????????????????? ????????????.???? ?????????????????? ?????? ???????', parse_mode='html', reply_markup=markup2)
        bot.register_next_step_handler(msg, fn3, '', '', '')
    elif flag == 1 and f1 != '':
        m = ''
        d = df1[df1['Email'] == f1]
        for index, row in d.iterrows():
            v_phone =  str(row['Phone']).strip()
            v_lastname = str(row['Surname']).strip()
            v_firstname = str(row['Name']).strip()
            m += '\n\n' + str(row['Surname']).strip() + ' ' + str(row['Name']).strip() + '\n' + str(row['Department']).strip()  + '\n' + '??????????????????: ' + str(row['Phone']).strip() + '\n' + 'E-mail: ' + str(row['Email']).strip() + '\n\n'
        msg = bot.send_message(message.chat.id, f'?? ?????????? ?????????????? ???? <b>email</b>: {m} ?????????????????? ?????? ??????? /contact', parse_mode='html', reply_markup=markup1)
        bot.register_next_step_handler(msg, fn3, v_phone, v_lastname, v_firstname)
    elif flag == 2 and f1 != '':
        NUM_RE = re.compile(r".*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*")
        m = ''
        d = df1[df1['Phone'].apply(str).apply(lambda x: "+7" + ''.join(NUM_RE.match(x).groups())) == f1]
        for index, row in d.iterrows():
            v_phone =  str(row['Phone']).strip()
            v_lastname = str(row['Surname']).strip()
            v_firstname = str(row['Name']).strip()
            m += '\n\n' + str(row['Surname']).strip() + ' ' + str(row['Name']).strip() + '\n' + str(row['Department']).strip()  + '\n' + '??????????????????: ' + str(row['Phone']).strip() + '\n' + 'E-mail: ' + str(row['Email']).strip() + '\n\n'
        msg = bot.send_message(message.chat.id, f'?? ?????????? ?????????????? ???? <b>???????????? ????????????????</b>: {m} ?????????????????? ?????? ??????? /contact', parse_mode='html', reply_markup=markup1)
        bot.register_next_step_handler(msg, fn3, v_phone, v_lastname, v_firstname)
    elif flag == 3 and f1 != '':
        m = ''
        d = df1[df1['Surname'] == f1]
        for index, row in d.iterrows():
            v_phone = str(row['Phone']).strip()
            v_lastname = str(row['Surname']).strip()
            v_firstname = str(row['Name']).strip()
            m += '\n\n' + str(row['Surname']).strip() + ' ' + str(row['Name']).strip() + '\n' + str(row['Department']).strip()  + '\n' + '??????????????????: ' + str(row['Phone']).strip() + '\n' + 'E-mail: ' + str(row['Email']).strip() + '\n\n'
        msg = bot.send_message(message.chat.id, f'?? ?????????? ?????????????? ???? <b>??????????????</b>: {m} ?????????????????? ?????? ??????? /contact', parse_mode='html', reply_markup=markup1)
        bot.register_next_step_handler(msg, fn3, v_phone, v_lastname, v_firstname)
    #???????? ???? ?????????? ???? ????????????????
    elif flag == 1 and f1 == '':
        m = df1[df1['Email'] == f1]
        msg = bot.send_message(message.chat.id, f'?? ???? ?????????? ?????????????? ???? <b>email</b> <b>{message.text}</b> ???? ??????????????. ?????????????????? ?????? ???????', parse_mode='html', reply_markup=markup2)
        bot.register_next_step_handler(msg, fn3, '', '', '')
    elif flag == 2 and f1 == '':
        m = df1[df1['Phone'] == f1]
        msg = bot.send_message(message.chat.id, f'?? ???? ?????????? ?????????????? ???? <b>???????????? ????????????????</b> <b>{message.text}</b> ???? ??????????????. ?????????????????? ?????? ???????', parse_mode='html', reply_markup=markup2)
        bot.register_next_step_handler(msg, fn3, '', '', '')
    elif flag == 3 and f1 == '':
        m = df1[df1['Surname'] == f1]
        msg = bot.send_message(message.chat.id, f'?? ???? ?????????? ?????????????? ???? <b>??????????????</b> <b>{message.text}</b> ???? ??????????????. ?????????????????? ?????? ???????', parse_mode='html', reply_markup=markup2)
        bot.register_next_step_handler(msg, fn3, '', '', '')

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
#
#
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
# website
# function to handle the /website command
@bot.message_handler(commands=['website'], func=lambda message: message.from_user.id in userid_list())
def fn_main_website(message):
    markup1 = types.InlineKeyboardMarkup()
    markup1.add(types.InlineKeyboardButton("?????????????? ???? ctitp.ru", url="https://ctitp.ru/"))
    bot.send_message(message.chat.id, "???????? ctitp.ru", reply_markup=markup1)

    markup2 = types.InlineKeyboardMarkup()
    markup2.add(types.InlineKeyboardButton("?????????????? ???? wiki", url="https://wiki.yandex.ru/"))
    bot.send_message(message.chat.id, "????????", reply_markup=markup2)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
#
#
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
# calendar
# function to handle the /calendar command
@bot.message_handler(commands=['calendar'], func=lambda message: message.from_user.id in userid_list())
def fn_main_calendar(message):
    from datetime import datetime
    import json
    from pytz import UTC # timezone
    import caldav
    from icalendar import Calendar, Event
    
    # CalDAV info
    url = "https://caldav.yandex.ru/calendars/polirov.d%40ctitp.ru/events-19645967/"
    userN = "polirov.d@ctitp.ru"
    passW = "qaqcdjpfdhaxlele"
    
    client = caldav.DAVClient(url=url, username=userN, password=passW)
    principal = client.principal()
    calendars = principal.calendars()
    
    if len(calendars) > 0:
        calendar = calendars[0]
        #print ("Using calendar", calendar)
        #results = calendar.events()
        #print(results)
        
        #print('------------')
        results = calendar.search(start=datetime(2022, 12, 13), end=datetime(2022, 12, 14),event=True)
        print(results)
        #print(datetime(2022, 12, 6))
        eventSummary = []
        eventDescription = []
        eventDateStart = []
        eventdateEnd = []
        eventTimeStart = []
        eventTimeEnd = []
        
        msg = '?? ?????? ?????????????????? ?????????????????? ??????????????: \n'
        
        for eventraw in results:
        
            event = Calendar.from_ical(eventraw._data)
            #print(event)
            for component in event.walk():
                if component.name == "VEVENT":
                    #print (component.get('summary'))
                    eventSummary.append(component.get('summary'))
                    
                    #print (component.get('description'))
                    eventDescription.append(component.get('description'))
                    
                    
                    startDate = component.get('dtstart')
                    #print (startDate.dt.strftime('%m/%d/%Y %H:%M'))
                    eventDateStart.append(startDate.dt.strftime('%m/%d/%Y'))
                    eventTimeStart.append(startDate.dt.strftime('%H:%M'))
                    
                    
                    endDate = component.get('dtend')
                    #print (endDate.dt.strftime('%m/%d/%Y %H:%M'))
                    eventdateEnd.append(endDate.dt.strftime('%m/%d/%Y'))
                    eventTimeEnd.append(endDate.dt.strftime('%H:%M'))
                    
                    
                    dateStamp = component.get('dtstamp')
                    #print (dateStamp.dt.strftime('%m/%d/%Y %H:%M'))
                    #print ('')
                    
                    msg = '<b>' + component.get('summary') + '</b>' + '\n'
                    msg = msg + startDate.dt.strftime('%H:%M') + ' - '
                    msg = msg + endDate.dt.strftime('%H:%M') + '\n'
                    msg = msg + component.get('description') + '\n'
            bot.send_message(message.chat.id, msg, parse_mode='html', reply_markup=hideBoard)

            #print(msg)
            time.sleep(1)
                    
        # Modify or change these values based on your CalDAV
        # Converting to JSON
        #data = [{ 'Events Summary':eventSummary[0], 'Event Description':eventDescription[0],'Event Start date':eventDateStart[0], 'Event End date':eventdateEnd[0], 'At:':eventTimeStart[0], 'Until':eventTimeEnd[0]}]
        
        #data_string = json.dumps(data)
        #print ('JSON:', data_string)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
#
#
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
# other text
# function to handle the "other text"
@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    #todo ?????? ?? ?????????????? CEF
    print('1' + ' | ' + str(message.from_user.id) + ' | ' + str(message.chat.id) + ' | ' + str(message.text))
    
    func=lambda x: x in userid_list()
    if not(func(message.from_user.id)):
        fn_main_start(message)
    else:
        msgs_start = ['/start']
        msgs_wifi  = ['/wifi']
        msgs_help  = ['/help']
        msgs_thx   = ['??????????????!', '??????????????!', '??????????????', '??????????????', '??????', 'c????', 'thx', 'thanks', '????????????', '??????????']
        msgs_hello = ['????????????','????????????','hi','hello','????????????????????']
        ###bot.send_message(346573500, '???? ?????? ???????????????????? ????????????????????????' + str(message.chat.id), reply_markup=hideBoard)
        if message.text in msgs_thx:
            print('7' + ' | ' + str(message.from_user.id) + ' | ' + str(message.chat.id) + ' | ' + str(message.text))
            rply_list = ['????????????????????', '?????? ??????????????????!???? ', '???????????????????? ????']
            random_index = random.randint(0, len(rply_list) - 1)
            bot.send_message(message.chat.id, rply_list[random_index], reply_markup=hideBoard)
        elif message.text in msgs_hello:
            print('19' + ' | ' + str(message.from_user.id) + ' | ' + str(message.chat.id) + ' | ' + str(message.text))
            bot.send_message(message.chat.id, '????????????!', reply_markup=hideBoard)
        else:
            print('8' + ' | ' + str(message.from_user.id) + ' | ' + str(message.chat.id) + ' | ' + str(message.text))
            f = open('/usr/src/app/dockerdata/message_else_text.log', 'a')
            f.write(message.text + '\n')
            bot.send_message(message.chat.id, '?? ??????????????????, ???? ?????????????? ?????? ????', reply_markup=hideBoard)
        
if __name__ == '__main__':
    print('0' + ' | ' + str('Start TG BOT') + ' | ' + str(' ') + ' | ' + str(' '))
    bot.infinity_polling()