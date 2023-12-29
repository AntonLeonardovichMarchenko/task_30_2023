# задача анализа вакансий на рынке труда:
# необходимо получить все вакансии определенной компании по всем
# городам России. И осуществлять это надо базе HeadHunter.

# Импорт необходимых для работы библиотек:

import requests  # Для запросов по API
import json  # Для обработки полученных результатов
import os  # Для работы с файлами

import time

global FullSalary, nSalary, lstVacancies


# страна idArea со всеми её внутренними зонами:
def getAreas(idArea):
    # регионы со своими внутренними зонами
    req = requests.get('https://api.hh.ru/areas')
    data = req.content.decode()
    req.close()

    # json - java script object notation - методом loads осуществляется
    # преобразование в python object
    jsObj = json.loads(data)
    areas = []  # всё готово к сбору информации о зонах (список зон объявлен)
    # areas - это список, куда будет собираться информация о зонах.
    # 'areas' - это ключ в словаре зон - большая разница!

    # ====================================================================
    for _obj in jsObj:
        # теперь в _obj отдельный объект из jsObj по структуре это списк.
        # И в _obj могут быть другие зоны (списки списков).
        # И если список не пустой, то это значит, что у зоны есть свои вложенные
        # зоны, которые надо разобрать. У списков стандартная структура: зоны
        # разбираются по общему алгоритму. Возможно, что список пустой. Тогда ничего
        # со списком делать не надо. Все зоны перебраны.
        # ================================================================
        for i in range(len(_obj['areas'])):
            # ============================================================
            if len(_obj['areas'][i]['areas']) != 0: # словарь не пустой.У зоны есть
                # внутренние зоны. И тогда внутренние зоны аналогичным образом разбираются
                # и цепляются к списку areas
                for j in range(len(_obj['areas'][i]['areas'])):
                    # ==== и так будет с каждой зоной ====================
                    if _obj['id'] == idArea:
                        areas.append([_obj['id'],
                                      _obj['name'],
                                      _obj['areas'][i]['areas'][j]['id'],
                                      _obj['areas'][i]['areas'][j]['name']])
                    # ====================================================
                    # из словаря получается список зон.
                    # Ключи не нужны. Здесь достаточно того, что каждая зона
                    # в списке зон (areas) строго упорядочено
            # ============================================================
            else:  # Если у зоны нет внутренних зон -
                # она к списку зон цепляется сама
                # ==== и так будет с каждой зоной ====================
                if _obj['id'] == idArea:
                    areas.append([_obj['id'],
                                  _obj['name'],
                                  _obj['areas'][i]['id'],
                                  _obj['areas'][i]['name']])
                # ====================================================
                # из словаря получается список зон

    return areas  # на выходе - список разобранных зон


# Поиск работодателей.

