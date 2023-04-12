import openpyxl
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
    i=0
    title = False
    lastisempty = False
    qcount = 0
    acount = 0
    qlist = []
    alist=[]
    course_name = ""
    for row in sheet.iter_rows():
        rlist = [rlist.value for rlist in row[0:25] if rlist.value]
        #print(rlist)
        i += 1
        if len(rlist) > 0 and not title:
            # Пришла тема
            # Надо проверить, что это точно тема, а не непонятные цифры в первой строке
            if len(rlist[0]) < 5:
                TLogger.WriteLog("Warning", f"Игнорируем ошибку формата файла. Лишние символы перед темой: {rlist[0]}")
                continue
            TLogger.WriteLog("Debug", f"Title: {rlist[0]}")
            course_name = rlist[0].replace("Тема:\n", " ").strip()
            title = True
            lastisempty = False
            continue
        if len(rlist) < 2: rlist = []
        if len(rlist) > 0 and lastisempty == True:
            # Пришел очередной вопрос
            # Это патч для неправильных файлов в которых ответы разбиты пустыми строками
            # Ячейка с вопросом всегда должна иметь заливку цветом
            if row[0].fill.fgColor.rgb == "00000000":
                #Заливки нет, значит это ответ
                lastisempty = False
            else:
                qcount += 1
                acount = 0
                if len(qlist) > 0:
                    qlist.append(alist)
                    qs.append(qlist)
                    qlist=[]
                    alist=[]
                TLogger.WriteLog("Debug", f"{qcount}. Вопрос: {rlist[1]}")
                #Картинки не обрабатываем, поэтому в последний элемент вопроса ставим none
                qlist = [f"{qcount}",f"{qcount}",rlist[1],"none"]
                lastisempty = False
                continue
        if len(rlist) > 0 and lastisempty == False:
            #Пришел очередной ответ
            acount += 1
            TLogger.WriteLog("Debug", f"{acount}. Ответ: {rlist[1]}  - {isright(rlist,right_symbol)}")
            #alist.append([f"{acount}",isright(rlist,right_symbol), f"{acount}. {rlist[1]}"])
            alist.append([f"{acount}", isright(rlist, right_symbol), f"{rlist[1]}"])
            continue
        if len(rlist) == 0:
            lastisempty = True
            continue
    if len(qlist) > 0:
        qlist.append(alist)
        qs.append(qlist)
    TLogger.WriteLog("Debug", f"{qs}")
    return course_name