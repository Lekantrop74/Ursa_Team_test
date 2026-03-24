import requests
from datetime import datetime, timedelta, timezone
from jinja2 import Environment, FileSystemLoader
import os, json

API_KEY = "JwqkBRVniS_eEONTSZwUW6J6_BYKYho0QN_HNl1qTx6_zJ3dpMA"

# ------------------- Шаблон Jinja2 -------------------
env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("page.html")


# ------------------- Получение матчей -------------------
def get_matches():
    """Получает список киберспортивных матчей через API Pandascore."""
    url = "https://api.pandascore.co/matches"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    params = {"range[begin_at]": "2026-03-23,2026-03-25"}
    return requests.get(url, headers=headers, params=params).json()


# ------------------- Подготовка матчей -------------------
def prepare_matches(matches):
    """
    Преобразует даты, формирует имя для отображения, сортирует и разделяет по дням.
    Возвращает словарь с ключами: 'yesterday', 'today', 'tomorrow'.
    """
    today = datetime.now(timezone.utc).date()
    yesterday, tomorrow = today - timedelta(1), today + timedelta(1)
    result = {"yesterday": [], "today": [], "tomorrow": []}

    # Сортируем матчи по времени начала
    for m in sorted(matches, key=lambda x: x.get("begin_at", "")):
        if not (begin := m.get("begin_at")):
            continue

        # Преобразуем дату ISO в datetime и в красивый формат
        dt = datetime.fromisoformat(begin.replace("Z", "+00:00"))
        m["_dt"] = dt
        m["begin_at_display"] = dt.strftime("%d.%m.%Y %H:%M")

        # Формируем отображаемое имя матча
        if m.get("opponents") and len(m["opponents"]) >= 2:
            m["name_display"] = f"{m['opponents'][0]['opponent']['name']} vs {m['opponents'][1]['opponent']['name']}"
        else:
            m["name_display"] = m.get("name", "Unknown match")

        # Разделяем по дням
        day_key = {yesterday: "yesterday", today: "today", tomorrow: "tomorrow"}.get(dt.date())
        if day_key:
            result[day_key].append(m)

    return result


# ------------------- Генерация Schema.org -------------------
def generate_schema(matches):
    """Создаёт микроразметку Schema.org для организации с матчами как события."""
    events = []
    for m in matches:
        events.append({
            "@type": "Event",
            "name": m["name_display"],
            "startDate": m["begin_at"],  # ISO
            "eventStatus": "https://schema.org/EventScheduled",
            "eventAttendanceMode": "https://schema.org/OnlineEventAttendanceMode",
        })
    schema = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "Esports Matches",
        "url": "https://your-site.example.com",
        "hasEvent": events
    }
    return json.dumps(schema)


# ------------------- Генерация HTML -------------------
def generate_page(name, matches):
    """Генерирует HTML-страницу с матчами и микроразметкой событий."""
    os.makedirs(f"output/{name}", exist_ok=True)
    html = template.render(
        title=f"Матчи {name}",
        description=f"Киберспортивные матчи {name}",
        matches=matches,
        schema=generate_schema(matches)
    )
    with open(f"output/{name}/index.html", "w", encoding="utf-8") as f:
        f.write(html)


# ------------------- Главная функция -------------------
def main():
    grouped = prepare_matches(get_matches())
    for key, matches in grouped.items():
        generate_page(key, matches)


if __name__ == "__main__":
    main()