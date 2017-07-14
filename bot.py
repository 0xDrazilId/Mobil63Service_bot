import config
import telebot
import MySQLdb

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start']) #команда /start
def start_conversation(message):
	bot.send_message(message.chat.id, "Просто пришлите боту номер вашей квитанции:")

@bot.message_handler(content_types=["text"]) #если прислали текст
def answer_message(message):
	try:
		conn = MySQLdb.connect(host=config.dbhost, user=config.dbuser, passwd=config.dbpasswd, db=config.dbname, charset=config.dbcharset)

	except MySQLdb.Error as err: 
		print("Connection error: {}".format(err)) #обработка ошибки подключения с указанными параметрами
		conn.close()

	try:
		cur = conn.cursor(MySQLdb.cursors.DictCursor) #подключаемся первый раз, чтобы узнать первый и последний номер элемента таблицы
		cur.execute("SET NAMES utf8")
		cur.execute("SELECT `id` from `application` order by `id` desc limit 1;")
		LAST_BASE_ID = cur.fetchall()
		cur.execute("SELECT `id` from `application` order by `id` limit 1;")
		FIRST_BASE_ID = cur.fetchall()
	except MySQLdb.Error as err: #если не удалось подключиться
		print("Query error: {}".format(err))

	if (message.text.isdecimal()): #если введенный текст = десятичное число
		if(int(message.text) > LAST_BASE_ID[0]['id'] or int(message.text) < FIRST_BASE_ID[0]['id']): #если не входит в радиус допустимых значений
			bot.send_message(message.chat.id, "Извините, вашей заявки нет в базе либо число слишком большое")
		else: #если входит в радиус
			sql = "SELECT `status`, `note`, `device`, `deadline` from `application` WHERE id = " + message.text #экранировать не нужно, есть проверка на текст
			try:
				cur = conn.cursor(MySQLdb.cursors.DictCursor)
				cur.execute(sql)
				data = cur.fetchall() #data - список со словарём, параметра - 2 [] и ['']
			except MySQLdb.Error as err:
				print("Query error: {}".format(err))

			result = "📌 Номер квитанции → " + message.text + "\n📱 Аппарат → "+ data[0]['device'] + "\n🔧 Статус ремонта → " + data[0]['status'] + "\n🕙Будет готов → " + str(data[0]['deadline']) + "\n📝 Комментарий → " + data[0]['note']
			bot.send_message(message.chat.id, result) #выводим всё красиво
	else:
		bot.send_message(message.chat.id, "Неверный формат!\nВведите номер квитанции без точек, тире и прочих знаков: ") 

if __name__ == '__main__':
    bot.polling(none_stop=True)