def getEmployers(areas, location, demand, f):


    global key_strings, localVac
    if not os.path.exists('./areas/'):
        os.makedirs('./areas/')



    ctrLst = list()

    area_number = -1  # !!!!!
    # ============================================================

    for area in areas:
        area_number += 1
        #print(f'{area_number} ... {area}')
        # вакансии по работодателю в каждой зоне России (ID 113) =========
        # area[0]   area[1]     area[2]                 area[3]
        # '113'     Россия      ещё код (региона?)...   населённый пункт

        # УКАЗАТЕЛЬ количества прочитанных (прочитанных с шагом 'per_page')
        # страниц с вакансиями для данного региона
        page = 0
        localVac = 0
        ctrLst.clear()

        while True:
            # Определение региона ========================================
            # Определение региона ========================================
            if area[3] == location:
                pass  # нужный регион (Москва) - формирование записи ======
            else:
                break  # переход к следующей записи вакансии ==============



            # с помощью java script object notation (json) функцией
            # getPage(номерСтраницы, кодРегиона)
            # формируются записи о вакансиях по данному кодуРегиона.
            # Возможны записи с пустыми списками ([] или None).
            # С такими записями ничего не делается.
            # Производится выбор новой зоны.
            # Там же увеличивается значение счётчика
            # area_number - член area
            jsObj = json.loads(getPage(page, area[2]))
            # аргумент page обеспечивает постраничное чтение: страница,
            # зона поиска, ... значение 'per_page': ... можно установить
            # ПО УМОЛЧАНИЮ.

            # исключение, которое возникает в результате сбоя при переборе
            # списка вакансий. возможно, что в этом случае может помочь такая
            # вот примочка:
            time.sleep(0.50)  # таймер обеспечивает стабильную работу
                              # оператора json.loads...

            vacancyJob = None

            # Попытка перебора списка вакансий. Этот список может быть
            # непустым и корректно заполненным, может быть пустым, может
            # быть пустым и содержать ошибки заполнения (плохо прочитан).


            try:
                vacancyJob = jsObj['items']
            except Exception as ex:
                print(f'{page}:  {area_number} ..... {vacancyJob} :::::: {ex} ..... ')
                break
                # из jsObj прочитано всё, что возможно (скорее всего НИЧЕГО здесь
                # прочесть не получилось). Можно выходить из цикла


            # список вакансий региона изначально пустой
            if len(vacancyJob) == 0:
                if page == 0:
                    print(f'{area_number}: {area[3]} vacancyJob is empty')
                break
            elif len(vacancyJob) > 0:

                nVac = 1  # !!!!! номер вакансии

                # разбор списка вакансий =================================


                for vc in vacancyJob:

                    # проверка текущего фрагмента на вхождение demand
                    if (vc['name'].find(demand) != -1) or (vc['name'].find(demand) == ''):
                        pass
                    else:
                        break

                    ctrlName = vc['name'].replace(' ', '')
                    if ctrlName in ctrLst:
                        continue
                    else:
                        ctrLst.append(ctrlName)

                    # формируется запись инфы о вакансии
                    # (развёрнутое название в заданном регионе)

                    key_strings = vc['name'] + ' >>> '

                    if vc['employer']['name'] != None:
                        key_strings += vc['employer']['name'] + ' - '
                    else:
                        key_strings += 'No employer name' + ' - '


                    localVac += 1


                    nVac += 1  # текущая вакансия зафиксирована. Увеличивается номер вакансии

                        # ================================================


                    key_strings = str(page) + ' ' + str(localVac) + ': ' + key_strings
                    if localVac == 1:
                        key_strings = '\n' + key_strings

                    print(key_strings)
                    f.write(key_strings + '\n')


            page += 1
            localVac = 0
        # ================================================================





