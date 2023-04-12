import docx, re
from logger import TLogger
from lxml import etree
from os.path import basename, splitext
import binascii, base64


def getText(filename, qs):
    doc = docx.Document(filename)
    vcount = 0
    acount = 0
    inQ = False
    q_images = [] # список иллюстраций для вопроса
    a = [] # список варантов ответов для текущего вопроса
    q = [] # список текущий вопрос + текст помощи
    for para in doc.paragraphs:
        isBold = False
        isList = False
        isMarked = False
        isPicture = False
        if para.style.name == 'List Paragraph':
            isList = True
        elif '<w:numPr>' in para._p.xml:
            isList = True
        buf = ''
        for run in para.runs:
            #print(f'Style: {run.style.name}')
            url = get_imag2(run, doc)
            if len(url)>0:
                # Если мы уже обрабатываем вопрос и пришла иллюстрация, до добавляем ее в отдельное поле
                # Считаем, что если пришла картинка в параграфе без текста - то это картинка к вопросу
                # А если есть текст вокруг - значит ее вставляем инлайн в текущий текст
                if inQ and len(buf) == 0:
                    q[3] = url
                    isPicture = True
            if run.font.highlight_color:
                if len(run.text) > 2:
                    isMarked = True
            if run.bold:
                if len(run.text) > 5:
                    # Защита от "дребезга", если пару символов случайно в болд покрасили
                    isBold = True
            buf += url + run.text

        if isPicture: continue
        if isBold and isList:
            # пришел новый вопрос
            if q:
                q.append(a) # добавляем к вопросу варианты ответов
                qs.append(q) # Добавляем вопрос с вариантам в итоговый список тестовых заданий
            a=[]
            q=[]
            vcount+=1
            acount = 0
            inQ = True
            #print(f'Это вопрос:({para.style.name}) {vcount}. {buf}')
            q = [len(qs) + 1] + [f"Номер вопроса в исходном файле: {vcount}"]+[buf.strip()] + ["none"]
        else:
            if not inQ: continue
            if len(buf) == 0 or buf=="\n": continue
            if not isList:
                if not isAnswer(buf):
                    #print (f'({para.style.name}: {buf}) Внимание ! Похоже не список !')
                    inQ = False
                    q.append(a)  # добавляем к вопросу варианты ответов
                    qs.append(q)  # Добавляем вопрос с вариантам в итоговый список тестовых заданий
                    q=[]
                    a=[]
                    continue
            acount+=1
            #print(f'Это ответ:({para.style.name}) {acount}. {buf}')
            a.append([acount, isMarked, buf.strip()])
    return

def isAnswer(text):
    # Анализируем строку и если начинается с номера, считаем что это ответ
    if re.match('^\d+.', text): return True
    return False

def check_answer(str):
    i = 0
    while i < len(str):
        if str[i] == '+': return 1
        if str[i].isalpha(): return 0
        i += 1

def get_imag2(run, doc):
    #ToDo Сделать режим с преобразованием размера иллюстрации до рекомендованного
    imageURL = ""
    if 'graphicData' in run._r.xml:
        rt = etree.ElementTree(etree.XML(run._r.xml)).getroot()
        for item in rt.findall(".//{*}graphicData/{*}pic/{*}blipFill/{*}blip"):
            for k in item.keys():
                if "embed" in k: rId = item.get(k)
            try:
                contentType = doc.part.related_parts[rId].content_type
            except Exception as e:
                TLogger.WriteLog("Error", "Ошибка поиска идентификатора картинки в ячейке: {}".format(e))
                continue
            if not contentType.startswith("image"): continue
            imageName = basename(doc.part.related_parts[rId].partname)
            imageExt = imageName.split(".")[1]
            imageData = doc.part.related_parts[rId]._blob
            base64_bytes = base64.b64encode(imageData)
            base64_message = base64_bytes.decode('ascii')
            imageURL = f'<img src="data:image/{imageExt};base64,{base64_message}"/>'
    return imageURL


def parse_docx_2(filename, qs):
    getText(filename, qs)

if __name__ == '__main__':
    questions = []
    col_id = 3
    filename = 'src_docx2//Test2.docx'
    #show_tables(filename)
    #parse_table(filename, col_id, questions)
    parse_docx_2(filename,  questions)
    print(f"Итого вопросов: {len(questions)}")
