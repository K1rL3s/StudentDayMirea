# День студента 2025 в РТУ МИРЭА

## Запуск

1. Склонировать репозиторий и перейти в него:
    ```
    git clone https://github.com/K1rL3s/StudentDayMirea
    cd ./StudentDayMirea
    ```

2. Создать и заполнить файл `.env` в корневой папке (пример: `.env.example`)
    ```
    BOT_TOKEN=token
    OWNER_ID=[123456789,987654321]
    DB_URL=postgresql+psycopg://user:password@address:port/name
    DB_NAME=name
    DB_USER=user
    DB_PASSWORD=password
    ```

3. Иметь установленный [Docker Engine](https://docs.docker.com/engine/) и [docker compose v2](https://docs.docker.com/compose/releases/migrate/)

4. Собрать и запустить:
    ```
    docker compose up -d --build
    ```

## Команды

`/start` `/menu` `/me` - Старт

`/help` - Описание бота

`/id` - Куркод с диплинком на юзера

`/shop` - Товары на продаже

`/cart` - Купленные товары

`/quest` - Квестовая линия

`/task` - Активное задание

`/transfer` - Перевод денег между юзерами

`/secret <phrase>` - Ввод секрета

`/coupon <phrase>` - Ввод купона

`/admin` - Админ панель

`/money <user_id> <amount>` - Прибавить amount Пятаков юзеру user_id


## Дизайн

### [Инструкция пользователя](./content/instruction.pdf)

![tg-bot.png](./content/tg-bot.png)
![tg-start.png](./content/tg-start.png)
![profile-picture.jpg](./content/profile-picture.jpg)
![start-picture.jpg](./content/start-picture.jpg)