def findPages(areas, location, demand, f):
    # это создатель директории для записи файла с вакансиями =====
    # вызывается по мере необходимости (один раз) ================

    global salaryTmpFrom, salaryTmpTo, salaryInfo, key_strings
    if not os.path.exists('./areas/'):
        os.makedirs('./areas/')

    FullSalary = 0.0
    nSalary = 0
    ctrLst = list()

    area_number = -1  # !!!!!
    # ============================================================

    for area in areas:
        area_number += 1
        # print(f'{area_number} ... {area}')
        # вакансии по работодателю в каждой зоне России (ID 113) =========
        # area[0]   area[1]     area[2]                 area[3]
        # '113'     Россия      ещё код (региона?)...   населённый пункт

        # УКАЗАТЕЛЬ количества прочитанных (прочитанных с шагом 'per_page')
        # страниц с вакансиями для данного региона
        page = 0
        localVac = 0
        ctrLst.clear()

        while True:
            # Определение региона ========================================
            if area[3] == location:
                pass  # нужный регион  - формирование записи =============
            else:
                break  # переход к следующей записи вакансии =============

            # По крайней мере вышли на заданный регион ===================
            # с помощью java script object notation (json) функцией
            # getPage(номерСтраницы, кодРегиона)
            # формируются записи о вакансиях по данному кодуРегиона.
            # Возможны записи с пустыми списками ([] или None).
            # С такими записями ничего не делается.
            # Производится выбор новой зоны.
            # Там же увеличивается значение счётчика
            # area_number - член area
            jsObj = json.loads(getPage(page, area[2]))
            # аргумент page обеспечивает постраничное чтение: страница,
            # зона поиска, ... значение 'per_page': ... можно установить
            # ПО УМОЛЧАНИЮ.

            # исключение, которое возникает в результате сбоя при переборе
            # списка вакансий. возможно, что в этом случае может помочь такая
            # вот примочка:
            time.sleep(0.50)  # таймер обеспечивает стабильную работу
            # оператора json.loads...

            vacancyJob = None

            # Попытка перебора списка вакансий. Этот список может быть
            # непустым и корректно заполненным, может быть пустым, может
            # быть пустым и содержать ошибки заполнения (плохо прочитан).

            try:
                vacancyJob = jsObj['items']
            except Exception as ex:
                print(f'{page}:  {area_number} ..... {vacancyJob} :::::: {ex} ..... ')
                break
                # из jsObj прочитано всё, что возможно (скорее всего НИЧЕГО здесь
                # прочесть не получилось). Можно выходить из цикла

            # список вакансий региона изначально пустой
            if len(vacancyJob) == 0:
                if page == 0:
                    print(f'{area_number}: {area[3]} vacancyJob is empty')
                break
            elif len(vacancyJob) > 0:

                nVac = 1  # !!!!! номер вакансии

                # разбор списка вакансий =================================
                for vc in vacancyJob:

                    # проверка текущего фрагмента на вхождение demand
                    if (vc['name'].find(demand) != -1) or (vc['name'].find(demand) == ''):
                        pass
                    else:
                        break

                    ctrlName = vc['name'].replace(' ', '')
                    if ctrlName in ctrLst:
                        continue
                    else:
                        ctrLst.append(ctrlName)

                    # формируется запись инфы о вакансии
                    # (развёрнутое название в заданном регионе)

                    key_strings = vc['name'] + ' >>> '

                    if vc['employer']['name'] != None:
                        key_strings += vc['employer']['name'] + ' - '
                    else:
                        key_strings += 'No employer name' + ' - '


                    localVac += 1

                    # простая обработка информации о зарплате ========
                    # это тест на случай, если не будет указана зарплата
                    salaryInfo = vc['salary']
                    if salaryInfo == None:
                        salaryInfo = "{'from': 0.0, 'to': 0.0, 'currency': 'RUR'}"
                        salaryTmpFrom = 0.0
                        salaryTmpTo = 0.0
                    else:

                        if vc['salary']['from'] == None:
                            salaryTmpFrom = 0.0
                            vc['salary']['from'] = '0.0'
                        else:
                            salaryTmpFrom = float(vc['salary']['from'])

                            if vc['salary']['to'] == None:
                                salaryTmpTo = 0.0
                                vc['salary']['to'] = '0.0'
                            else:
                                salaryTmpTo = float(vc['salary']['to'])

                        # ================================================
                        if salaryTmpFrom > 0.0:
                            FullSalary += salaryTmpFrom
                            nSalary += 1

                        if salaryTmpTo > 0.0:
                            FullSalary += salaryTmpTo
                            nSalary += 1

                    nVac += 1  # текущая вакансия зафиксирована. Увеличивается номер вакансии

                    # ================================================

                    salaryInfo = f'from: {salaryTmpFrom}, to: {salaryTmpTo}, currency: RUR'

                    key_strings += salaryInfo

                    key_strings = str(page) + ' ' + str(localVac) + ': ' + key_strings
                    if localVac == 1:
                        key_strings = '\n' + key_strings

                    print(key_strings)
                    f.write(key_strings + '\n')

                # а это перебор страниц. Страниц с вакансиями может быть больше одной.
                # Это количество определяется значением записи в словаре с параметрами
                # поиска
                #
                #    params = {
                #               ::::::::::
                #               'per_page': 100  # Количество вакансий
                #               ::::::::::
                #             }
                #
                # Результат разбора записи зависит от самого поиска и может быть причиной
                # возбуждения исключения. Могут быть как корректно заполненные непустые
                # списки, незаполненные ПУСТЫЕ списки, списки прочитанные или заполненые
                # с ошибками.
                #
                # = в списке были записи,
                # = он с самого начала был пустой,
                # = он был неправильно прочитан или некорректно заполнен.
                #
                # Разница между пустым и непустым списками в
                # конечном счёте заключается в значении page.
                # Страница прочитана и разобрана - page увеличен.
                # jsObj = json.loads(getPage(page, area[2])) - это прочтение
                # очередной страницы.

            page += 1
            localVac = 0
        # ================================================================

    if nSalary != 0:
        middleSalary = float(FullSalary / nSalary)
        middleSalary = float("%.3f" % middleSalary)
    else:
        middleSalary = 0.0

    print(f'the middleSalary is: {middleSalary}')
    return middleSalary

    # ============================================================================================


