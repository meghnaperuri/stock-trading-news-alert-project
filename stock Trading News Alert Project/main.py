import requests
import datetime as dt
import smtplib
from googletrans import Translator, LANGUAGES


my_email="meghnaperuri222@gmail.com"
password="awjqsxdrmduedxus"

x=dt.datetime.now()
day=x.day
month=x.month
year=x.year
# print(day, month, year)
def translate_to_english(text):
    translator = Translator()
    translated_text = translator.translate(text, dest='en')
    return translated_text.text
def print_news():
    API_KEY_NEWS="d44fe49439cd426b94f2e658fb45b805"
    NEWS_ENDPOINT=f"https://newsapi.org/v2/everything?q=tesla&from=2024-02-20&sortBy=publishedAt&apiKey={API_KEY_NEWS}"
    news=requests.get(NEWS_ENDPOINT)
    news_data=[]


    for i in range(0,3):
        # print(news.json()["articles"][i]["title"])
        news_data.append(translate_to_english(news.json()["articles"][i]["title"]))
    return news_data


def stock_calculator():
    try:
        API_KEY_STOCK="RH44AQUWFAXISJK5"
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TSLA&apikey={API_KEY_STOCK}"
        r = requests.get(url)
        r.raise_for_status()
        code=r.status_code
        if code==200:
            yesterdays_date=f"{year}-0{month}-{day-1}"
            day_before_yesterday_date=f"{year}-0{month}-{day-2}"
            print(yesterdays_date)
            data_yest = r.json()["Time Series (Daily)"][yesterdays_date]["4. close"]
            data_dayBefore_yest=r.json()["Time Series (Daily)"][day_before_yesterday_date]["4. close"]

            diff=float(data_yest) - float(data_dayBefore_yest)
            if diff < 0:
                update = "📉decrease in the stock"
                news = print_news()
                # print(news)
                send_email(news, update)

            else:
                update = "📈increase in the stock"
                news = print_news()
                # print(news)
                send_email(news, update)
    except KeyError:
        print("limit exceeded.")
        return []


def send_email(news, update):
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        subject = f"STOCK {update}"
        body = "\n".join(news)
        msg = f"Subject: {subject}\n\n{body}"
        connection.sendmail(
            from_addr=my_email,
            to_addrs="mperuri@gmu.edu",
            msg=msg.encode("utf-8")
        )
    print("email sent!")

stock_calculator()