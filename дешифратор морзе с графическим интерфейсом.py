from tkinter import *
def shifrovka():
    predl= pole_vvoda.get()
    sent= list(predl)
    for i in range(0, len(sent)):
        sent[i]= sent[i].lower()
        sent[i]= alphabet[sent[i]]
    itog= ''.join(sent)
    result.configure(text= itog)
def deshifrovka():
    itog= ''
    sent= pole_vvoda.get().split(' ')
    for i in range(0, len(sent)):
        for k in alphabet.keys():
            if alphabet[k]==sent[i]:
                itog+= k
    result.configure(text= itog)
alphabet= {'а':'.-', 'б':'-...', 'в':'.--', 'г':'--.', 'д':'-..', 'е':'.', 'ж':'...-',
           'з':'--..', 'и':'..', 'й':'.---', 'к':'-.-', 'л':'.-..', 'м':'--', 'н':'-.',
           'о':'---', 'п':'.--.', 'р':'.-.', 'с':'...', 'т':'-', 'у':'..-', 'ф':'..-.',
           'х':'....', 'ц':'-.-.', 'ч':'---.', 'ш':'----', 'щ':'--.-', 'ъ':'.--.-.',
           'ы':'-.--', 'ь':'-..-', 'э':'...-...', 'ю':'..--', 'я':'.-.-', ',':'.-.-.-',
           '.':'......', '?':'..--..', '!':'--..--'}
c= Tk()
window= Canvas(c, width= 1000, height= 550, bg= 'white')
window.pack()
c.title('Дешифратор')
tekst1= Label(window, text='Это дешифратор из русского в Морзе и обратно', justify= CENTER,
              bg= 'White', font= ("Arial Bold", 13))
tekst1.grid(row= 0, column= 0, columnspa= 4)
tekst2= Label(window, text='Введите слово:', justify= CENTER, bg= 'White', font= ("Arial Bold", 11))
tekst2.grid(row= 1, column= 0, columnspan= 4)
pole_vvoda= Entry(window, width= 30)
pole_vvoda.grid(row= 2, column= 0, columnspan= 4)
button1= Button(window, bg= 'White', width= 15, text= 'Ru to Mor', command= shifrovka)
button1.grid(row= 3, column= 0)
button2= Button(window, bg= 'White', width= 15, text= 'Mor to Ru', command= deshifrovka)
button2.grid(row=3, column= 2)
tekst3= Label(window, text= 'Результат:', bg= "White", font= ("Arial Bold", 10))
tekst3.grid(row= 4, column= 0, columnspan= 4)
result= Label(window, text='', bg= 'White', font= ("Arial Bold", 20))
result.grid(row= 5, column= 0, columnspan=4)
window.mainloop()

