from handlers.dispatcher import *


def main(file_name="result.xlsx"):

    """Credit: website https://snipp.ru/tools. Snipp.ru - все для веб-разработчиков"""

    l_list = []
    count_errors = 0
    fatal_errors = 0

    try:
        df_init = pd.read_excel('required files/addresses.xlsx')
        address_list = df_init['L'].tolist()

        website = "https://snipp.ru/tools/address-coord"

        for i in range(0, len(address_list)):
            coord = ''
            address = str(df_init['L'][i])
            try_ = 0

            while coord == '':
                try_ += 1
                try:
                    if try_ >= 2:

                        print(f"It's my {try_} try on getting the value... ")
                        count_errors += 1
                    elif try_ > 9:
                        fatal_errors += 1
                        coord = None
                        break
                    driver.get(website)
                    input_field = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "ymaps-b-form-input__input")))

                    input_field.send_keys(address)
                    find_button = driver.find_element(By.CLASS_NAME, 'ymaps-b-form-button__text')
                    find_button.click()

                    coord_holder = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, "ypoint")))
                    coord_holder.send_keys('')

                    coord = driver.find_element(By.ID, 'ypoint').get_attribute('value')

                except Exception as ex:

                    print(ex)
                    coord = ''

            l_list.append(coord)

            print(f"{i}: {address}: {coord}")

        dictionary = {

            'address': address_list,
            'coordinates': l_list}

        df_result = pd.DataFrame.from_dict(dictionary)
        print(df_result)

        with pd.ExcelWriter(f"output/{file_name}", engine='xlsxwriter') as writer:
            df_result.to_excel(writer, index=False)

    except Exception as ex:  # if file execution breaks - creates a file that includes partial saved data

        with open("output/partial_data.txt", "w+") as file:
            file.write(f"{datetime_stamp}\nL_LIST: {l_list}\n{ex}\n")
        print(ex)
        time.sleep(10)

    finally:
        print(f"Done! Total error count was {count_errors} and the number of missing values is {fatal_errors}")
        print(f"The resulting excel table is {file_name}")
        driver.close()


if __name__ == '__main__':
    main()
