import requests
import bs4
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import clipboard
from selenium.webdriver.common.by import By
import time
import pytesseract
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
options = Options()
options.headless = True

driver = webdriver.Firefox(options=options)


def main():
    L_list = []

    try:
        df_init = pd.read_excel('addresses.xlsx')

        website = "https://snipp.ru/tools/address-coord"

        for i in range(0, len(df_init)):
            driver.get(website)
            address = str(df_init['L'][i])
            input_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ymaps-b-form-input__input")))

            input_field.send_keys(address)
            find_button = driver.find_element(By.CLASS_NAME, 'ymaps-b-form-button__text')
            find_button.click()
            time.sleep(3)
            copy_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "ypoint-copy"))).click()

            coord = clipboard.paste()
            dictionary = {address: coord}
            print(dictionary)
            L_list.append(dictionary)

            time.sleep(1)
        df_result = pd.DataFrame(L_list)
        df_result.to_csv('RESULT.csv')
    except Exception as ex:

        print(ex)
        time.sleep(10)
    finally:

        driver.close()


if __name__ == '__main__':
    main()
