import json, os, os.path, configparser
import termika_docx_parser, termika_xlsx_parser, indigo_txt_parser, termika_docx_2_parser
from logger import TLogger


def create_answer(a):
    a = {"Content": '<div style=\"text-align: justify;\">' + a[2] + '</div>',
         "IsCorrect": False if a[1] == 0 else True
         }
    return a


def create_tag():
    tag = {"Content": ""}
    return tag


def create_question(q):
    if q[3] != "none": img = '<div>'+q[3]+'</div>'
    else: img = ''
    d = {"Content": '<div align=\"center\"><b>' + q[2] + '</b></div>',
         "Help": '<div style=\"text-align:justify;\">' + q[1] + '</div>',
         "QuestionAnswerType": 0,
         "QuestionMainImg": img,
         "Answers": [create_answer(a) for a in q[4]],
         "Tags": [create_tag()],
         "MaterialHeader": ""
         }
    return d


def create_course(data, course_code, course_name, questions):
    data.update({"Code": course_code,
                 "EditorVersion": "1.4.9",
                 "XmlFilename": course_code + ".xml",
                 "Name": course_name,
                 "MaterialVersion": 2
                 })
    data.update({"Topics": [{"Name": "Тема 1.",
                             "Description": "Описание темы 1",
                             "Questions": [create_question(q) for q in questions],
                             "Documents": [{"Name": "Документ1", "FileName": ""}],
                             "Scorms": [{"Name": "", "Path": "", "Link": "/1/start.html", "IsResponsive": False}]}]})
    return 0

def make_number(number, max_char):
    st = f"{int(start_number)+int(number)-1}"
    if len(st) >= max_char: return st
    cn = max_char-len(st)
    st = "0"*cn+st
    return st

file_name = ""

path = "config.ini"
if not os.path.exists(path):
    TLogger.WriteLog("Error", "Не удалось загрузить настройки из файла")
    exit(1)
config = configparser.ConfigParser()
try:
    config.read(path, encoding="utf8")
except configparser.Error as e:
    TLogger.WriteLog("Error", "Ошибка в файле конфигурации: {}".format(e))
    exit(1)

course_code = config.get("Main", "coursecode").strip()+" "
start_number = config.get("Main", "startnumber")
maxchar = int(config.get("Main", "maxchar"))
source_format = config.get("Main", "sourceformat")
src_path = config.get("Main", "srcpath")
rigth_symbol = config.get("Main","rigthsymbol")
TLogger.LogLevel = config.get("Main","loglevel").split(",")
TLogger.WriteLog("Info", f"В настройках включен уровень логирования: {TLogger.LogLevel}")
# docx_parser.parse_table('src//'+file_name, 3, questions)
if not os.path.exists(src_path):
    TLogger.WriteLog("Error", "Не удалось найти каталог с исходными файлами для экспорта")
    exit(1)

counter = 0
for root, dirs, files in os.walk(src_path, topdown=True):
    for fl in files:
        data = {}
        questions = []
        course_name = ""
        if fl.endswith('txt') and source_format == "indigo_txt":
            counter += 1
            TLogger.WriteLog("Info", f"Конвертируем файл: {fl} в курс: {course_code + make_number(str(counter),maxchar)}")
            try:
                indigo_txt_parser.indigo_txt_parser(os.path.join(root, fl), questions)
            except Exception as e:
                TLogger.WriteLog("Error", "Ошибка обработки файла с тестами: {}".format(e))
        elif fl.endswith('docx') and source_format == "termika_docx":
            counter += 1
            TLogger.WriteLog("Info", f"Конвертируем файл: {fl} в курс: {course_code + make_number(str(counter),maxchar)}")
            #termika_docx_parser.parse_table(os.path.join(root, fl), questions)
            try:
                termika_docx_parser.parse_table(os.path.join(root, fl), questions)
            except Exception as e:
                TLogger.WriteLog("Error", "Ошибка обработки файла с тестами: {}".format(e))
        elif fl.endswith('docx') and source_format == "termika_docx_2":
            counter += 1
            TLogger.WriteLog("Info", f"Конвертируем файл: {fl} в курс: {course_code + make_number(str(counter),maxchar)}")
            #termika_docx_parser.parse_table(os.path.join(root, fl), questions)
            #termika_docx_2_parser.parse_docx_2(os.path.join(root, fl), questions)
            try:
                termika_docx_2_parser.parse_docx_2(os.path.join(root, fl), questions)
            except Exception as e:
                TLogger.WriteLog("Error", "Ошибка обработки файла с тестами: {}".format(e))
        elif fl.endswith('xlsx') and source_format == "termika_xlsx":
            counter += 1
            TLogger.WriteLog("Info", f"Конвертируем файл: {fl} в курс: {course_code + make_number(str(counter),maxchar)}")
            try:
                course_name = termika_xlsx_parser.parse_table(os.path.join(root, fl), questions, rigth_symbol)
            except Exception as e:
               TLogger.WriteLog("Error", "Ошибка обработки файла с тестами: {}".format(e))
        else:
            continue

        if course_name == "": course_name = fl[0:len(fl) - 4]
        #create_course(data, course_code + make_number(str(counter),maxchar), course_name, questions)

        try:
           if course_name == "": course_name = fl[0:len(fl) - 4]
           create_course(data, course_code + make_number(str(counter),maxchar), course_name, questions)
        except Exception as e:
            TLogger.WriteLog("Error", "Ошибка создания курса в формате ОЛИМПОКС: {}".format(e))
        dst_folder = os.path.join(os.getcwd(), "dst", course_code + make_number(str(counter),maxchar))
        os.makedirs(dst_folder, exist_ok=True)
        with open(dst_folder + "//" + "course.json", "w", encoding="utf8") as write_file:
            json.dump(data, write_file, ensure_ascii=False)
TLogger.WriteLog("Info",f"Импорт файлов в ОКС:Курс выполнен. Результат в папке: {os.path.abspath(os.curdir)}\dst")
k = input("Нажмите Ввод для закрытия окна")