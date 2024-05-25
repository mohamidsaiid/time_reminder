import time
from winotify import Notification, audio
import mysql.connector
from datetime import datetime, date



class sql:
    def __init__(self) -> None:
        self.__d = datetime.today().date()
        self.__m = ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May.', 'Jun.', 'Jul.', 'Aug.', 'Sept', 'Oct.', 'Nov.', 'Dec.']
        self.__x = []
        self.__x.append(self.__d)
        
    def __connect_and_execute(self,query):
        try:
            connection = mysql.connector.connect(
               user='root',password='9625', host = '127.0.0.1', database = 'timer_app'
            )
            cursor = connection.cursor()
            cursor.execute(query)
            # Fetch results if needed
            # ...
        except mysql.connector.Error as err:
            print(err)
        finally:
            if connection and connection.is_connected():
                connection.close()

    def __connect_and_execute(self,query, data):
        try:
            connection = mysql.connector.connect(
                user='root',password='9625', host = '127.0.0.1', database = 'timer_app'
            )
            cursor = connection.cursor()

            cursor.execute(query,data)
            connection.commit()
            # Fetch results if needed
            # ...
        except mysql.connector.Error as err:
            print(err)
        finally:
            if connection and connection.is_connected():
                connection.close()


    def start_new_day(self):
        def get_date_of_today():
            #get date of today
            return [self.__d, int(self.__d.strftime('%m'))]


        date_today = get_date_of_today()

        insert_row = "insert into days (dates, sessions, month) values (%s, 1, %s)"
        data = (date_today[0],self.__m[date_today[1]-1])
        self.__connect_and_execute(insert_row, data)


    def update_on_existing_day(self):
        if self.__d != datetime.today().date():
            self.__d = datetime.today().date()
            print("starting a new day")
            self.start_new_day()
            return
        
        s = "select sessions from days where dates = %s"
        connection = mysql.connector.connect(
            user='root',password='9625', host = '127.0.0.1', database = 'timer_app'
        )
        cursor = connection.cursor()

        cursor.execute(s, self.__x)    
        cnt = 1
        res = 0
        for i in cursor:
            if cnt == 0:
                break
            res = i[0]
            cnt -= 1

        update_row = "update days set sessions = %s where dates = %s"
        self.__connect_and_execute(update_row, (res+1,self.__d))

    def update_spent_hours(self):
        queury = "update days set hours = hours + 0.5 where dates = %s"
        self.__connect_and_execute(queury, self.__x)

    def chck(self):
        cnx = mysql.connector.connect(user='root',password='9625', host = '127.0.0.1', database = 'timer_app')
        cursor = cnx.cursor()
        querey = ("select dates from days where dates = %s order by dates desc")
        cursor.execute(querey,self.__x)
    
    
        for i in cursor:
            if i[0] == self.__d:

                cursor.close()
                cnx.close()

                return True

        cursor.close()
        cnx.close()
        return False

working_database = sql()        
hour = 0
def strt():
    if working_database.chck():
        working_database.update_on_existing_day()
    else:
        working_database.start_new_day()
    noti = Notification(
        app_id="App started",
        title=f"Time started",
        msg=f"Hello", 
        icon=r"C:\Users\msaee\OneDrive\Desktop\test\time reminder\hot-air-balloon_8006915.png")
    noti.set_audio(audio.Default, loop=False)
    noti.show()
    


def notfication(hours):
    working_database.update_spent_hours()
    noti = Notification(
        app_id="every hour",
        title=f"SPENT ANOTHER HALF HOUR",
        msg=f"SPENT {hour} hour", 
        icon=r"C:\Users\msaee\OneDrive\Desktop\test\time reminder\skull.512x512.png")
    noti.set_audio(audio.Default, loop=False)
    noti.show()

strt()

while True:
    time.sleep(1800)
    hour += 0.5
    notfication(hour)

