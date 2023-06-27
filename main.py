import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import sys
import json
import os

api_key = "69425251c4acad99d5539cdec6bfecf1"
directory = 'C:\.ADSPOWER_GLOBAL\cache'
#chrome_path = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
ADS_ids_txt = "ADS_ids.txt"


def ads_id_from_cache():
    # Получение списка профилей из кэша
    if not os.path.exists(ADS_ids_txt):
        # Получение списка папок в директории
        folders = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
        # Запись названий папок в файл
        with open(ADS_ids_txt, 'w') as file:
            for folder in folders:
                parts = folder.split('_')
                folder = parts[0]
                file.write(folder + '\n')
        print('ID профилей сохранены в файл: ', ADS_ids_txt)
        print('При необходимости, измените их порядок в указанном файле.')


def set_def_settings():
    # Задание первичных настроек
    if not os.path.exists("settings.json"):
        profiles_count = input("Сколько профилей открывать одновременно? (Пример ответа: 3)")
        data = {
            "pr_count": profiles_count
        }
        json_data = json.dumps(data, indent=4)
        with open("settings.json", "w") as file:
            file.write(json_data)


def main():

    ads_id_from_cache()
    set_def_settings()

    # Открытие файла для чтения
    with open(ADS_ids_txt, "r") as file:
        # Чтение содержимого файла и запись в список
        ids = file.readlines()

        # Удаление символа новой строки "\n" из каждой строки
        ids = [line.strip() for line in ids]

    # Вывод списка
    print(ids)


    # ads_folder = "j5v7h6t_gl40mk"
    # ads_id = "j5v7h6t"
    #
    # open_url = "http://localhost:50325/api/v1/browser/start?user_id=" + ads_id
    # close_url = "http://localhost:50325/api/v1/browser/stop?user_id=" + ads_id
    #
    # resp = requests.get(open_url).json()
    # if resp["code"] != 0:
    #     print(resp["msg"])
    #     print("please check ads_id")
    #     sys.exit()
    #
    # chrome_driver = resp["data"]["webdriver"]
    # service = Service(chrome_driver)
    # chrome_options = Options()
    # chrome_options.add_experimental_option("debuggerAddress", resp["data"]["ws"]["selenium"])
    # driver = webdriver.Chrome(service=service, options=chrome_options)
    # print(driver.title)
    # driver.get("https://github.com/AdsPower/localAPI/blob/main/py-examples/example-start-profile.py")
    #time.sleep(5)
    #driver.quit()
    #requests.get(close_url)


if __name__ == '__main__':
    main()





