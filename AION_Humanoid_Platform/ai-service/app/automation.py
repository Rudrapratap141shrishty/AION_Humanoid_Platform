import os
import socket
import webbrowser
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def _allowed_hosts():
    raw = os.getenv("AUTOMATION_ALLOWED_HOSTS", "example.com,localhost")
    return {host.strip().lower() for host in raw.split(",") if host.strip()}

def validate_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("URL must start with http:// or https:// and include a hostname.")
    host = parsed.hostname.lower()
    if host not in _allowed_hosts():
        raise ValueError(f"Host '{host}' is not allowlisted. Configure AUTOMATION_ALLOWED_HOSTS.")
    # Prevent obvious local-network access except explicitly allowlisted localhost.
    if host != "localhost":
        try:
            ip = socket.gethostbyname(host)
            if ip.startswith(("127.", "10.", "192.168.", "169.254.")) or ip.startswith("172."):
                raise ValueError("Private or loopback network destinations are blocked.")
        except socket.gaierror:
            raise ValueError("Hostname could not be resolved.")
    return url

def open_allowed_url(url: str, open_browser: bool = False):
    safe_url = validate_url(url)
    if open_browser:
        webbrowser.open(safe_url)
    return {"url": safe_url, "opened": bool(open_browser), "message": "URL passed allowlist validation."}

def selenium_title(url: str) -> str:
    safe_url = validate_url(url)
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280,900")
    driver = webdriver.Chrome(options=options)
    try:
        driver.set_page_load_timeout(12)
        driver.get(safe_url)
        return driver.title
    finally:
        driver.quit()
