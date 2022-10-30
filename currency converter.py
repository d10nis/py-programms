import re     #библа для regexp
import datetime
import urllib.request   #библа для чтения xml
import xml.etree.ElementTree as ET  #библа для парсинга
from os import path    #библа определения наличия файла
import telebot
import socket


REQUEST_REGEXP = '([0-9]+)\s+([А-я]+)\s+(в)\s+([А-я]+)'
REQUEST_TEXT = 'Введи запрос в формате "300 долларов в рублях"'
ERROR_TEXT = 'Запрос некорректен'
API_TOKEN = 'YOUR TOKEN'
BOT_GREETING = "Привет, я бот-конвертер валют. Я беру данные с сайта ЦБ РФ на сегодняшний день.\n\nДоступные валюты:\n\nевро\nдоллары\nрубли\nиены\nюани"

def main():
    global request
    return check_request(request )

def check_request(request ):
    match = re.findall(REQUEST_REGEXP, request) #проверка на совпадение с маской

    if match:
        first_match = match[0]
        summ = float(first_match[0])    #запись суммы искомой валюты
        in_currency = first_match[1].lower()
        out_currency = first_match[3].lower()

        result = correcting(summ, in_currency, out_currency )
        return result
    else:
        print(ERROR_TEXT )
    main()

def correcting(summ, in_currency, out_currency ):
    currencies_regexp = {'^доллар*': 'USD', '^рубл*': 'RUB', '^евр*': 'EUR', '^иен*': 'JPY', '^юан*': 'CNY'}   #словарь с обозначениями валют
    IPaddress=socket.gethostbyname(socket.gethostname())
    currencies_values_in_roubles = {'USD': 60, 'RUB': 1, 'EUR': 50, 'JPY': 40, 'CNY': 80}         #словарь с заданными валютами

    if IPaddress != "127.0.0.1":
        currencies_values_in_roubles = update_values(currencies_values_in_roubles )


    search_currency = lambda search, dict: [value for key, value in dict.items() if re.match(key, search)]
    
    in_currency_id = search_currency(in_currency, currencies_regexp )
    out_currency_id = search_currency(out_currency, currencies_regexp )

    if not in_currency_id or not out_currency_id:
        return ERROR_TEXT
    else:
        in_currency_id = in_currency_id[0]
        out_currency_id = out_currency_id[0]

    result_sum = float(summ * currencies_values_in_roubles[in_currency_id ] / currencies_values_in_roubles[out_currency_id ] )
    result_sum = round(result_sum, 2 )

    return f"{result_sum:,}"

def parse_cbrf(url):     #чтение и декодирование xml файла
    req = urllib.request.Request(url=url )
    response = ''
    with urllib.request.urlopen(req) as f:
        response += f.read().decode('windows-1251')
    return response     #возврат готового объекта

def read_cache(cache_filename):      #считывание файла кэша
        cache_file = open(cache_filename, 'r')
        cache_content = cache_file.read()
        cache_file.close()
        return cache_content

def update_cache(cache_filename, cache_content):   #редактирование кэша
        cache_file = open(cache_filename, 'w')
        cache_file.write(cache_content )
        cache_file.close()

def check_cache(cache_filename, check_date ):
    if not path.exists(cache_filename ):    #проверка на наличие кэша
        cache_file = open(cache_filename, 'w')
        cache_file.close()
        return False
    else:
        cache_content = read_cache(cache_filename )
        cache_root = ET.fromstring(cache_content )
        if cache_root.attrib['Date'] != check_date:  #проверка на совпадение дат
            return False
    return True


    
def update_values(currencies ):

    URL = "http://www.cbr.ru/scripts/XML_daily.asp?date_req="
    TODAY = datetime.date.today().strftime('%d/%m/%Y')    #получение даты в нужном формате
    URL += TODAY   #склейка для получения ссылки
    TODAY_XML = datetime.date.today().strftime('%d.%m.%Y')
    FILENAME = 'cbrf.xml'    #создание файла с xml данными
    
    response = ''
    if check_cache(FILENAME, TODAY_XML ):
        response = read_cache(FILENAME )
    else:
        response = parse_cbrf(URL )
        update_cache(FILENAME, response )

    root = ET.fromstring(response)   #парсинг корневого элемента xml 

    for valute in root.iter('Valute'):    #перебор подкоренных элементов
        charcode = valute.find('CharCode').text
        value = valute.find('Value').text
        value = value.replace(',', '.')
        value = float(value)
        if charcode in currencies:
            currencies[charcode] = value
    
    return currencies

BOT = telebot.TeleBot(API_TOKEN )

@BOT.message_handler(commands = ['start' ] )

def start_message(message ):
    BOT.send_message(message.chat.id, BOT_GREETING)
    BOT.send_message(message.chat.id, REQUEST_TEXT)

@BOT.message_handler(func = lambda message: True )

def give_result(message ):
    global request
    request = message.text
    BOT.reply_to(message, main() )

BOT.infinity_polling()
