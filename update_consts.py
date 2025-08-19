# update_consts.py
import requests
import re
import pathlib
import importlib
import logging as log

URL = "https://store.ubisoft.com/on/demandware.store/Sites-us_ubisoft-Site/en-US/UPlayConnect-GetAPISettingsJson"

def _consts_path() -> pathlib.Path:
    # Resolve consts.py location regardless of CWD
    m = importlib.import_module("consts")
    return pathlib.Path(m.__file__).resolve()

def fetch_settings():
    resp = requests.get(URL, timeout=5)
    resp.raise_for_status()
    return resp.json()

def update_consts_file(appid: str, genomeid: str):
    const_file = _consts_path()
    text = const_file.read_text(encoding="utf-8")

    text = re.sub(r'CLUB_APPID\s*=\s*".*?"',    f'CLUB_APPID = "{appid}"',   text)
    text = re.sub(r'CLUB_GENOME_ID\s*=\s*".*?"', f'CLUB_GENOME_ID = "{genomeid}"', text)

    const_file.write_text(text, encoding="utf-8")
    log.info(f"Updated {const_file} with app-id={appid}, genome-id={genomeid}")

def run_update_blocking():
    try:
        data = fetch_settings()
        appid = data.get("app-id")
        genomeid = data.get("genome-id")
        if not (appid and genomeid):
            log.warning("Ubisoft settings missing app-id/genome-id; skipping update.")
            return
        update_consts_file(appid, genomeid)
    except Exception as e:
        # Never crash plugin
        log.warning(f"update_consts.py failed: {e}")
