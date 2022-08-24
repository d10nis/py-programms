import re

# isaltanov: 
# 1. Хорошим тоном является использование глобальных конфигурационных переменных,
# которые не меняются в результате работы кода
# 2. Регулярное выражение [а-я-А-Я] можно сократить до [A-я] - это то же самое
REQUEST_REGEXP = '([0-9]+)\s+([А-я]+)\s+(в)\s+([А-я]+)'
REQUEST_TEXT = 'Введите запрос в формате "300 долларов в рублях"'
ERROR_TEXT = 'Запрос некорректен'

def main():

    # isaltanov:
    # 3. Глобальные переменные, которые меняются в коде, лучше не использовать
    
    # global request
    # print('Введите запрос в формате "300 долларов в рублях"')
    print(REQUEST_TEXT)
    request = input()

    # isaltanov:
    # 4. Раз тут решил использовать функцию, дай ей на вход переменную request
    
    # check_1()
    check_1(request)

# def check_1():
def check_1(request):

    # isaltanov:
    # 5. Лучше использовать функцию findall - она сразу тебе вернет массив из тех элементов, которые ты
    # подошли под маски внутри скобочек ( ) и не нужно делать split
    
    # match= re.fullmatch(r'([0-9]+)\s+([а-я-А-Я]+)\s+(в)\s+([а-я-А-Я]+)', request) #проверка на совпадение с маской
    match = re.findall(REQUEST_REGEXP, request) #проверка на совпадение с маской

    if match:
        # isaltanov:
        # 6. здесь лучше сразу подготовить данные из строки, раз мы разобрали ее по элементам
        first_match = match[0]
        sum = float(first_match[0])
        in_currency = first_match[1].lower()
        out_currency = first_match[3].lower()

        # isaltanov:
        # 7. Ценность этой функции - расчет результата, а не печать на экран. Пусть она принимает на вход уже
        # подготовленные данные из строки и возвращает результат. Дальше мы сами тут напечатаем

        # correcting()
        result = correcting(sum, in_currency, out_currency )
        print (result)
    else:
        # print('Запрос некорректен')
        print(ERROR_TEXT )

        # isaltanov:
        # 8. Здесь уже можно вывести из условия повторный вызов main() - он используется для обоих сценариев if .. else
        
        # main()
    main()

#def correcting():
def correcting(sum, in_currency, out_currency ):

    # global request
    # request= request.split()
    # request[0]= int(request[0])
    # request[1]= request[1].lower()
    # request[3]= request[3].lower()

    # isaltanov:
    # 9. Дальше идет лапша кода из if и else - предлагаю ее оптимизировать таким образом:
    # мы создадим словарик слов, по которым будем понимать валюту, и словарик курсов, по которым 
    # будем выбирать нужный курс. Сначала с помощью регулярного выражения поймем, из какой валюты
    # конвертируем, потом - в  какую конвертируем - и сделаем конвертацию

    currencies_regexp = {'^доллар*': 'USD', '^рубл*': 'RUR'}
    currencies_values_in_roubles = {'USD': 70, 'RUR': 1}

    # это лямбда-функция, чтобы два раза не писать одну и ту же логику для входящей и исходящей валюты
    search_currency = lambda search, dict: [value for key, value in dict.items() if re.match(key, search)]
    
    in_currency_id = search_currency(in_currency, currencies_regexp )
    out_currency_id = search_currency(out_currency, currencies_regexp )

    if not in_currency_id or not out_currency_id:
        return ERROR_TEXT
    else:
        in_currency_id = in_currency_id[0]
        out_currency_id = out_currency_id[0]

    result_sum = float(sum * currencies_values_in_roubles[in_currency_id ] / currencies_values_in_roubles[out_currency_id ] )
    result_sum = round(result_sum, 2 )

    return result_sum 

    # if re.fullmatch(r'(доллар)([а-я]*)', request[1]):  #проверки на валюту
    #    request[1]= 'доллар'
    # elif re.fullmatch(r'(рубл)([а-я]*)', request[1]):
    #    request[1]= 'рубл'
    # if re.fullmatch(r'(доллар)([а-я]*)', request[3]):
    #    request[3]= 'доллар'
    # elif re.fullmatch(r'(рубл)([а-я]*)', request[3]):
    #    request[3]= 'рубл'
    # if request[1]== 'доллар' and request[3]== 'рубл':
    #    summ= int(request[0])*70
    # else:
    #    summ= int(request[0])/70
    # if request[0]== 0 and request[3]== 'рубл':
    #    print('0 рублей')
    # elif request[0]== 0 and request[3]== 'доллар':
    #    print('0 долларов')
    # elif int(request[0]%10)== 1:
    #    if request[3]== 'рубл':
    #        print(summ, 'рубль')
    #    else:
    #        print(summ, 'доллар')
    # elif re.fullmatch(r'([0-9]*)([2-4])', str(int(summ))):
    #    if request[3]== 'рубл':
    #        print(summ, 'рубля')
    #    else:
    #        print(summ, 'доллара')
    # elif re.fullmatch(r'([0-9]*)([5-9-0])', str(int(summ))):
    #    if request[3]== 'рубл':
    #        print(summ, 'рублей')
    #    else:
    #        print(summ, 'долларов')
    # main()
main()
