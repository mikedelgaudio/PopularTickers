from sqlite3.dbapi2 import Date
from bs4 import BeautifulSoup
import requests
import sqlite3
import time
import schedule
from dotenv import load_dotenv
import os
from notifications import emailMe



def main():
    load_dotenv()
    try:
        conn = sqlite3.connect('popular_tickers.db')
    except Exception as err:
        print("Error Connecting to Database")
        conn.close()

    try:
        r = requests.get("https://eresearch.fidelity.com/eresearch/gotoBL/fidelityTopOrders.jhtml")
        soup = BeautifulSoup(r.content, features="html.parser")
    except Exception as err:
        print("Error grabbing page: {0}".format(err))
        conn.close()

    stocks = []

    for ticker_tag in soup.find_all('td', class_='second'):
        stocks.append([ticker_tag.find("span").get_text()])

    for i, company_tag in enumerate(soup.find_all('td', class_='third')):
        stocks[i].append(company_tag.get_text())

    for i, price_change in enumerate(soup.find_all('td', class_='fourth')):
        price_amount = price_change.find("span").get_text()
        price_amount = float(price_amount)
        stocks[i].append(price_amount)
    
    for i, buy_orders in enumerate(soup.find_all('td', class_='fifth')):
        buy_amount = buy_orders.find("span").get_text()
        buy_amount = int(buy_amount)
        stocks[i].append(buy_amount)

    for i, sell_orders in enumerate(soup.find_all('td', class_='seventh')):
        sell_amount = sell_orders.find("span").get_text()
        sell_amount = int(sell_amount)
        stocks[i].append(sell_amount)

    for stock in stocks:
        #addToDb(stock, conn)
        pass

    emailMe()
    
    conn.close()

def addToDb(stock, conn):
    '''
    If stock at [0] == ticker && price of previous day do not insert (means it was a holiday)
    '''
    conn.execute("INSERT INTO stocks (ticker, company, price_change, buys, sells) VALUES (:ticker, :company, :price, :buys, :sells);", {'ticker': stock[0], 'company': stock[1], 'price': stock[2], 'buys': stock[3],'sells': stock[4]})
    conn.commit()
    print("executed")

# def emailMe():
#     port = 465 
#     smtp_server = "mail.delgaudiomike.com"
#     sender_email = os.environ.get("EMAIL_USER") 
#     receiver_email = "delgaudiomike@gmail.com" 
#     password = os.environ.get("EMAIL_PASS")
#     message = MIMEMultipart("alternative")
#     message["Subject"] = "[POPULAR TICKERS] {}".format(date.today().strftime("%m/%d/%y"))
#     message["From"] = sender_email
#     message["To"] = receiver_email

#     html = """\
#     <html>
#     <body>
#         <h1>Today's most popular trade: ''</h1>
#         <h2>Most frequent for this week: ''</h2>
#         <h2>Here are new tickers that first appeared today: ''</h2>
#     </body>
#     </html>
#     """
#     part2 = MIMEText(html, "html")
#     message.attach(part2)
#     try:
#         server = smtplib.SMTP_SSL(smtp_server, port)
#         server.login(sender_email, password)
#         server.sendmail(sender_email, receiver_email, message.as_bytes())
#     except Exception as err:
#         print(err)
#     finally:
#         server.quit()
   

def allMostPopular(conn):
    c = conn.execute("SELECT ticker, COUNT(*) AS frequency FROM stocks GROUP BY ticker ORDER BY frequency DESC")
    print(c.fetchall())

main()

# schedule.every().day.at("17:00:00").do(main)

# while True:
#     schedule.run_pending()
#     time.sleep(60)
#     print("running")

# Protect against INSERT in less than 24hrs for debug or add a debug mode