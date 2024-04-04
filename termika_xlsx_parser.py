import openpyxl,image_lib
from openpyxl_image_loader import SheetImageLoader
from openpyxl.cell.cell import MergedCell
from logger import TLogger


def isright(rlist,right_symbol):
    if len(rlist) < 3: return False
    str = rlist[2]
    if not str: return False
    if right_symbol in str: return True
    return False

def parse_table(filename, qs, right_symbol):
    wb_obj = openpyxl.load_workbook(filename)
    sheet = wb_obj.active
    if SheetImageLoader:
        SheetImageLoader._images={}
    image_loader = SheetImageLoader(sheet)
    i=0
    title = False
    lastisempty = False
    qcount = 0
    acount = 0
    qlist = []
    alist=[]
    course_name = ""
    current_topic_mame = ['Названия темы нет в исходном файле.']
    for row in sheet.iter_rows():
        rlist = [rlist.value for rlist in row[0:25] if rlist.value]
        #print(rlist)
        i += 1
        if len(rlist) > 0 and not title:
            # Пришла строка с названием курса
            # Надо проверить, что это точно тема, а не непонятные цифры в первой строке
            if len(rlist[0]) < 5:
                TLogger.WriteLog("Warning", f"Игнорируем ошибку формата файла. Лишние символы перед темой: {rlist[0]}")
                continue
            TLogger.WriteLog("Debug", f"Title: {rlist[0]}")
            course_name = rlist[0].replace("Тема:\n", " ").strip()# Это костыль для Губкинских файлов, убирам из названия курса Тема
            title = True
            lastisempty = False
            continue
        ###  Определяем новую тему курса по признаку наличия объединенных ячеек ###
        # Признак начинает со второй ячейки, а значение лежит в первой (индекс = 0)
        if isinstance(row[1], MergedCell) and len(rlist) > 0:
            # Пришла новая тема, надо закрывать вопрос
            #### Далее идет блок, который закрывает текущий вопрос. Если пришла тема, значит все варианты мы уже получили
            if len(qlist) > 0: # Проверяем есть ли вопрос, который надо закрыть
                qlist.append(alist)
                qlist.append(current_topic_mame[len(current_topic_mame) - 1])# Добавляем атрибут с текущей темой
                qs.append(qlist)
                qlist = []
                alist = []
            lastisempty = True
            #### Здесь заканчивается блок сохранения вопроса, такой же блок есть в части обработки нового вопроса!!!
            current_topic_mame.append(rlist[0].strip())# Только теперь устанавливаем новую тему для след. вопросов
            TLogger.WriteLog('Debug', f"Обнаружена новая тема: {current_topic_mame}")
            continue
        ###
        if len(rlist) < 2: rlist = []
        if len(rlist) > 0 and lastisempty == True:
            # Пришел очередной вопрос, сначала закрываем текущий, а потом создаем объект с новым вопросом
            # который будем наполнять вариантами ответов
            # Это патч для неправильных файлов в которых ответы разбиты пустыми строками
            # Ячейка с вопросом всегда должна иметь заливку цветом
            if row[0].fill.fgColor.rgb == "00000000":
                #Заливки нет, значит это ответ
                lastisempty = False
            else:
                qcount += 1
                acount = 0
                if len(qlist) > 0: # Проверяем существует ли текущий вопрос, который надо закрыть. Такой же блок есть выше, новая тема !!!
                    qlist.append(alist) # Добаваляем к вопросу варианты ответов
                    qlist.append(current_topic_mame[len(current_topic_mame)-1]) #Добавляем текущую тему
                    qs.append(qlist) #сохраняем все в листе с вопросами
                    qlist=[] # Очищаем ткущий вопрос (это список с его атрибутами)
                    alist=[] # Очищаем список вариантов ответа к текущему вопросу
                TLogger.WriteLog("Debug", f"{qcount}. Вопрос: {rlist[1]}")
                # И вот только теперь создаем объект (список) для сохранения атрибутов нового вопроса
                # Картинки обрабатываем, поэтому в последний элемент вопроса ставим картинку если она есть
                if image_loader.image_in(row[1].coordinate):
                    #print(f">>>Find Image in {row[1].coordinate}")
                    img = image_loader.get(row[1].coordinate)
                    qlist = [f"{qcount}", f"{qcount}", rlist[1], image_lib.get_image(img)] # создание нового вопроса
                else: qlist = [f"{qcount}",f"{qcount}",rlist[1],"none"] # новый вопрос, если в нем нет картинки
                lastisempty = False # Ставим флаг, что строка была не пустая, значит дальше ждем варианты ответов
                continue
        if len(rlist) > 0 and lastisempty == False:
            #Пришел очередной ответ
            acount += 1
            TLogger.WriteLog("Debug", f"{acount}. Ответ: {rlist[1]}  - {isright(rlist,right_symbol)}")
            #alist.append([f"{acount}",isright(rlist,right_symbol), f"{acount}. {rlist[1]}"])
            if image_loader.image_in(row[1].coordinate):
                #print(f">>>Find Image in answer, cell: {row[1].coordinate}")
                img = image_loader.get(row[1].coordinate)
                alist.append([f"{acount}", isright(rlist, right_symbol),
                              f'{rlist[1]} <div style="justify-content: center;">{image_lib.get_image(img)}</div>'])
            else:
                alist.append([f"{acount}", isright(rlist, right_symbol), f"{rlist[1]}"])
            continue
        if len(rlist) == 0:
            lastisempty = True
            continue
    if len(qlist) > 0:
        qlist.append(alist)
        qlist.append(current_topic_mame[len(current_topic_mame)-1])
        qs.append(qlist)
    TLogger.WriteLog("Debug", f"{qs}")
    return course_name

if __name__ =="__main__":
    #qs = []
    #res = parse_table('src\\Shablon.xlsx',qs,"v")
    #print(f"Parse complite: {res}")
    #print(qs)
    qs = []
    res = parse_table('src13\\Перечень вопросов с ответами по проверки знаний слесарь ЭРГО с (004).xlsx', qs, "v")
    #res = parse_table('src\\Shablon.xlsx', qs, "v")
    print(f"Parse complite: {res}")
    print(qs)
