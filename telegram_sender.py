import os
import json
import requests
import logging
from dotenv import load_dotenv

# Настройка логирования
logging.basicConfig(filename="bot_log.txt", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Загрузка переменных из .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Проверка наличия переменных окружения
if not TOKEN or not CHAT_ID:
    logging.error("BOT_TOKEN или CHAT_ID не найдены в .env файле. Проверьте настройки.")
    raise ValueError("BOT_TOKEN или CHAT_ID не найдены в .env файле")

# Функция для отправки альбома фотографий через ссылки
def send_photos_as_album(image_urls, caption=None):
    """Отправляет альбом фотографий в Telegram, используя ссылки."""
    url_media = f"https://api.telegram.org/bot{TOKEN}/sendMediaGroup"
    media = [{"type": "photo", "media": url} for url in image_urls]

    if caption:
        media[0]["caption"] = caption
        media[0]["parse_mode"] = "Markdown"

    try:
        response = requests.post(url_media, data={"chat_id": CHAT_ID, "media": json.dumps(media)})
        response.raise_for_status()
        logging.info(f"Альбом успешно отправлен: {response.json()}")

    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при отправке альбома: {e}")

# Функция для создания описания лота
def create_description(car_title, secondary_data, tertiary_data, lot_price):
    """Создает текстовое описание лота для Telegram, с жирным выделением важных частей."""
    
    miles = int(secondary_data.get("Одометр", "0").replace(",", "").split()[0])
    kilometers = round(miles * 1.609)

    description = f"""🚗 **{car_title}**  
     
📌 **Характеристики:**  
📍 **Пробіг:** **{miles} миль ({kilometers} км)**  
🔧 **Двигун:** **{tertiary_data.get("Двигун", "N/A")}**  
⛽ **Паливо:** **{tertiary_data.get("Тип палива", "N/A")}**  
🔄 **Трансмісія:** **{tertiary_data.get("Трансмісія", "N/A")}**  
⚙ **Привід:** **{tertiary_data.get("Тип приводу", "N/A").replace("|", "").strip()}**  

💰 **Цена лота:** **{lot_price}**  

📞 **Контакты:**  
📍 **Київ, Лівий берег**  
📱 **Ігор:** **+38 066 923 74 34**  
📞 **Viber:** **@GS_USA_UA**  
🌐 **Facebook:** **[BloodyHarry86](https://www.facebook.com/BloodyHarry86)**  
🌐 **Facebook:** **[GSCkyiv](https://www.facebook.com/GSCkyiv)**  
🎥 **TikTok:** **[@gscarsusa](https://www.tiktok.com/@gscarsusa?is_from_webapp=1&sender_device=pc)**  
📸 **Instagram:** **[keep_garri](https://www.instagram.com/keep_garri/)**  
"""

    return description

def process_albums(car_title, image_urls, secondary_data, tertiary_data, lot_price):
    """Отправляет один альбом из 10 изображений в Telegram."""

    if not image_urls:
        logging.warning("Нет ссылок на изображения для отправки.")
        return

    # Берем только первые 10 фото
    image_urls = image_urls[:10]

    # Создаем описание с названием автомобиля
    text = create_description(car_title, secondary_data, tertiary_data, lot_price)

    # Отправляем единственный альбом
    send_photos_as_album(image_urls, caption=text)

    logging.info("Альбом успешно отправлен.")