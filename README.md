# TP2022_questioner

Базой данных выбрана PostgreSQL, необходимые команды для работы проекта: 
```
CREATE USER appuser WITH PASSWORD '123';
ALTER ROLE appuser SET client_encoding TO 'utf8';
ALTER ROLE appuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE appuser SET timezone TO 'UTC';
CREATE DATABASE app;
GRANT ALL PRIVILEGES ON DATABASE app TO appuser;
```

### 1. Верстка статического сайта
Верстка общего вида (layout) страницы - 4:

- общий вид: 2 колонки, header, footer - 1;✅
- правая колонка - 1;✅
- блок авторизованного юзера - 1;✅
- поисковая строка и логотип - 1.✅

Верстка листинга вопросов - 3:
- общий вид (паддинги, аватарка) - 1;✅
- кнопки лайков - 1;✅
- теги, счетчики ответов, остальное - 1.✅

Верстка страницы вопроса - 3:
- общий вид - 1;✅
- чекбокс “правильный ответ”, кнопки лайков - 1;✅
- форма ответа - 1.✅

Верстка формы добавления вопроса - 3:
- общий вид - 2;✅
- сообщения об ошибках - 1.✅

Верстка форм логина и регистрации - 3:
- общий вид - 2;✅
- аватарка и сообщения об ошибках - 1.✅


### 2. Обработка HTTP запросов

Создать views и шаблоны для основных страниц - 6:

- главная (список новых вопросов) - 1;✅
- страница вопроса (список ответов) - 1;✅
- страница добавления вопроса - 1;✅
- форма регистрации - 1;✅
- форма входа - 1;✅
- форма добавления вопроса - 1.✅

Создать urls.py для всех страниц - 4:
- Собственно urls.py - 2;✅
- Именованные маршруты (во всех шаблонах) - 2.✅

Постраничное отображение - 4:

- функция пагинации - 1;✅
- шаблон для отрисовки пагинатора - 2;✅
- корректная обработка “неправильных” параметров - 1.✅


### 3. Проектирование модели данных
Проектирование модели - 5:

- правильные адекватные типы данных и внешние ключи - 1;✅
- своя модель пользователя - 1;✅
- таблицы тегов, лайков - 1;✅
- query-set'ы для типовых выборок: новые вопросы, популярные, по тегу - 2.✅

Наполнение базы тестовыми данными - 3:
- скрипт для наполнения данными - 1;✅
- использование django management commands - 1;✅
- соблюдение требований по объему данных - 1.

Отображение списка вопросов - 3:
- список новых вопросов - 1;✅
- список популярных - 1;✅
- список вопросов по тегу - 1.✅

Отображение страницы вопроса - 3:
- общее - 3.✅

Использование СУДБ - 2:
- MySQL или PostgreSQL - 2.✅