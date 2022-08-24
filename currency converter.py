import re
def main():
    global request
    print('Введите запрос в формате "300 долларов в рублях"')
    request= input()
    check_1()

def check_1():
    match= re.fullmatch(r'([0-9]+)\s+([а-я-А-Я]+)\s+(в)\s+([а-я-А-Я]+)', request) #проверка на совпадение с маской
    if match:
        correcting()
    else:
        print('Запрос некорректен')
        main()

def correcting():
    global request
    request= request.split()
    request[0]= int(request[0])
    request[1]= request[1].lower()
    request[3]= request[3].lower()
    if re.fullmatch(r'(доллар)([а-я]*)', request[1]):  #проверки на валюту
        request[1]= 'доллар'
    elif re.fullmatch(r'(рубл)([а-я]*)', request[1]):
        request[1]= 'рубл'
    if re.fullmatch(r'(доллар)([а-я]*)', request[3]):
        request[3]= 'доллар'
    elif re.fullmatch(r'(рубл)([а-я]*)', request[3]):
        request[3]= 'рубл'
    if request[1]== 'доллар' and request[3]== 'рубл':
        summ= int(request[0])*70
    else:
        summ= int(request[0])/70
    if request[0]== 0 and request[3]== 'рубл':
        print('0 рублей')
    elif request[0]== 0 and request[3]== 'доллар':
        print('0 долларов')
    elif int(request[0]%10)== 1:
        if request[3]== 'рубл':
            print(summ, 'рубль')
        else:
            print(summ, 'доллар')
    elif re.fullmatch(r'([0-9]*)([2-4])', str(int(summ))):
        if request[3]== 'рубл':
            print(summ, 'рубля')
        else:
            print(summ, 'доллара')
    elif re.fullmatch(r'([0-9]*)([5-9-0])', str(int(summ))):
        if request[3]== 'рубл':
            print(summ, 'рублей')
        else:
            print(summ, 'долларов')
    main()
main()