def getPage(n_page, area):
    #               зона, где будут выбираться вакансии
    #      номер страницы для постраничного выбора вакансий

    # словарь с параметрами поиска
    params = {
        #'employer_id': 3529,  # ID 2ГИС - это только про СБЕР !
        'area': area,  # Поиск в зоне
        'page': n_page,  # Номер страницы
        #'per_page': 100 # Количество вакансий на 1 странице по умолчанию
    }

    # вакансии по работодателю по зоне России (ID 113)
    req = requests.get('https://api.hh.ru/vacancies', params)  # параметры поиска
    data = req.content.decode()
    req.close()
    return data


# ========================================================================


def relevantsVacancies(areas, location):
    dictVacancies = None

    area_number = -1  # !!!!!

    # ============================================================

    for area in areas:
        # листатель страниц с вакансиями =================================
        page = 0
        area_number += 1
        # print(f'{area_number} ... {area}')
        # вакансии по работодателю в зоне России (ID 113) ================
        # area[0]   area[1]     area[2]                 area[3]
        # '113'     Россия      ещё код (региона?)...   населённый пункт

        while True:
            # Определение региона ========================================
            if area[3] == location:
                pass  # нужный регион (Москва) - формирование записи ======
            else:
                break  # переход к следующей записи вакансии ==============

            # По крайней мере вышли на заданный регион ===================
            # с помощью java script object notation (json) функцией
            # getPage(номерСтраницы, кодРегиона)
            # формируются записи о вакансиях по данному кодуРегиона.
            # Возможны записи с пустыми списками ([] или None).
            # С такими записями ничего не делается.
            # Производится выбор новой зоны.
            # Там же увеличивается значение счётчика
            # area_number - член area
            jsObj = json.loads(getPage(page, area[2]))

            #print(f'------------------- {page} -------------------')


            # исключение, которое возникает в результате сбоя при переборе
            # списка вакансий. возможно, что в этом случае может помочь такая
            # вот примочка:
            time.sleep(0.50)   # таймер обеспечивает стабильную работу
                               # оператора json.loads...
            try:
                vacancyJob = jsObj['items']
            except Exception as ex:
                # if page == 0:
                #    print(f'{area_number}: {area[3]} vacancyJob is empty')
                break

            # ну вот как раз тот самый случай, когда список вакансий региона
            # изначально пустой
            if vacancyJob == []:
                # if page == 0:
                #     print(f'{area_number}: {area[3]} vacancyJob is empty')
                break
            elif vacancyJob != []:

                # разбор списка вакансий =================================
                nVc = 0

                #vTest = []
                for vc in vacancyJob:
                    # формируется список вакансий:
                    nVac = 1
                    # счётчик совпадений описаний вакансий

                    # начало записи инфы о вакансии
                    # (развёрнутое название вакансии в заданном регионе, приведённое к нижнему регистру)
                    vac = vc['name']  # это выбор значения из словаря по ключу 'name'
                    empl_name = ' - ' + vc['employer']['name']
                    fullVac = vac
                    fullVac += '  ' + empl_name
                    vac = vac.lower()

                    vacForCompare = vac.replace(' ','')
                    # Оптимизация процедуры сравнения: удаление пробелов в описании вакансии.
                    context = 0  # счётчик на контекст ВСЕЙ тестируемой вакансии

                    nMac = 0  # !!!!! количество применений findContext

                    for mt in vacancyJob:

                        # НЕ сравнивать описания вакансий с одним и тем же индексом вхождения
                        vcInd = vacancyJob.index(vc)
                        mtInd = vacancyJob.index(mt)

                        #if vacancyJob.index(vc) == vacancyJob.index(mt):
                        if vcInd == mtInd:
                            continue
                        else:
                            mac = mt['name']  # это выбор значения из словаря по ключу 'name'
                            mac = mac.lower()

                            macForCompare = mac.replace(' ','')
                            # Оптимизация процедуры сравнения: удаление пробелов в описании вакансии.

                            if (vacForCompare != macForCompare):
                                context = max(context, findContext(context, vac, mac))
                                nMac += 1
                                print(f"{nMac}, {context}: {vac} ... {mac} ")
                                #                                     имя текущей вакансии
                                #                           имя базовой вакансии из vacancyJob()
                                #                результат применения findContext
                                #        количество применений findContext
                                # context / len(vac)
                                # context = float('%.2f' % context)

                            elif (vacForCompare == macForCompare):
                                # повторное вхождение объявления о вакансии на данной странице
                                nVac += 1

                    # разбор страниц с информацией о вакансиях ===============
                    # сборка очередной строки из страницы с записями.
                    # vc - строкa, которая содержит информацию о snippet'ах
                    sd = skillsDescriptor(vc, 'snippet')
                    fullVac = fullVac + f'   | {nVac}    ' + sd
                    # и она цепляется к описанию вакансии
                    # основная обработка информации о вакансии уже проведена.
                    # Поэтому для представления используется исходный фрагмент строки
                    # (со всякими скобками, знаками препинания, заглавными буквами и
                    # прочей хренью, от которой избавлялись на этапе препроцессорной обработки)
                    #dictVacancies = rvIn(dictVacancies, page, context, vac)
                    dictVacancies = rvIn(dictVacancies, page, context, fullVac)


            page += 1

    #print(dictVacancies)
    writeRelevantsVacanciesResult(dictVacancies)

