from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pytesseract
from selenium.webdriver.firefox.options import Options


options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)
website = "https://urait.ru/viewer/gorodskaya-logistika-gruzovye-perevozki-486420#page/1"
driver.get(website)

# elem = driver.find_element_by_name('user')
# elem.clear()
# elem.send_keys("eadavydova_1@edu.hse.ru")
# elem = driver.find_element_by_name('pass')
# elem.clear()
# elem.send_keys("Pm8VGeUYH")
# elem.send_keys(Keys.RETURN)

# open file
file1 = open("output/uchhebnik.txt", "w+")
file1.truncate(0)
time.sleep(10)

try:

    for i in range(34):
        page = i+1
        site = website + str(page)
        # viewer.loaded.fullscreen div#viewer__wrapper div#viewer__wrapper__buttons
        driver.get(site)
        driver.find_element_by_xpath('/html/body/div/div[3]/div[4]/div[3]').click()
        driver.get_screenshot_as_file('screenshot'+str(i+1)+'.png')
        text = pytesseract.image_to_string('screenshot'+str(i+1)+'.png', lang='rus')
        file1.write(text)
        print(page)

except Exception as ex:
    print(ex)
finally:
    driver.close()
    file1.close()