import pandas_datareader.data as web
import datetime
import time
import pyodbc

conn = pyodbc.connect(r'DSN=sqlnetflix')
cur = conn.cursor()


while True:
    try:
        t = web.get_quote_google('ITV')
        #stamp = datetime.datetime.strptime(str(t.at['ITV', 'time']), '%Y-%m-%d %H:%M:%S')
        timestamp = datetime.datetime.now()
        cur.execute('insert into dbo.TickerITV ( last, timestamp) values (?,?)', t.at['ITV', 'last'], timestamp)
        conn.commit()
        time.sleep(9.7)
    except:
        cur.execute('insert into dbo.TickerTimer ( last, timestamp) values (?,?)', '-', datetime.datetime.now())
        conn.commit()
        print('@LADBANTER')

