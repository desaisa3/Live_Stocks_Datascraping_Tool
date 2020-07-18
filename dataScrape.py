from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import concurrent.futures
import pandas as pd


# SETUP SELENIUM
options = Options()
options.add_argument('headless')
options.add_argument('--disable-gpu')

# SET UP FILE READER
# section to be customized to allow user input
# user will enter tickers for stocks they wish to track
# Currently set to a static file
tickers = []
file = open("C:/Ticker_data/ticker_numbers.txt", "r")
for i in file:
    tickers.append(i[:-1])
file.close()

# function scrapes live values
# tick: list of ticker codes
def lookup(tick):
    driver_path = "C:\Drivers\chrome_driver\chromedriver.exe"
    driver = webdriver.Chrome(executable_path=driver_path, options=options)
    # driver = webdriver.Chrome(executable_path=driver_path)
    driver.get("https://web.tmxmoney.com/quote.php?qm_symbol=" + tick)
    # finding by xpath
    x_path = '//*[@id="contentWrapper"]/div/div/div/div[1]/div/div[2]/div[1]/div[2]/div/div[1]/div/span/span'
    find_value = driver.find_element_by_xpath(x_path).text
    now = datetime.now()
    driver.quit()
    return [find_value, now]

# function builds data frame with specified columns and rows equal to all the ticker codes
def build_table():
    data_f = pd.DataFrame(columns=['Current Price', 'Time'], index=tickers)
    return data_f


if __name__ == '__main__':

    df = build_table()

    # Following block uses parallelization to execute multiple processes for scraping data
    # results of data collection are added to data frame
    # looping to continuously go back and update values
    while True:
        with concurrent.futures.ProcessPoolExecutor() as executor:
            value = executor.map(lookup, tickers)

        counter = 0
        for result in value:
            df.at[tickers[counter], 'Current Price'] = result[0]
            df.at[tickers[counter], 'Time'] = result[1].strftime("%d/%m/%Y %H:%M:%S")
            counter += 1
        print(df)