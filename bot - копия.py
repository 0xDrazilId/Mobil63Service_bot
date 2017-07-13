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
		conn = MySQLdb.connect(host="localhost", user="root", passwd="1234", db="service123")

	except MySQLdb.Error as err:
		print("Connection error: {}".format(err))
		conn.close()

	sql = "SELECT description FROM table1 WHERE id = " + message.text
	    
	try:
		cur = conn.cursor(MySQLdb.cursors.DictCursor)
		cur.execute(sql)
		data = cur.fetchall()
	except MySQLdb.Error as err:
		print("Query error: {}".format(err))
	bot.send_message(message.chat.id, data[0]['description'])

if __name__ == '__main__':
    bot.polling(none_stop=True)