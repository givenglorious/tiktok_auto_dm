"""
TikTok Auto DM - Selenium Automation
Kirim pesan otomatis ke beberapa username TikTok saat dijalankan
"""

import sys
import time
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager



CONFIG = {
    "email":                    "",
    "password":                 "",
    "message":                  "",
    "target_usernames":         [],
    "headless":                 False,
    "delay_between_messages":   10,
}


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("tiktok_dm.log", encoding="utf-8"),
        logging.StreamHandler(open(sys.stdout.fileno(), mode="w", encoding="utf-8", closefd=False))
    ]
)
log = logging.getLogger(__name__)


class TikTokDMSender:

    def _init_driver(self):
        log.info("Memulai browser Chrome...")
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

    def _login(self, driver):
        wait = WebDriverWait(driver, 30)
        log.info("Membuka halaman login TikTok...")
        driver.get("https://www.tiktok.com/login/phone-or-email/email")
        time.sleep(3)

        try:
            email_input = wait.until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            email_input.clear()
            email_input.send_keys(CONFIG["email"])
            time.sleep(1)

            pass_input = driver.find_element(By.XPATH, '//input[@type="password"]')
            pass_input.clear()
            pass_input.send_keys(CONFIG["password"])
            time.sleep(1)

            login_btn = driver.find_element(
                By.XPATH, '//button[@data-e2e="login-button"]'
            )
            login_btn.click()
            log.info("Menunggu login selesai...")
            time.sleep(5)

            if "captcha" in driver.current_url.lower():
                log.warning("CAPTCHA terdeteksi! Selesaikan manual dalam 60 detik...")
                time.sleep(60)

            log.info("Login berhasil!")
            return True

        except Exception as e:
            log.error(f"Gagal login: {e}")
            driver.save_screenshot("login_error.png")
            return False

    def _send_dm(self, driver, username, message):
        wait = WebDriverWait(driver, 20)
        log.info(f"Membuka profil @{username}...")

        try:
            driver.get(f"https://www.tiktok.com/@{username}")
            time.sleep(3)

            message_btn = wait.until(
                EC.element_to_be_clickable((By.XPATH,
                    '//button[contains(@data-e2e,"message") or '
                    'contains(translate(text(),"MESSAGE","message"),"message")]'
                ))
            )
            message_btn.click()
            log.info(f"Membuka DM ke @{username}...")
            time.sleep(3)

            msg_box = wait.until(
                EC.presence_of_element_located((By.XPATH,
                    '//div[@contenteditable="true"] | //textarea[@placeholder]'
                ))
            )
            msg_box.click()
            time.sleep(1)
            msg_box.send_keys(message)
            time.sleep(1)

            msg_box.send_keys(Keys.RETURN)
            time.sleep(2)

            log.info(f"Pesan berhasil dikirim ke @{username}")
            return True

        except Exception as e:
            log.error(f"Gagal kirim pesan ke @{username}: {e}")
            driver.save_screenshot(f"error_{username}.png")
            return False

    def run(self):
        log.info("=" * 50)
        log.info(f"Mulai sesi - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        log.info("=" * 50)

        driver = self._init_driver()
        try:
            if not self._login(driver):
                log.error("Login gagal, sesi dibatalkan.")
                return

            berhasil = 0
            gagal = 0

            for username in CONFIG["target_usernames"]:
                success = self._send_dm(driver, username, CONFIG["message"])
                if success:
                    berhasil += 1
                else:
                    gagal += 1
                time.sleep(CONFIG["delay_between_messages"])

            log.info(f"Selesai - Berhasil: {berhasil} | Gagal: {gagal}")

        finally:
            driver.quit()
            log.info("Browser ditutup.")


if __name__ == "__main__":
    sender = TikTokDMSender()
    sender.run()