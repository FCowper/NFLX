import pandas_datareader.data as web
import datetime
import sched, time
import pyodbc

conn = pyodbc.connect(r'DSN=crimesqlcon')
cur = conn.cursor()

s = sched.scheduler(time.time, time.sleep)
def ticker(sc):
    t = web.get_quote_google('WFM')
    cur.execute('insert into dbo.TickerTimer (change_pct, last, time) values (?,?,?)', t.at['WFM', 'change_pct'],t.at['WFM', 'last'], t.at['WFM', 'time'])
    conn.commit()
    s.enter(60, 1, ticker, (sc,))


s.enter(60, 1, ticker, (s,))
s.run()