# Утилита для конвертации тестов из файлов формата DOCX, XLSX, TXT в ОЛИМПОКС:Редактор

Утилита позволяет сформировать тесты, подготовленные в формате docx, xlsx, txt, в формате обучающих продуктов ОКС:Курс для последующей загрузки в систему ОЛИМПОКС или ОЛИМПОКС:Предприятие.

Файлы docx, xlsx, txt должны быть подготовлены по специальным шаблонам, которые можно найти в папке [src](https://github.com/kvorob/olimpoks-course-gen/tree/main/src).

## Как пользоваться данным конвертором

Для запуска утилиты необходимо:
1.  Загрузить zip архив из каталога [install](https://github.com/kvorob/olimpoks-course-gen/raw/main/install/olimpoks-course-gen.zip)
1.	Распаковать архив с файлами утилиты на локальном диске компьютера.
2.	В папку “src”  скопировать файлы с тестами (docx, txt), подготовленные по шаблонам. 
3.	Запустить исполняемый файл Course_gen.exe из места распаковки архива (п.1).  
4.  После окончания работы утилиты результирующие курсы будут записаны в папку “dst”. Она расположена там же, где находится запускаемый файл.
6.	Сформированные утилитой курсы, Вы сможете открыть с помощью ОЛИМПОКС:Редактор, внести необходимые изменения (например, указать правильное наименование теста) и сформировать пакет для загрузки в систему ОЛИМПОКС.

В операционных системах Linux или MacOS запуск утилиты осуществляется из командной стороки:

```
python Course_gen.py

```

Утилита поддерживает загрузку тестов только закрытого типа, с одним или несколькими правильными вариантами ответов на вопрос.

## Настройка утилиты

Для настройки утилиты необходимо внести соответствующие изменения в файл config.ini

**Внимание !** По умолчанию утилита настроена на работу с файлами xslsx.

**Изменения:** 
04/04/2024: В текущей версии утилиты появилась возможность загружать тесты из шаблона xlsx в курс ОЛИМПОКС с разбивкой на темы. Для этого блоки вопросов должны быть разделены строкой в которой первые 4 ячейки объеденены и в них содержится наименование темы. Пример можно посмотреть в шаблоне в папке dst\ 

Описание файла настроек:

```
[Main]
# Префикс наименования папки ОКС:Курс
coursecode = ter
startnumber = 1
maxchar = 4
# Шаблон тестов который надо обрабатывать
# sourceformat = indigo_txt
#sourceformat = termika_docx
#sourceformat = termika_xlsx
sourceformat = termika_docx_2
# Используется для sourceformat termika_xlsx
rigthsymbol = V
# Каталог с исходными файлами для конвертации. Может размещаться в любом месте, например: srcpath = c:\src\
srcpath = src\
# Ширина картинки к которой будет приведена картинка из загружаемого файла
image_max_width = 550
# Уровень логирования процесса конвертации
# loglevel = Error,Info,Debug,Warning
loglevel = Error,Info,Debug
# Наименование лог-файла 
logfile = application.log
```

## Куда обращаться за помощью

**Внимание !** Данная утилита не является официальным программным продуктом компании ТЕРМИКА. Она разрабатывается и сопровождается энтузиастами и пользователями программных продуктов ОЛИМПОКС на принципах свободно распространяемого ПО. 

**Пожалуйста**, не пытайтесь обращаться в официальную техническую поддержку системы ОЛИМПОКС, они не смогут Вам помочь.
Если у Вас возникли проблемы с запуском утилиты, выявили ошибки в ее работе или хотите предложить улучшения, обращайтесь по электронной почте на адрес: kv@kvorob.ru

