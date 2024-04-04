import docx
from docx.text.paragraph import Paragraph
from docx.document import Document
from docx.table import _Cell, Table
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl


def iter_block_items(parent):
    if isinstance(parent, Document):
        parent_elm = parent.element.body
    elif isinstance(parent, _Cell):
        parent_elm = parent._tc
    else:
        raise ValueError("something's not right")

    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            table = Table(child, parent)
            yield table

def isMarked(cell):
    #Проверяем есть ли цветовое выделение, если есть, значит правильный вариант ответа
    for para in cell.paragraphs:
        for run in para.runs:
            if run.font.highlight_color:
                if len(run.text) > 2:
                    return True

    return False

def getText(filename, qs):
    doc = docx.Document(filename)
    a = []  # список варантов ответов для текущего вопроса
    q = []  # список текущий вопрос + текст помощи
    vcount = 0
    buf = ""
    for block in iter_block_items(doc):
        if isinstance(block, Paragraph):
            if len(block.text) == 0: continue
            buf += block.text
        elif isinstance(block, Table):
            # print("Пришла таблица:")
            vcount += 1
            print(f"Вопрос {vcount}: {buf}")
            q = [len(qs) + 1] + [f"Номер вопроса в исходном файле: {vcount}"] + [buf.strip()] + ["none"]
            acount = 0
            buf = ""
            for row in block.rows:
                for cell in row.cells:
                    buf += cell.text
                acount += 1
                print(f"Ответ {acount} ({isMarked(cell)}): {buf}")
                a.append([acount, isMarked(cell), buf.strip()])
                buf = ""
            q.append(a)  # добавляем к вопросу варианты ответов
            qs.append(q)  # Добавляем вопрос с вариантам в итоговый список тестовых заданий
            q = []
            a = []

def parse_docx_3(filename, qs):
    getText(filename, qs)