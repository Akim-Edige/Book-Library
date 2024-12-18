# Система Управления Библиотекой

## Описание

Консольное приложение и Веб приложение для управления библиотекой книг. Позволяет добавлять, удалять, искать и отображать книги, а также изменять их статус. Для более разширенной веб версии читайте ниже

## Консольная версия

### Функционал

1. **Добавление книги**: Ввод названия, автора и года издания. Книга получает уникальный ID и статус "в наличии".
2. **Удаление книги**: Удаление книги по ее ID.
3. **Поиск книги**: Поиск по названию, автору, id или году издания.
4. **Отображение всех книг**: Вывод списка всех книг с их деталями.
5. **Изменение статуса книги**: Изменение статуса книги на "в наличии" или "выдана".

## Установка и Запуск

1. Убедитесь, что у вас установлен Python 3.6 или выше.
2. Скачайте или клонируйте репозиторий.
```bash
   git clone https://github.com/Akim-Edige/Book-Library.git
```
3. Перейдите в директорию проекта.
```bash
    cd Book-Library
    cd Console_Version
````
4. Запустите приложение командой:

```bash
   python start.py
```



# Web версия проекта

Это веб-версия проекта Book-Library, разработанная с использованием Django.

## Описание

Это приложение для управления библиотекой книг, разработанное на Django. Приложение позволяет добавлять, удалять, искать, изменять и отображать книги в библиотеке.



### Основные компоненты:

1. **Django** — фреймворк для веб-разработки.
2. **Модели** — для работы с базой данных.
3. **Контроллеры** — для обработки запросов и маршрутизации.
4. **Шаблоны** — для отображения данных пользователю.


## Структура проекта

Проект разделен на несколько приложений

```
Web_Version/      
│─── manage.py             # Утилита командной строки для выполнения административных задач  
│─── BookShelf/
```
BookShelf - это основное приложение в котором расписано основная логика приложения. Он содержит в себе контроллеры views.py. Контроллеры в Django обрабатывают запросы, взаимодействуют с моделями для извлечения данных, а затем возвращают ответы в виде отрендеренных HTML-страниц, JSON-ответов или других типов данных. Их роль заключается в управлении потоком данных между пользователем, представлением и моделью.
```
Bookshelf/  
│─── migrations/           # Папка для миграций базы данных  
│─── views.py              # Представления (логика обработки запросов)  
│─── models.py             # Определение моделей данных (таблиц базы данных)   
│─── serializers.py        # Для преобразования данных между JSON и моделями (если используется DRF)
│─── tests.py/             # Юнит тесты для проверки работы ендпоинтов 
│─── templates/            # HTML-шаблоны для этого приложения

```

## Демонстрация

https://drive.google.com/file/d/1mWiTtbWNuduC0Q23C_j6EwU3R7d7pNEk/view?usp=sharing


Чтобы зайти в админ панель изпользуйте это:
- Логин: library-admin
- Пароль: adminadmin

## Установка

1) Для запуска проекта нужно сделать предыдущие шаги по установке наверху:

- Перейдите в директорию проекта.
```bash
  cd ..
  cd Web_Version
````
2) Создайте виртуальную среду

```bash
  python3 -m venv venv
````

3) Активируйте виртуальную среду

```bash
  source venv/bin/activate
````
4) Установите зависимости

```bash
  pip install -r requirements.txt
````

5) Запустите сервер и откройте ссылку во вкладке браузера

```bash
  python3 manage.py runserver
````
