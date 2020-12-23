from bs4 import BeautifulSoup
import requests
import sqlite3

try:
    conn = sqlite3.connect('popular_tickers.db')
except Exception as err:
    print("Error Connecting to Database")
    conn.close()
        
try:
    r = requests.get("https://eresearch.fidelity.com/eresearch/gotoBL/fidelityTopOrders.jhtml")
    soup = BeautifulSoup(r.content)
except Exception as err:
    print("Error grabbing page: {0}".format(err))
    conn.close()


def main():
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
        addToDb(stock)


def addToDb(stock):
    conn.execute("INSERT INTO stocks (ticker, company, price_change, buys, sells) VALUES (:ticker, :company, :price, :buys, :sells);", {'ticker': stock[0], 'company': stock[1], 'price': stock[2], 'buys': stock[3],'sells': stock[4]})
    conn.commit()

main()
conn.close()