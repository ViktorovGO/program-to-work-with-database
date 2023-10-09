import os
import sqlite3
def DB(sql):  #Внесение изменений в БД
    if sql != '':
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        cur.close()
        con.close()

def ch_bd(sql,tbl_name):  #Запись таблицы в переменную
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    with con:
        BD= cur.execute(sql).fetchall()

    cur.close()
    con.close()
    return BD

def out_bd(BD,tbl_name):  #Вывод БД в виде таблицы
    leng=len(BD)
    print('Таблица: ', tbl_name, ' из БД ', db_name)
    for i in range(leng):
        print(BD[i])

global db_name
db_name= input('Укажите имя файла SQLite: ') #ввод имени файла SQLite
tbl_name1='vuzkart'
tbl_name2='vuzstat'
flag=True
if (os.path.isfile(db_name) != True):
    print('Нет такого файла!')
    flag = False

if flag==True:
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    sql_1='SELECT * FROM {}'.format(tbl_name1)
    sql_2 = 'SELECT * FROM {}'.format(tbl_name2)
    BD1 = ch_bd(sql_1,tbl_name1)
    BD2 = ch_bd(sql_2,tbl_name2)
    cur.close()
    con.close()
while(flag):
        what= int(input("""
        Выберите действие(Введите цифру):
        1 - Отображение текущего содержимого обеих БД на экране в виде таблицы
        2 - Выбрать статус из списка статусов вуза и вывести все вузы с выбранным статусом
        3 - Распределение процента преподавателей, имеющих ученые степени, по профилям 
        4 - Отображение первой БД
        5 - Отображение второй БД
        6 - Завершение работы с программой \n"""))

        if what==1:
            out_bd(BD1, tbl_name1) #Вывод БД
            out_bd(BD2, tbl_name2)
        if what==2:
            sql='SELECT status FROM {}'.format(tbl_name1) #Формирование запроса sql
            stat=ch_bd(sql,tbl_name1) #Чтение БД
            stat=set(stat)
            stat=str(stat)
            stat=stat.replace(' ','')  #Операции редактирования списка статусов
            stat=stat.replace('(','')
            stat = stat.replace(')', '')
            flag_1=True
            while(flag_1):
                print("Введите статус из данного списка:",stat) #Пользовательский ввод выбранного статуса
                sel_stat=input()
                if (sel_stat in stat )==True:
                    while len(sel_stat)<15: #Дополнение статуса до 15 символов, если это необходимо
                        sel_stat+=" "

                    sql = 'SELECT z1 FROM {} WHERE status = "{}"'.format(tbl_name1,sel_stat) #Формирование запроса sql
                    vuz_name_stat= ch_bd(sql,tbl_name1) #Чтение БД
                    out_bd(vuz_name_stat,tbl_name1) #Вывод БД
                    flag_1=False
                else:
                    print('Такого статуса нет, введите еще раз')
        if what==3:
            sql = 'SELECT count(prof) FROM (SELECT distinct prof FROM {}) '.format(tbl_name1)
            count=ch_bd(sql,tbl_name1)
            sql = 'SELECT distinct prof FROM {} '.format(tbl_name1)
            data =ch_bd(sql,tbl_name1) # Имена профилей
            count=count[0][0]  #Количество профилей

            for i in range(count):
                sql = 'SELECT  a.prof,sum(b.PPS),(sum(b.DN)+sum(b.KN)) FROM {} a LEFT JOIN {} b on a.codvuz=b.codvuz WHERE a.prof="{}"'.format(tbl_name1, tbl_name2,data[i][0]) #sql запрос на получение Профиля, суммы кол-ва преподавателей и кол-ва преподавателей с учеными степенями,реализовано путем объединения двух таблиц
                exec(f'data{i}=ch_bd(sql,tbl_name1)')# Соединение двух таблиц
                """exec(f'out_bd(data{i}, tbl_name1)')"""  #Вывод считанной таблицы
                exec(f'data{i}=list(data{i}[0])')

            print('[N,','Профиль,','Кол-во преподователей,','Кол-во преподователей с учеными степенями,','Процентное отношение преподавателей со степенями к общему числу преподавателей]')
            z_1=0
            z_2=0
            for i in range(count):
                exec(f'data{i}.insert(0,(i+1))')
                exec(f'y=data{i}[3]')
                exec(f'x=data{i}[2]')
                x=round((y/x)*100,3)
                exec(f'data{i}.append(x)')
                exec(f'z_1+=data{i}[2]')
                exec(f'z_2+= data{i}[3]')
                exec(f'length=len(data{i}[1])')

                while(length<7):
                    exec(f'data{i}[1]+=" "')
                    exec(f'length=len(data{i}[1])')
                exec(f'print(data{i})')

            print('[ALL,','ALL    ,',z_1,',',z_2,',',round((z_2/z_1)*100,3),"]")
        if what==4:
            out_bd(BD1, tbl_name1) #Вывод БД
        if what==5:
            out_bd(BD2, tbl_name2)
        if what==6:

            break




