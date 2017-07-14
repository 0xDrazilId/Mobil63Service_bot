import config
import telebot
import MySQLdb

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def start_conversation(message):
	bot.send_message(message.chat.id, "Просто пришлите боту номер вашей квитанции:")

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
	try:
		conn = MySQLdb.connect(host="localhost", user="root", passwd="1234", db="mobilservice", charset="utf8" )

	except MySQLdb.Error as err:
		print("Connection error: {}".format(err))
		conn.close()

	try:
		cur = conn.cursor(MySQLdb.cursors.DictCursor)
		cur.execute("SET NAMES utf8")
		cur.execute("SELECT `id` from `application` order by `id` desc limit 1;")
		LAST_BASE_ID = cur.fetchall()
		cur.execute("SELECT `id` from `application` order by `id` limit 1;")
		FIRST_BASE_ID = cur.fetchall()
	except MySQLdb.Error as err:
		print("Query error: {}".format(err))

	if (message.text.isdecimal()):
		if(int(message.text) > LAST_BASE_ID[0]['id'] or int(message.text) < FIRST_BASE_ID[0]['id']):
			bot.send_message(message.chat.id, "Извините, вашей заявки нет в базе либо число слишком большое")
		else:
			sql = "SELECT `status`, `note`, `device`, `deadline` from `application` WHERE id = " + message.text 
			try:
				cur = conn.cursor(MySQLdb.cursors.DictCursor)
				cur.execute(sql)
				data = cur.fetchall()
			except MySQLdb.Error as err:
				print("Query error: {}".format(err))

			result = "📌 Номер квитанции → " + message.text + "\n📱 Аппарат → "+ data[0]['device'] + "\n🔧 Статус ремонта → " + data[0]['status'] + "\n🕙Будет готов → " + str(data[0]['deadline']) + "\n📝 Комментарий → " + data[0]['note']
			bot.send_message(message.chat.id, result)
	else:
		bot.send_message(message.chat.id, "Неверный формат!\nВведите номер квитанции без точек, тире и прочих знаков: ") 

if __name__ == '__main__':
    bot.polling(none_stop=True)