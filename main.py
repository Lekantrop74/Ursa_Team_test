import requests
from datetime import datetime, timedelta, timezone
from jinja2 import Environment, FileSystemLoader
import os
import json

API_KEY = "JwqkBRVniS_eEONTSZwUW6J6_BYKYho0QN_HNl1qTx6_zJ3dpMA"

env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("page.html")


def get_date_range():
    """Возвращает даты: вчера, сегодня, завтра."""
    today = datetime.now(timezone.utc).date()
    return today - timedelta(1), today, today + timedelta(1)


def get_matches():
    """Запрашивает матчи из API Pandascore за диапазон (вчера–завтра)."""
    yesterday, today, tomorrow = get_date_range()

    url = "https://api.pandascore.co/matches"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    params = {
        "range[begin_at]": f"{yesterday.isoformat()},{tomorrow.isoformat()}"
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Ошибка при запросе API: {e}")
        return []


def format_match(match):
    """Преобразует матч в удобный для отображения формат."""
    begin = match.get("begin_at")
    if not begin:
        return None

    dt = datetime.fromisoformat(begin.replace("Z", "+00:00"))

    # Название матча
    if match.get("opponents") and len(match["opponents"]) >= 2:
        name = f"{match['opponents'][0]['opponent']['name']} vs {match['opponents'][1]['opponent']['name']}"
    else:
        name = match.get("name", "Unknown match")

    return {
        "name_display": name,
        "begin_at": begin,
        "begin_at_display": dt.strftime("%d.%m.%Y %H:%M"),
        "date": dt.date()
    }


def prepare_matches(matches):
    """Группирует матчи по дням: вчера, сегодня, завтра."""
    yesterday, today, tomorrow = get_date_range()

    grouped = {"yesterday": [], "today": [], "tomorrow": []}

    for raw_match in sorted(matches, key=lambda x: x.get("begin_at") or ""):
        match = format_match(raw_match)
        if not match:
            continue

        if match["date"] == yesterday:
            grouped["yesterday"].append(match)
        elif match["date"] == today:
            grouped["today"].append(match)
        elif match["date"] == tomorrow:
            grouped["tomorrow"].append(match)

    return grouped


def generate_schema(matches):
    """Генерирует JSON-LD микроразметку Schema.org."""
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "Esports Matches",
        "url": "https://your-site.example.com",
        "hasEvent": [
            {
                "@type": "Event",
                "name": m["name_display"],
                "startDate": m["begin_at"],
                "eventStatus": "https://schema.org/EventScheduled",
                "eventAttendanceMode": "https://schema.org/OnlineEventAttendanceMode",
            }
            for m in matches
        ]
    })


def generate_page(grouped):
    """Генерирует HTML страницу с матчами."""
    os.makedirs("output", exist_ok=True)

    all_matches = (
        grouped["yesterday"] +
        grouped["today"] +
        grouped["tomorrow"]
    )

    html = template.render(
        title="Киберспортивные матчи",
        description="Матчи вчера, сегодня и завтра",
        grouped=grouped,
        schema=generate_schema(all_matches)
    )

    with open("output/index.html", "w", encoding="utf-8") as f:
        f.write(html)


def main():
    """Точка входа: получает данные и генерирует страницу."""
    matches = get_matches()
    grouped = prepare_matches(matches)
    generate_page(grouped)


if __name__ == "__main__":
    main()