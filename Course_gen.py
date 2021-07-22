import json, os, os.path, configparser
import termika_docx_parser, indigo_txt_parser
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
    d = {"Content": '<div align=\"center\"><b>' + q[2] + '</b></div>',
         "Help": '<div style=\"text-align:justify;\">' + q[1] + '</div>',
         "QuestionAnswerType": 0,
         "Answers": [create_answer(a) for a in q[3]],
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


course_name = ""
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

course_code = config.get("Main", "coursecode")
source_format = config.get("Main", "sourceformat")
src_path = config.get("Main", "srcpath")

# docx_parser.parse_table('src//'+file_name, 3, questions)
if not os.path.exists(src_path):
    TLogger.WriteLog("Error", "Не удалось найти каталог с исходными файлами для экспорта")
    exit(1)

counter = 0
for root, dirs, files in os.walk(src_path, topdown=True):
    for fl in files:
        data = {}
        questions = []
        if fl.endswith('txt') and source_format == "indigo_txt":
            TLogger.WriteLog("Info", f"Конвертируем файл: {fl}")
            counter += 1
            try:
                indigo_txt_parser.indigo_txt_parser(os.path.join(root, fl), questions)
            except Exception as e:
                TLogger.WriteLog("Error", "Ошибка обработки файла с тестами: {}".format(e))
        elif fl.endswith('docx') and source_format == "termika_docx":
            TLogger.WriteLog("Info", f"Конвертируем файл: {fl}")
            counter += 1
            # termika_docx_parser.parse_table(os.path.join(root, fl), questions)
            try:
                termika_docx_parser.parse_table(os.path.join(root, fl), questions)
            except Exception as e:
                TLogger.WriteLog("Error", "Ошибка обработки файла с тестами: {}".format(e))
        else:
            continue
        try:
            create_course(data, course_code + str(counter), fl[0:len(fl) - 4], questions)
        except Exception as e:
            TLogger.WriteLog("Error", "Ошибка создания курса в формате ОЛИМПОКС: {}".format(e))
        dst_folder = os.path.join(os.getcwd(), "dst", course_code + str(counter))
        os.makedirs(dst_folder, exist_ok=True)
        with open(dst_folder + "//" + "course.json", "w", encoding="utf8") as write_file:
            json.dump(data, write_file, ensure_ascii=False)
TLogger.WriteLog("Info",f"Импорт файлов в ОКС:Курс выполнен. Результат в папке: {os.path.abspath(os.curdir)}\dst")
k = input("Нажмите Ввод для завершения")