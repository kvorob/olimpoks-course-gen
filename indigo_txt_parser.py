def get_question_type(ans_list):
# Типы вопросов:
# 1 - Выбор одного правильного отевета (*....)
# 2 - Выбор нескольких правильных ответов (#....)
# 3 - Ввод с клавиатуры ([....])
# 4 - Установка соответствия (....=....)
# 5 - Расстановка в нужном порядке (....)
   isType4 = False
   isType4Counter = 0
   for item in ans_list:
      if item[0] == "*": return 1
      if item[0] == "#": return 2
      if item[0] == "[": return 3
      if item.find("=") !=-1:
         isType4 = True
         isType4Counter += 1
         if isType4Counter == len(ans_list):return 4
   return 5

def create_answer(a_item,q_type):
   str = ""
   isCorrect = 0
   if a_item[0] =="*" or a_item[0] =="#":
      str = a_item[1:]
      isCorrect = 1
   else: str = a_item
   return [0,isCorrect,str]

def create_question(qs,i):
   q_item = []
   q_type = get_question_type(qs[1:len(qs)])
   if q_type == 3 or q_type == 4: return # вопросы 3 и 4 типа пока не поддерживаем
   q_item = [i,"Текст помощи отсуствует",qs[0],"none"]
   a_items = [create_answer(a_item,q_type) for a_item in qs[1:len(qs)]]
   q_item.append(a_items)
#   print(f"{q_type}: {q_item}")
   return q_item

def indigo_txt_parser(fname, questions):
   with open(fname,"r", encoding="windows-1251") as exp_file:
      i=0
      qs = []
      for line in exp_file:
         if len(line) <= 1:
            i += 1
            questions.append(create_question(qs,i))
            qs = []
            continue
         qs.append(line.strip())
      if len(qs)>0:
         i += 1
         questions.append(create_question(qs,i))

if __name__ == '__main__':
   questions = []
   filename = 'src//СТО КИСМ 121-22-2018_Подрядные организации.txt'
   indigo_txt_parser(filename,questions)

