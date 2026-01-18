import os
import requests
from playwright.sync_api import sync_playwright

STEAM_PROFILE_URL = os.environ["STEAM_PROFILE_URL"]
DISCORD_WEBHOOK = os.environ["DISCORD_WEBHOOK"]
OUTPUT_FILE = "steam_profile.png"


def capture_screenshot():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1400, "height": 900})

        page.goto(STEAM_PROFILE_URL, wait_until="networkidle")
        page.wait_for_timeout(5000)  # İçerik tam yüklensin

        # Profilde biraz scroll yap (örneğin 1200px aşağı)
        page.mouse.wheel(0, 1200)
        page.wait_for_timeout(2000)

        page.screenshot(path=OUTPUT_FILE, full_page=True)
        browser.close()


def send_to_discord():
    with open(OUTPUT_FILE, "rb") as f:
        r = requests.post(
            DISCORD_WEBHOOK,
            files={"file": ("steam_profile.png", f, "image/png")},
        )
    r.raise_for_status()


if __name__ == "__main__":
    capture_screenshot()
    send_to_discord()
