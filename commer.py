# -*- coding: utf-8 -*-
#!/usr/bin/python3

# Created by AnonimFA https://github.com/AnonimFA
# Version 1.0.0
# Realese date 09.06.2019
#  ____  ____   _____   _____   ___________
# _/ ___\/  _ \ /     \ /     \_/ __ \_  __ \
# \  \__(  <_> )  Y Y  \  Y Y  \  ___/|  | \/
# \___  >____/|__|_|  /__|_|  /\___  >__|
#     \/            \/      \/     \/
# Если вы хотите модифицировать и куда-то выкладывать этот скрипт, пожалуйста, согласуйте с автором.

from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api
import time
from random import randint
import os
import requests
import json

R = '\033[31m'
G = '\033[32m'
Y = '\033[33;1m'
B = '\033[34;1m'
W = '\033[37m'
LG = '\033[32;1m'

def check():
    try:
        requests.get("https://google.com/", timeout = 3)
    except requests.ConnectionError:
        print(R + "\n[ 〤 ] Ошибка! Возникла проблема с интернет соединением!" + W)
        print(Y + "\n[ * ] Выходим..." + W)
        exit()

def main_print():
    os.system("clear")
    print(LG + r'''
+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+
  ____  ____   _____   _____   ___________
_/ ___\/  _ \ /     \ /     \_/ __ \_  __ \
\  \__(  <_> )  Y Y  \  Y Y  \  ___/|  | \/
 \___  >____/|__|_|  /__|_|  /\___  >__|
     \/            \/      \/     \/
+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+''' + W)
    print("[Version] = 1.0.0")
    print("[Created By] = AnonimFA")
    print("[GitHub] = https://github.com/AnonimFA")

main_print()
check()

try:
    if not os.path.exists("configuration.txt"):
        print(Y + "\n[ ! ] Файл конфигурации не найден!\n" + W)

        while True:
            token = str(input("[ * ] Введите свой токен: "))
            session = vk_api.VkApi(token=token)
            api = session.get_api()
            try:
                api.account.getProfileInfo()
            except vk_api.exceptions.ApiError as vk_error:
                print(R + "\n[ 〤 ] Ошибка! " + str(vk_error) + W)
                continue
            else:
                print(LG + "\n[ + ] Верификация токена прошла успешно!\n" + W)
                token_dict = {'token' : token}

                with open("configuration.txt", 'w') as f:
                    json.dump(token_dict, f)
                    f.close()
                break

    else:
        print(W + "\n[ * ] Инициализация файла конфигурации...")

        with open("configuration.txt", "r") as f:
            token_dict = json.load(f)
        session = vk_api.VkApi(token=token_dict["token"])
        api = session.get_api()

        try:
            api.account.getProfileInfo()
        except vk_api.exceptions.ApiError as vk_error:
            print(R + "\n[ 〤 ] Ошибка! " + str(vk_error) + W)
            print("\n[ * ] Удаление повреждённого файла конфигурации...")
            os.system("rm configuration.txt")
            print(Y + "\n[ * ] Выходим..." + W)
            exit()
        else:
            print(LG + "\n[ + ] Верификация токена прошла успешно!\n" + W)
    while True:
        try:
            group = int(input("[ > ] Укажите ID сообщества/страницы (-123456789/123456789): "))
            offs = int(input("[ > ] Укажите смещение (если в сообществе нет закрепов, пишите 0): "))
            mes = str(input("[ > ] Укажите текст комментария для следующего поста: "))
            delay = float(input("[ > ] Укажите временной промежуток между запросами (рекомендуется 3): "))
        except ValueError:
            print(R + "\n[ 〤 ] Ошибка! Неправильный ввод!\n" + W)
            continue
        else:
            break

    check()

    try:
        post_full = api.wall.get(owner_id=group, offset=offs, count=1)
    except vk_api.exceptions.ApiError as vk_error:
        print(R + "\n[ 〤 ] Ошибка! " + str(vk_error) + W)

    post = post_full["items"]
    post = post[0]
    post = post["id"]
    print(B + "\n[ * ] Сейчас в группе " + str(group) + " актуальный пост с ID " + str(post))
    print("[ * ] [ " + time.strftime("%H:%M:%S", time.localtime()) + " ] Ожидание нового поста!" + W)

    get = 1

    while True:
        check()
        time.sleep(delay)
        get += 1

        try:
            post_full_a = api.wall.get(owner_id=group, offset=offs, count=1)
        except vk_api.exceptions.ApiError as vk_error:
            print(R + "\n[ 〤 ] Ошибка! " + str(vk_error) + W)

        post_a = post_full_a["items"]
        post_a = post_a[0]
        post_a = post_a["id"]

        if post != post_a:
            print(Y + "\n[ ! ] [ " + time.strftime("%H:%M:%S", time.localtime()) + " ] Обнаружен новый пост! ID " + str(post_a) + W)
            print("[ * ] Во время ожидания нового поста было произведено " + str(get) + "/5000 запросов.")
            print("[ * ] Попытка создать комментарий под постом id " + str(post_a))

            check()

            try:
                api.wall.createComment(owner_id=group, post_id=post_a, message=mes)
            except vk_api.exceptions.ApiError as vk_error:
                print(R + "\n[ 〤 ] Ошибка! " + str(vk_error) + W)
            else:
                print("\n")
                while True:
                    print(LG + "[ + ] Комментарий под постом ID " + str(post_a) + " успешно опубликован!", end="\r", sep="")
                    time.sleep(1)
                    print("                                                               ", end="\r", sep="")
                    time.sleep(1)

except KeyboardInterrupt:
    print(Y + "\n[ * ] Выходим..." + W)

# Created by AnonimFA https://github.com/AnonimFA
# Version 1.0.0
# Realese date 09.06.2019
# Если вы хотите модифицировать и куда-то выкладывать этот скрипт, пожалуйста, согласуйте с автором.
