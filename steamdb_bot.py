import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

STEAMDB_URL = os.environ["STEAMDB_URL"]
DISCORD_WEBHOOK = os.environ["DISCORD_WEBHOOK"]
OUTPUT_FILE = "steamdb.png"


def capture_screenshot():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1400, 900)
    driver.get(STEAMDB_URL)

    # Sayfanın tam yüklenmesi için küçük bekleme
    driver.implicitly_wait(10)

    driver.save_screenshot(OUTPUT_FILE)
    driver.quit()


def send_to_discord():
    with open(OUTPUT_FILE, "rb") as f:
        r = requests.post(
            DISCORD_WEBHOOK,
            files={"file": ("steamdb.png", f, "image/png")}
        )
    r.raise_for_status()


if __name__ == "__main__":
    capture_screenshot()
    send_to_discord()
