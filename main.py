from data_loader import load_data
from telegram_sender import process_albums

if __name__ == "__main__":
    car_title, secondary_data, tertiary_data, lot_price, image_urls = load_data()
    process_albums(car_title, image_urls, secondary_data, tertiary_data, lot_price)