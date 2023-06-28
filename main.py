import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import sys
import json
import os
import math
import mm_lavamoat_fix_cache
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from termcolor import cprint
import colorama

#api_key = "69425251c4acad99d5539cdec6bfecf1" НЕДЕЙСТВИТЕЛЕН
directory = 'C:\.ADSPOWER_GLOBAL\cache'
#chrome_path = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
ADS_ids_txt = "ADS_ids.txt"
start_url = "https://lumpics.ru/where-are-the-extensions-in-google-chrome/#i-2"

def line_control(file_txt):
    # Удаление пустых строк
    with open(file_txt) as f1:
        lines = f1.readlines()
        non_empty_lines = (line for line in lines if not line.isspace())
        with open(file_txt, "w") as n_f1:
            n_f1.writelines(non_empty_lines)
def ads_id_from_cache():
    # Получение списка профилей из кэша
    # TODO: Изменить способ получения на обращение к api ads
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
            "pr_count": profiles_count,
            "lavamoat_fixed": False,
        }
        json_data = json.dumps(data, indent=4)
        with open("settings.json", "w") as file:
            file.write(json_data)

def get_id_numbers(group_index, group_size, total_words):
    start_index = group_index * group_size
    end_index = min(start_index + group_size, total_words)
    return list(range(start_index, end_index))

def main():
    # TODO: Добавить возможность изменения настроек
    # TODO: Добавить мультипоток
    colorama.init()
    ads_id_from_cache()
    set_def_settings()

    line_control(ADS_ids_txt)
    line_control("passwords.txt")

    # Загрузка id_ads
    with open(ADS_ids_txt, "r") as file:
        # Чтение содержимого файла и запись в список
        ids = file.readlines()
        # Удаление символа новой строки "\n" из каждой строки
        ids = [line.strip() for line in ids]

    # Загрузка параметров
    with open("settings.json", "r") as file:
        settings = json.load(file)

    # Проверка lavamoat_fix
    if not settings["lavamoat_fixed"]:

        mm_lavamoat_fix_cache.lavamoat_editor()
        settings["lavamoat_fixed"]=True
        with open('settings.json', 'w') as f:
            json.dump(settings, f)

    group_num = math.ceil(len(ids) / int(settings["pr_count"]))
    cprint("!!!Для перехода в настройки введите 0.", "yellow")
    gr_open = input("Номер открываемой группы? (Всего {}): ".format(group_num))
    gr_open = int(gr_open)-1

    # Загрузка паролей
    with open("passwords.txt", "r") as file:
        passwrds = file.readlines()
        passwrds = [line.strip() for line in passwrds]

    # Получение номеров в заданной группе
    id_nums = get_id_numbers(gr_open, int(settings["pr_count"]), len(ids))
    # Работа с профилями
    print("Открываются профили: ")
    prof_nums = list(id_nums)
    for i in range(len(prof_nums)):
        prof_nums[i] += 1
    cprint(str(prof_nums), "green")
    del prof_nums

    args1 = ["--disable-popup-blocking", "--disable-web-security"]
    args1 = str(args1).replace("'", '"')

    for id in id_nums:
        ads_id = ids[id]
        # TODO: Разобраться с launch_args и найти способ открывать url при запуске;
        # TODO: Вынести start_url в settings.json

        open_url = "http://localhost:50325/api/v1/browser/start?user_id=" + ads_id+"&open_tabs=1" + f"&launch_args={str(args1)}"
        # print(open_url)
        resp = requests.get(open_url).json()
        if resp["code"] != 0:
            print(resp["msg"])
            cprint("please check ads_id", "red")
            sys.exit()
        chrome_driver = resp["data"]["webdriver"]
        service = Service(chrome_driver)

        chrome_options = Options()
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--disable-site-isolation-trials")
        chrome_options.add_argument("--disable-popup-blocking")
        #chrome_options.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])
        chrome_options.add_experimental_option("debuggerAddress", resp["data"]["ws"]["selenium"])
        # print(service.command_line_args())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get("https://www.google.com/?hl=ru")
        #time.sleep(5)
        #driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + Keys.F5)
        #driver.switch_to.window(driver.window_handles[-1])
        #input_element = driver.find_element(By.CSS_SELECTOR, 'input[name="q"]')
        # Ввод текста в строку поиска браузера
        #input_element.send_keys('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')
        # Нажатие клавиши Enter для выполнения поиска
        #input_element.send_keys(Keys.ENTER)


        driver.execute_script('window.open("chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html");')
        window_handles = driver.window_handles
        driver.switch_to.window(window_handles[1])
        driver.refresh()
        # driver.close()
        # window_handles = driver.window_handles
        # driver.switch_to.window(window_handles[0])
        # Ввод пароля от MM
        time.sleep(2)
        input_element = driver.find_element(By.ID, "password")
        if len(passwrds) == 1:
            input_element.send_keys(passwrds[0])
        else:
            input_element.send_keys(passwrds[id])
        input_element.send_keys(Keys.ENTER)

        driver.quit()
        colorama.deinit()
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





