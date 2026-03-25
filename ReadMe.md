# Ursa Team Test

Генератор статического сайта с киберспортивными матчами на основе API Pandascore.

---

## 📌 Описание

Проект получает список матчей с Pandascore, обрабатывает их и генерирует **одну HTML-страницу** с интерактивным переключением:

- Матчи за вчера
- Матчи за сегодня
- Матчи за завтра

Переключение осуществляется с помощью кнопок без перезагрузки страницы.

---

## ⚙️ Функциональность

- Получение данных через API Pandascore
- Группировка матчей по дням (yesterday / today / tomorrow)
- Генерация HTML через Jinja2
- Переключение данных на странице (JS tabs)
- SEO-оптимизация:
  - `title`, `description`, `keywords`
  - Open Graph мета-теги
- Микроразметка Schema.org (Organization + Event)
- Полностью статический сайт (без backend)

---

## 🚀 Демо

Сайт доступен по ссылке:

👉 https://lekantrop74.github.io/Ursa_Team_test/output/index.html

---

## 🛠 Установка

```bash
git clone https://github.com/Lekantrop74/Ursa_Team_test.git
cd Ursa_Team_test
```

Создать виртуальное окружение:

```bash
python -m venv venv
```

Активировать:

Linux/macOS:
```bash
source venv/bin/activate
```

Windows:
```bash
venv\Scripts\activate
```

Установить зависимости:

```bash
pip install requests jinja2
```

---

## ▶️ Использование

1. Указать API-ключ в `main.py`:

```python
API_KEY = "ваш_API_KEY"
```

2. Запустить скрипт:

```bash
python main.py
```

3. Результат:

- Генерируется файл:
  ```
  output/index.html
  ```
- Это готовая страница сайта

---

## 📁 Структура проекта

```
Ursa_Team_test/
├─ main.py
├─ templates/
│  └─ page.html
├─ output/
│  └─ index.html
└─ README.md
```

---

## 💡 Особенности

- Не используется сервер — сайт полностью статический
- Подходит для деплоя на GitHub Pages
- Данные обновляются при каждом запуске скрипта

---

## 📦 Технологии

- Python
- requests
- Jinja2
- HTML / CSS / JavaScript

---

## 📄 API

Используется API Pandascore:

https://www.pandascore.co/

---

## 👤 Автор

Виктор Королёв