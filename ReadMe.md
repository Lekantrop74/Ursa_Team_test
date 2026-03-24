# Ursa Team Test

Автоматическая генерация HTML-страниц с киберспортивными матчами с использованием API Pandascore.

---

## Описание

Проект получает список матчей с Pandascore, сортирует их по времени, разделяет по дням (`yesterday`, `today`,
`tomorrow`) и генерирует HTML-страницы с:

- SEO-полями (`title`, `description`, `keywords`)
- Open Graph мета-тегами
- Микроразметкой Schema.org для организации и событий (матчей)
- Дизайном на голом HTML/CSS

---

## Установка

1. Склонировать репозиторий:

git clone https://github.com/Lekantrop74/Ursa_Team_test.git
cd Ursa_Team_test

2. Установить зависимости (рекомендуется виртуальное окружение):

python -m venv venv

# Linux/macOS

source venv/bin/activate

# Windows

venv\Scripts\activate

pip install requests jinja2

3. Создать папку `templates` и положить туда шаблон `page.html` (либо использовать уже готовый шаблон из проекта).

---

## Использование

1. В файле `main.py` укажите свой API_KEY Pandascore:

API_KEY = "ваш_API_KEY"

2. Запустить скрипт:

python main.py

3. Результат:

- HTML-страницы будут созданы в папках `output/yesterday`, `output/today`, `output/tomorrow`
- Каждая страница будет содержать список матчей с форматированной датой и микроразметкой Schema.org

---

## Структура проекта

```
esports-matches/
├─ main.py             # Главный скрипт
├─ templates/
│  └─ page.html        # Шаблон HTML для генерации страниц
├─ output/             # Сгенерированные страницы
│  ├─ yesterday/
│  ├─ today/
│  └─ tomorrow/
└─ README.md
```

---