# parserAvito_beta
Beta version program pulling info from avito website + Telegram Bot parser

Парсинг в данный момент выполняется только по перваой странице. <br>
В результате создается файл-таблица xlsx со следующими полями: 

![image](https://user-images.githubusercontent.com/63307876/161378358-6310137b-977a-45f5-a07d-80e7fc8e20a5.png)

, а также создается dataframe с которым уже можно полноценно работать (выполнять различные аналитические сценарии).

Пример: на данном графике видно в каком ценовом диапазоне продается видеокарта "gtx 1080 ti" на 04.2022 года
(Большинство продают по цене от 60 до 72 т.р)
![image](https://user-images.githubusercontent.com/63307876/161378440-5018e715-a700-4af6-81f8-73c26a150ed1.png)

p.s. опять же стоит брать во внимание тот факт, что парсинг выполнен только по первой странице!

Добавлен функционал парсинга через Telegram бота (функционал пока остался такой же):<br>
В боте имеется довольно простой функционал:
![image](https://user-images.githubusercontent.com/63307876/161594512-c864711a-f338-4beb-a1b0-54ace4d5c399.png)

Команды:<br>
<li>/start - Главное меню </li>
<li>/parse - Команда на выполнение парсинга</li>
<li>/help - Команда вызова помощи</li>
![image](https://user-images.githubusercontent.com/63307876/161594885-6ccdb961-daa6-41d6-9643-835cfdfcba29.png)

Результат выполнения в телеграмме выглядит следующим образом:
![image](https://user-images.githubusercontent.com/63307876/161594319-5d414c0f-a2b1-4d27-bb91-9e79bfa9c602.png)