# ========================================================================

def writeRelevantsVacanciesResult(dictVacancies):
    # файл для записи результатов сопоставления
    f = open('r_result.txt', mode='w', encoding='utf8')

    keys = dictVacancies.keys()
    for key in keys:
        f.write(f'  {key}\n')
        for val in dictVacancies[key]:
            f.write(f'{key}: {val}\n')

    f.close()

# ========================================================================

def rvIn(dictVacancies, page, context, vac):
    #                            текущая вакансия
    #                   результат применения findContext
    #    ссылка на словарь

    context = str(page) + '_' + str(context)

    if dictVacancies == None:
        value = [vac]
        dictVacancies = {context: value}

    else:
        keys = list(dictVacancies.keys())

        if (context in keys) == True:
            values = dictVacancies[context]
            if not (vac in values):
                values.append(vac)
        else:
            keys.append(context)
            lstValues = list(dictVacancies.values())
            value = [vac]
            lstValues.append(list(value))
            dictVacancies = dict(zip(keys, lstValues))

    return dictVacancies


def findContext(context, strTst, strMark):
    # удалить сокращения, привести к нижнему регистру, разбить на фрагменты
    # проверка на вхождение значимых фрагментов strMark в strTst
    # возвращается индекс вхождения значимых фрагментов из strMark в strTst

    sTst = 0

    str_remove =  ['(ст.',
                   '(ст.',
                   '(м.',
                   ' м.',
                   ' и ',
                   ' в ',
                   ' к ',
                   ' за ',
                   ' на ',
                   ' с ',
                   ' до ',
                   ' по ',
                   '/',
                   ')',
                   '(',
                   '-',
                   '(г.',
                   ' г.',
                   ]

    for str_r in str_remove:
        strTst = strTst.replace(str_r, ' ')
        strMark = strMark.replace(str_r, ' ')

    tsts = strTst.split(' ')

    tmp = []
    for t in tsts:
        if t == '':
            pass
        else:
            tmp.append(t)

    tsts = tmp

    # ====================================================================
    for t in tsts:



        # проверить значимый фрагмент strMark на вхождение в strTst

        if (t in strMark) == True:
            sTst += 1  # в случае вхождения фрагмента в strMark изменить
            # индекс вхождения этого фрагмента

            #print(f'{sTst}: {t}:::{strMark}')
    # ====================================================================


    return max(sTst, context)

