import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from discord import Webhook, RequestsWebhookAdapter

# --------- Ayarlar ----------
STEAMDB_URL = os.getenv("STEAMDB_URL")  # Örn: https://steamdb.info/calculator/76561199883458792/
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")  # Discord webhook URL
OUTPUT_FILE = "screenshot.png"
# ------------------------------

def capture_screenshot(url, output_file=OUTPUT_FILE):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1200, 800)
    driver.get(url)
    driver.save_screenshot(output_file)
    driver.quit()
    return output_file

def send_discord_image(image_path):
    webhook = Webhook.from_url(DISCORD_WEBHOOK, adapter=RequestsWebhookAdapter())
    with open(image_path, "rb") as f:
        webhook.send(file=f)

if __name__ == "__main__":
    screenshot = capture_screenshot(STEAMDB_URL)
    send_discord_image(screenshot)
