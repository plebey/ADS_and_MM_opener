import time
import traceback
from termcolor import colored
from termcolor import cprint
import glob



path_to_ads_folder = 'C:\.ADSPOWER_GLOBAL'
ids_txt = "ADS_ids.txt"


def get_profile_cache_path(ads_id, path_from_ads_settings):
    folder_path = glob.glob(fr"{path_from_ads_settings}/cache/{ads_id}*")

    if folder_path:
        path_to_profile = folder_path[0].replace("\\", "/")
        path = fr'{path_to_profile}/extensionCenter/07de772c049203839ed54e4156de1a89/runtime-lavamoat.js'
    else:
        return 0
    return path


def line_control(file_txt):
    # Удаление пустых строк
    with open(file_txt) as f1:
        lines = f1.readlines()
        non_empty_lines = (line for line in lines if not line.isspace())
        with open(file_txt, "w") as n_f1:
            n_f1.writelines(non_empty_lines)


def runtime_lavamoat_cache_editor(path):

    with open(path, 'r', encoding="utf-8") as read:
        lines = read.readlines()

    key_edt = False
    # Изменяет переменную scuttleGlobalThis на значение false
    with open(path, 'w', encoding="utf-8") as read:
        for line in lines:
            if line.startswith('    } = {"scuttleGlobalThis":{"enabled":true,"scuttlerName":"SCUTTLER","exceptions":["toString","getComputedStyle","addEventListener","removeEventListener","ShadowRoot","HTMLElement","Element","pageXOffset","pageYOffset","visualViewport","Reflect","Set","Object","navigator","harden","console","Image","/cdc_[a-zA-Z0-9]+_[a-zA-Z]+/iu","performance","parseFloat","innerWidth","innerHeight","Symbol","Math","DOMRect","Number","Array","crypto","Function","Uint8Array","String","Promise","JSON","Date","__SENTRY__","appState","extra","stateHooks","sentryHooks","sentry"]}}'):
                line = '    } = {"scuttleGlobalThis":{"enabled":false,"scuttlerName":"SCUTTLER","exceptions":["toString","getComputedStyle","addEventListener","removeEventListener","ShadowRoot","HTMLElement","Element","pageXOffset","pageYOffset","visualViewport","Reflect","Set","Object","navigator","harden","console","Image","/cdc_[a-zA-Z0-9]+_[a-zA-Z]+/iu","performance","parseFloat","innerWidth","innerHeight","Symbol","Math","DOMRect","Number","Array","crypto","Function","Uint8Array","String","Promise","JSON","Date","__SENTRY__","appState","extra","stateHooks","sentryHooks","sentry"]}}'
                key_edt = True
            read.write(line)
    return key_edt


def lavamoat_editor():
    print(colored('Выполняется исправление файла lavamoat для metamask...', 'green'))
    line_control(ids_txt)
    with open(ids_txt, "r") as f:
        id_users = [row.strip() for row in f]

    i = 0
    for ads_id in id_users:
        i += 1
        try:
            path = get_profile_cache_path(ads_id, path_to_ads_folder)
            if path == 0:
                cprint(f'{i}. < {ads_id} >  cache not found or wrong id', 'yellow')
                continue
            key_edt = runtime_lavamoat_cache_editor(path)
            if key_edt is True:
                cprint(f'{i}. < {ads_id} >  fixed', 'green')
            elif key_edt is False:
                cprint(f'{i}. < {ads_id} >  already fixed', 'green')

        except FileNotFoundError:
            # traceback.print_exc()
            # time.sleep(.3)
            cprint(f'{i}. < {ads_id} >  runtime-lavamoat.js not found', 'red')

        except Exception as ex:
            traceback.print_exc()
            time.sleep(.3)
            cprint(f'{i}. < {ads_id} >  Unexpected error. Обратитесь к разработчику.', 'red')
