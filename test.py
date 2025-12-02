#УРОК 1, ВЫВОД НА ЭКРАН
#print ("result",2, 4 + 2, sep="", end="! \n")

#УРОК 2, РАБОТА С КОМАНДАМИ

#print("re\nsult24")
#print("res\\nult24")
#print("Result: ", 5*199)
#print("Result:", max (5, 10, 2, 7)) маx - возвращает максимальное значение из переданных аргументов
#print("Result:", min (5, 10, 2, 7)) min - возвращает минимальное значение из переданных аргументов
#print("Result:", round (3.14159, 2)) round - округляет число до указанного количества знаков после запятой
#print("Result:", sum ([1, 2, 3, 4, 5])) sum - возвращает сумму всех элементов в итерируемом объекте        
#print("Result:", abs (-7)) abs - возвращает абсолютное значение числа
#print("Result:", pow (3, 4)) pow - возводит число в степень
#print("Result:", len ("Hello, World!")) len - возвращает длину объекта (строки, списка и т.д.)
#print("Result:", sorted ([5, 2, 9, 1, 5 , 6])) sorted - возвращает отсортированный список из итерируемого объекта
#print("Result:", list ("Hello")) # list - преобразует итерируемый объект в список
#print("Result:", str (123)) # str - преобразует объект в строку  
#УРОК 3 , ПЕРЕМЕННЫЕ И ВВОД ДАННЫХ

#number = 12+21 #int єто число целое
#boolean = True или False, #bool это логическое значение

#print ("Result: ", boolean)

#digit = 3.1421234 #float число с плавающей точкой
#word = "Result:" #str это строка
#number = 22-4
#str_num = "44" #str

#print (number + int (str_num)) #int() приводит строку к числу
#print (word + str (digit)) приводит число к строке

inp1 = int (input ("Введите что-нибудь: ")) #input() позволяет вводить данные с клавиатуры

inp2 = int (input ("Введите что-нибудь еще : "))
inp1 
print ("Result:", inp1 + inp2)  
print("Result:", inp1 * inp2)
print("Result:", inp1 - inp2)
print("Result:", inp1 / inp2)
print("Result:", inp1 // inp2) #целочисленное деление
print ("Result:", inp1 % inp2) #остаток от деления   
print("Result:", inp1 ** inp2) #возведение в степень
word = 3 
print (word*2)