# Космический телеграм

Проект позволяет скачивать фотографии с сайтов:

- SpaceX (фото запуска ракет компании Илона Маска). Можно скачать серию фотографий по каждому запуску (задается номер запуска, 
если номер не задан, то берутся фотографии с последнего запуска в котором они есть)
файл `fetch_spacex_images.py`.
```py
fetch_spacex_launch(picture_path='images/spacex', flight_number=None)
```
- NASA. Можно скачать много красивых снимков космоса (задается количество необходимых фотографий)
файл `fetch_NASA_images.py`.
```py
fetch_space_pictures_from_nasa(pictures_quantity=30,
                        picture_path='images/nasa_apod', nasa_api_key=nasa_api_key)
```
- EPIC: Earth Polychromatic Imaging Camera. Можно скачать фотографии земли с космоса (задается количество необходимых фотографий)
файл `fetch_EPIC_images.py`.
```py
fetch_earth_pictures_from_nasa(pictures_quantity=10, picture_path='images/epic_nasa', nasa_api_key=nasa_api_key)
```

А затем передавать их в телеграмм по таймеру файл `publish_image_to_telegram.py`. 
Таймер настроен на передачу одной скаченной фотографии через каждые 4 часа.
Задается путь директории куда будут скачиваться фотографии, если папка пуста, то программа скачивает в нее с трех сайтов, 
указанных выше заданное количество фотографий, а потом программа берет случайные фотографии из директории и отправляет их в телеграм.
Когда фотографии закончаться закачка осуществляется по новой.
```py
send_picture(picture_directory='images', flight_number=None, nasa_api_key=nasa_api_key,
                 token=token, chat_id=chat_id, timer=timer)
```
Также можно запустить отдельную фотографию в телеграм канал указав `picture_user_path`

```py
send_picture(picture_directory='images', flight_number=None, nasa_api_key=nasa_api_key,
                 token=token, chat_id=chat_id, timer=5,
                 picture_user_path="C:/Документы Макс/Программирование/Devman/Уроки/5 неделя/герберы.jpg")
```

### Как установить

Python3 должен быть уже установлен. 
Затем используйте `pip` для установки зависимостей:
```
pip install -r requirements.txt
```
- Для скачивания фото с сайта NASA необходима генерация своего токена на сайте https://api.nasa.gov/.
- Создать в корневом катологе файл .env
- Записать в этом файле ваш токен.
- Для запуска телеграм нужно зарегистрировать бота в Telegram через Bot Father, получить токен
- Создать канал в Telegram и скопировать имя канала 

Все это положить в созданный текстовый файл .env

``` 
NASA_API_KEY=.....
TG_TOKEN=.......
TG_CHAT_ID=@.....
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
