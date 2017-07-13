import MySQLdb

try:
    conn = MySQLdb.connect(host="localhost", user="root", 
                           passwd="1234", db="mobilservice")
except MySQLdb.Error as err:
    print("Connection error: {}".format(err))
    conn.close()

sql = "SELECT `note` from `application` WHERE id = 1"
    
try:
    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SET NAMES utf8")
    cur.execute(sql)
    data = cur.fetchall()
except MySQLdb.Error as err:
    print("Query error: {}".format(err))

print(data[0]['note'])
#print(data[0]['test'])   
#print(type(data[0]['note']))	