# ========================================================================
def skillsDescriptor(vacancyJob, vcKeys):

    vcKeyStrA = vacancyJob['snippet']['requirement']
    if type(vcKeyStrA) == None:
        vcKeyStrA = '__________'

    vcKeyStrB = vacancyJob['snippet']['responsibility']
    if type(vcKeyStrB) == None:
        vcKeyStrB = '----------'

    return(str(vcKeyStrA) + ':  ' + str(vcKeyStrB))


# ========================================================================
# это фрагменты кода, которые описывают структуру записи о вакансии.
# Взято из открытых источников. Пригодились по крайней мере для понимания.

# ========================================================================
# df = pd.DataFrame(dt, columns = [
#                                   'id',
# #                                 'premium',
# #                                 'name',
# #                                 'department_name',
# #                                 'has_test',
# #                                 'response_letter_required',
# #                                 'area_id',
# #                                 'area_name',
# #                                 'salary_from',
# #                                 'salaty_to',
# #                                 'type_name',
# #                                 'address_raw',
# #                                 'response_url',
# #                                 'sort_point_distance',
# #                                 'published_at',
# #                                 'created_at',
# #                                 'archived',
# #                                 'apply_alternate_url',
# #                                 'insider_interview',
# #                                 'url',
# #                                 'alternate_url',
# #                                 'relations',
# #                                 'employer_id',
# #                                 'employer_name',
# #                                 'snippet_requirement',
# #                                 'snippet_responsibility',
# #                                 'contacts',
# #                                 'schedule_name',
# #                                 'working_days',
# #                                 'working_time_intervals',
# #                                 'working_time_modes',
# #                                 'accept_temporary'
#                                 ])
# df.to_excel('result_2gis.xlsx')
# ========================================================================

areas = getAreas('113')

# f = open('resultSalary.txt', mode='w', encoding='utf8')
# middleSalary = findPages(areas, 'Москва', ' менеджер ', f)  # выборка по требуемой специальности
# # middleSalary = findPages(areas, 'Москва', '', f)  # выборка по ВСЕМ специальностям или по заданным
# # # ('менеджер '), в регионе Москва, с  определением средней зарплаты
# f.close()

###### middleSalary = findPages(areas, 'Москва', '', f)  # выборка по ВСЕМ специальностям
# f = open('resultSalary.txt', mode='w', encoding='utf8')
# middleSalary = findPages(areas, 'Москва', '', f)  # выборка по ВСЕМ специальностям
# # в регионе Москва, с определением средней зарплаты
# f.close()

#relevantsVacancies(areas, 'Москва')
relevantsVacancies(areas, 'Санкт-Петербург')

# f = open('resultEmployers.txt', mode='w', encoding='utf8')
# getEmployers(areas, 'Казань', '', f)
# f.close()
