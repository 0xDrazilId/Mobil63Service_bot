import config
import telebot
import MySQLdb

bot = telebot.TeleBot(config.token)
#пробуем установить соединение с указанными параметрами
try:
	conn = MySQLdb.connect(host=config.dbhost, user=config.dbuser, passwd=config.dbpasswd, db=config.dbname, charset=config.dbcharset)

except MySQLdb.Error as err: 
	print("Connection error: {}".format(err)) #обработка ошибки подключения с указанными параметрами
	conn.close()
#один раз пробуем подключиться для получения двух глобальных переменных,
#чтобы не подключаться к базе при каждом сообщениии
try:
	cur = conn.cursor(MySQLdb.cursors.DictCursor) #подключаемся первый раз, чтобы узнать первый и последний номер элемента таблицы
	cur.execute("SET NAMES utf8")
	cur.execute("SELECT `id` from `application` order by `id` desc limit 1;")
	LAST_BASE_ID = cur.fetchall()
	cur.execute("SELECT `id` from `application` order by `id` limit 1;")
	FIRST_BASE_ID = cur.fetchall()
except MySQLdb.Error as err: #если не удалось подключиться
	print("Query error: {}".format(err))

#если прислали команду /start
@bot.message_handler(commands=['start']) 
def start_conversation(message):
	bot.send_message(message.chat.id, "#️⃣ Просто пришлите боту номер вашей квитанции:")

#О разработчике /about
@bot.message_handler(commands=['about']) 
def about_me(message):
	bot.send_message(message.chat.id, "Разработка данного бота - @feraf\nОбращайтесь!😉")

#если прислали не текст
@bot.message_handler(content_types=["document", "audio", "voice", "contact", "video", "location"])
def notext(message):
	bot.send_message(message.chat.id, "😄Извините, но мне врядли понадобятся Ваши файлы и прочий контент, попробуйте нажать /start чтобы начать работу и /about чтобы увидеть информацию о разработчике")

#если прислали стикер
@bot.message_handler(content_types=["sticker"])
def notext(message):
	bot.send_message(message.chat.id, "😊Классный стикер!\nЕсли вы хотите свой стикерпак, разработчик этого бота может вам его нарисовать\n👍Обращайтесь - @feraf")	

#если прислали текст
@bot.message_handler(content_types=["text"]) 
def answer_message(message):
	if (message.text.isdecimal()): #если введенный текст = десятичное число
		if(int(message.text) > LAST_BASE_ID[0]['id'] or int(message.text) < FIRST_BASE_ID[0]['id']): #если не входит в радиус допустимых значений
			bot.send_message(message.chat.id, "🤷‍♂️ Такой заявки нет в базе. Проверьте номер и попробуйте еще раз: ")
		else: #если входит в радиус
			sql = "SELECT `status`, `worked`, `device`, `deadline` from `application` WHERE id = " + message.text #экранировать не нужно, есть проверка на текст
			try:
				cur = conn.cursor(MySQLdb.cursors.DictCursor) #подключаемся второй раз чтобы выполнить запрос
				cur.execute(sql)
				data = cur.fetchall() #data - список со словарём, параметра - 2 [] и ['']
			except MySQLdb.Error as err:
				print("Query error: {}".format(err))

			result = "📌 Номер квитанции → " + message.text + "\n📱 Аппарат → "+ data[0]['device'] + "\n🔧 Статус ремонта → " + data[0]['status'] + "\n🕙Будет готов → " + str(data[0]['deadline']) + "\n📝 Комментарий → " + data[0]['worked']
			bot.send_message(message.chat.id, result) #выводим всё красиво
	else:#если прислали что-то кроме цифр
		bot.send_message(message.chat.id, "⚠️ Неверный формат!\nВведите номер квитанции без точек, тире и прочих знаков: ") 

if __name__ == '__main__':
    bot.polling(none_stop=True)