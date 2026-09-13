import sys
import json
import time
import logging
from pathlib import Path
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

CONFIG = {
    "cookies_file":           "cookies.json",  # Cookies file from Cookie-Editor
    "message":                "STREAK!!!",     # Message to send
    "target_usernames":       ["USERNAME", "USERNAME"],  # List of TikTok usernames (without @)
    "headless":               False,           # False = visible browser | True = background (no window)
    "delay_between_messages": 10,              # Delay in seconds between each message
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("tiktok_dm.log", encoding="utf-8"),
        logging.StreamHandler(
            open(sys.stdout.fileno(), mode="w", encoding="utf-8", closefd=False)
        )
    ]
)
log = logging.getLogger(__name__)


class TikTokDMSender:

    def _init_driver(self):
        log.info("Starting browser...")
        options = Options()
        if CONFIG["headless"]:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--window-size=1280,900")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
        return driver

    def _load_cookies(self, driver) -> bool:
        cookies_path = Path(CONFIG["cookies_file"])
        if not cookies_path.exists():
            log.error("cookies.json not found! Export it first using Cookie-Editor.")
            return False

        log.info("Opening TikTok to inject cookies...")
        driver.get("https://www.tiktok.com")
        time.sleep(3)

        try:
            cookies  = json.loads(cookies_path.read_text(encoding="utf-8"))
            injected = 0
            for cookie in cookies:
                for key in ["sameSite", "storeId", "id", "hostOnly", "session", "firstPartyDomain"]:
                    cookie.pop(key, None)
                if "tiktok.com" not in cookie.get("domain", ""):
                    continue
                try:
                    driver.add_cookie(cookie)
                    injected += 1
                except Exception:
                    pass

            log.info(f"Injected {injected} cookies — refreshing...")
            driver.refresh()
            time.sleep(4)

            if "login" in driver.current_url.lower():
                log.error("Cookies expired or invalid — login failed.")
                return False

            log.info("Login via cookies successful!")
            return True

        except Exception as e:
            log.error(f"Failed to load cookies: {e}")
            return False

    def _send_dm(self, driver, username, message):
        wait = WebDriverWait(driver, 20)
        log.info(f"Opening profile @{username}...")

        try:
            driver.get(f"https://www.tiktok.com/@{username}")
            time.sleep(3)

            message_btn = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, 'button[data-e2e="message-button"]')
                )
            )
            message_btn.click()
            log.info(f"Message button clicked for @{username}...")
            time.sleep(3)

            msg_box = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'div.public-DraftEditor-content')
                )
            )
            msg_box.click()
            time.sleep(1)

            actions = ActionChains(driver)
            actions.move_to_element(msg_box).click().pause(0.5)
            for char in message:
                actions.send_keys(char)
                actions.pause(0.05)
            actions.perform()
            time.sleep(1)

            ActionChains(driver).move_to_element(msg_box).click().send_keys(Keys.RETURN).perform()
            time.sleep(2)

            log.info(f"Message sent successfully to @{username}")
            return True

        except Exception as e:
            log.error(f"Failed to send message to @{username}: {e}")
            driver.save_screenshot(f"error_{username}.png")
            return False

    def run(self):
        log.info("=" * 50)
        log.info(f"Starting session - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        log.info("=" * 50)

        driver = self._init_driver()
        try:
            if not self._load_cookies(driver):
                log.error("Cookie login failed. Make sure cookies.json exists and is valid.")
                return

            success = 0
            failed  = 0

            for username in CONFIG["target_usernames"]:
                result = self._send_dm(driver, username, CONFIG["message"])
                if result:
                    success += 1
                else:
                    failed += 1
                time.sleep(CONFIG["delay_between_messages"])

            log.info(f"Session completed — Successful: {success} | Failed: {failed}")

        finally:
            driver.quit()
            log.info("Browser closed.")


if __name__ == "__main__":
    sender = TikTokDMSender()
    sender.run()