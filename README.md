# Загрузчик комиксов в VK сообщество 

Приложение скачивает комикс с [xkcd](https://xkcd.com) и загружает его в VK сообщество

## Как установить

Клонируйте проект и установите зависимости командами ниже.

```
git clone https://github.com/xegrassa/dvm_API_6.git
cd dvm_API_6
pip install -r requirements.txt
```

## Получение необходимых Токенов

- Для работы приложения нужно создать свое приложение в [dev.vk](https://dev.vk.com) 
  - `Тип приложения указать standalone — это приложения, которые запускаются на компьютере.`
- Получить Токен доступа для приложения **VK_ACCESS_TOKEN** [Инструкция](https://vk.com/dev.php?method=implicit_flow_user)
- **VK_CLUB_ID** сообщества можно получить из адресной строки  `ex: https://vk.com/club216985772`

# Настройка окружения

Для работы в корне проекта создайте файл **.env** с перечисленными ниже полями
```
VK_ACCESS_TOKEN=vk1.a.kyn6dQoZ2qTACLfd5eAGRhlP478gwg1vHrBOTiJJqlhy...
VK_CLUB_ID=216985772
```

## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).

## Запуск

Находясь в корне проекта запустите проект командой
```
python main.py
```

## Результат работы:
- В вашем сообществе появится пост с комиксом !

## Зависимости

* [Python 3.10](https://www.python.org/)
* [Requests](https://pypi.org/project/requests/)
* [python-dotenv](https://pypi.org/project/python-dotenv/)