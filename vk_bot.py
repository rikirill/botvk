https://github.com/rikirill/botvk
token = ''
vk = vk_api.VkApi(token=token)

longpoll = VkLongPoll(vk)


def write_msg(user_id, message):
    vk.method('messages.send',
              {'user_id': user_id, 'message': message, 'random_id': random.randint(0, 922337203685477580)})


def send_stiker(user_id):
    stikers = (17161.489, 12507.367, 16293.464, 14280.415,
               12696.372, 11608.346, 11609.346, 11255.338, 9992.306, 7147.219)
    vk.method('messages.send',
              {'user_id': user_id, 'sticker_id': random.choice(stikers),
               'random_id': random.randint(0, 922337203685477580)})


zodiaks = {
    ('22', '01', '18', '02'): 'https://www.astrostar.ru/horoscopes/main/vodoley/week.html',
    ('19', '02', '20', '03'): 'https://www.astrostar.ru/horoscopes/main/riby/week.html',
    ('21', '03', '20', '04'): 'https://www.astrostar.ru/horoscopes/main/oven/week.html',
    ('21', '04', '20', '05'): 'https://www.astrostar.ru/horoscopes/main/telets/week.html',
    ('21', '05', '20', '06'): 'https://www.astrostar.ru/horoscopes/main/bliznetsi/week.html',
    ('21', '06', '22', '07'): 'https://www.astrostar.ru/horoscopes/main/rac/week.html',
    ('23', '07', '22', '08'): 'https://www.astrostar.ru/horoscopes/main/lev/week.html',
    ('23', '08', '23', '09'): 'https://www.astrostar.ru/horoscopes/main/deva/week.html',
    ('24', '09', '23', '10'): 'https://www.astrostar.ru/horoscopes/main/vesy/week.html',
    ('24', '10', '21', '11'): 'https://www.astrostar.ru/horoscopes/main/scorpion/week.html',
    ('22', '11', '21', '12'): 'https://www.astrostar.ru/horoscopes/main/strelets/week.html',
    ('22', '12', '19', '01'): 'https://www.astrostar.ru/horoscopes/main/kozerog/week.html',

}


def red(text, key):
    wrong_word = wrong_words[key]
    text = text.replace('Звёзды', ' ')
    for word in wrong_words:
        text = text.replace(word, ' ')
    return text


def zodiakus(date ='25.01.2001'):
    month = int(date.split('.')[1])
    day = int(date.split('.')[0])
    for dates in zodiaks.keys():
        if month == int(dates[1]):
            if day >= int(dates[0]):
                return zodiaks[dates]
        elif month == int(dates[3]):
            if day <= int(dates[2]):
                return zodiaks[dates]


def future(zodiak):
    future = req.get(zodiak)
    soup = beatsup(future.text, 'html.parser')
    future_text = soup.find('div', {'class': 'col-xs-12 col-sm-9 col-md-7 horoscopes-single-content'}).find('p').text
    return red(future_text, zodiak)


def bot_body():
    for event in longpoll.listen():

        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            request = event.text
            try:
                date = request.split('.')
                print(date)
                chislo = int(date[1])
            except:
                chislo = 'no'
            print(request)
            if request == "привет" or request == 'Привет':
                write_msg(event.user_id,
                          "привет, ты хочешь узнать своё будущее? Скажи свою дату рождения (дд.мм.гг), и я открою его тебе.")
                print(event.user_id)
            elif request == "пока" or request == 'Пока':
                print(event.user_id)
                write_msg(event.user_id, "Пока")
            elif request == "самосвал" or request == "Самосвал":
                print(event.user_id)
                send_stiker(event.user_id)
            elif isinstance(chislo, int):
                prediction = future(zodiakus(request))
                write_msg(event.user_id, prediction)
            else:
                print(event.user_id)
                print(type(request))
                write_msg(event.user_id, "Не понял вашего ответа, попытайтесь ещё раз.")
bot_body()
