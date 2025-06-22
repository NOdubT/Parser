import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def extract_data_section(driver, section_id, css_selector):
    """Извлекает данные из секции с указанным ID."""
    data = {}
    try:
        info_section = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, section_id)))
        options = info_section.find_elements(By.CSS_SELECTOR, css_selector)
        for option in options:
            label = option.text.strip().split("\n")[0]
            value_element = option.find_elements(By.CSS_SELECTOR, "span.right-info")
            value = value_element[0].text.strip() if value_element else "N/A"
            data[label] = value
    except Exception as e:
        print(f"Ошибка загрузки данных из секции '{section_id}': {e}")
    return data


def load_data():
    """Загружает название автомобиля, характеристики, цену и ссылки на изображения."""
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    chrome_driver_path = os.getenv("CHROME_DRIVER_PATH")
    if not chrome_driver_path:
        raise ValueError("CHROME_DRIVER_PATH не установлен в переменных окружения.")
    chrome_service = Service(chrome_driver_path)

    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    try:
        print("Ожидание полной загрузки страницы...")
        WebDriverWait(driver, 60).until(lambda d: d.execute_script("return document.readyState") == "complete")
        print("Страница загружена.")

        secondary_data = extract_data_section(driver, "secondary-info", "div.option")
        tertiary_data = extract_data_section(driver, "tertiary-info", "div.option")

        # Извлечение названия автомобиля
        try:
            title_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "title_lot")))
            car_title = title_element.text.strip()
        except Exception as e:
            car_title = "Название неизвестно"
            print(f"Ошибка загрузки названия автомобиля: {e}")

        # Извлечение цены
        try:
            lot_price_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "lot-price-large")))
            lot_price = lot_price_element.text.strip()
        except Exception as e:
            lot_price = "N/A"
            print(f"Ошибка загрузки цены: {e}")

        # Извлечение ссылок на изображения
        image_urls = []
        try:
            gallery = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "galleryThumbs")))
            image_elements = gallery.find_elements(By.CSS_SELECTOR, "div.f-carousel__thumb img")
            for img in image_elements:
                url = img.get_attribute("data-lazy-src") or img.get_attribute("src")
                if url:
                    image_urls.append(url)
        except Exception as e:
            print(f"Ошибка загрузки изображений: {e}")

        return car_title, secondary_data, tertiary_data, lot_price, image_urls

    finally:
        driver.quit()