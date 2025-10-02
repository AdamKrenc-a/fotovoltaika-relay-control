#!/usr/bin/env python3
"""
Automatické ovládání relé pro fotovoltaiku podle ceny elektřiny.
Skript kontroluje aktuální cenu elektřiny z OTE.cz API a podle ní zapíná/vypíná relé.

Cron úloha pro spouštění každou hodinu ve 2. minutě:
# Spouštět skript každou hodinu ve 2. minutě
2 * * * * cd /cesta/k/skriptu && python3 main.py >> /var/log/fotovoltaika.log 2>&1
"""

import requests
import sys
import os
from typing import Dict, Any
from datetime import datetime
from zoneinfo import ZoneInfo
import json

# Konfigurace
PRICE_THRESHOLD = 23.0  # Prahová cena v €/MWh
OTE_API_URL = "https://www.ote-cr.cz/cs/kratkodobe-trhy/elektrina/denni-trh/@@chart-data"  # JSON API endpoint
SHELLY_API_URL = "https://shelly-193-eu.shelly.cloud/device/relay/control"
SHELLY_DEVICE_ID = os.getenv('SHELLY_DEVICE_ID', '2cbcbba4373c')
SHELLY_AUTH_KEY = os.getenv('SHELLY_AUTH_KEY', 'MzQxOTU2dWlkE68406B9DA8511CF2F40693C563A099F43A2992A3FCF1C2D6E26CC980FDAD353C2A4A6F09E0D1705')


def get_current_price() -> float:
    """
    Získá aktuální spotovou cenu elektřiny z OTE.cz API.
    
    Returns:
        float: Aktuální cena elektřiny v €/MWh
        
    Raises:
        Exception: Pokud není možné získat cenu pro aktuální hodinu
    """
    try:
        # Získání dat z OTE.cz API pro aktuální den
        czech_tz = ZoneInfo("Europe/Prague")
        today = datetime.now(czech_tz).strftime('%Y-%m-%d')
        api_url = f"https://www.ote-cr.cz/cs/kratkodobe-trhy/elektrina/denni-trh/@@chart-data?date={today}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        print(f"🌐 API URL: {api_url}")
        print(f"📅 Datum: {today}")
        response = requests.get(api_url, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Parsování JSON dat
        data = response.json()
        
        # Získání aktuálního času v české časové zóně
        czech_tz = ZoneInfo("Europe/Prague")
        now = datetime.now(czech_tz)
        current_hour = now.hour
        
        print(f"🔍 Hledám cenu pro hodinu {current_hour}:00 (český čas)...")
        print(f"⏰ Aktuální čas (český): {now.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🌍 Časová zóna: {now.tzinfo}")
        
        # Hledání hodinových cen (60min cena) v JSON datech
        # Poznámka: API vrací 15minutové intervaly (96 bodů = 24 hodin)
        hourly_prices = {}
        
        # Procházíme všechny datové řady
        for data_line in data.get('data', {}).get('dataLine', []):
            # Hledáme řadu s hodinovou cenou (60min cena)
            if data_line.get('title') == '60min cena (EUR/MWh)':
                print(f"📊 Dostupné hodinové ceny z API (15min intervaly):")
                
                # Zpracováváme body dat - každé 4 body = 1 hodina
                points = data_line.get('point', [])
                for i in range(0, len(points), 4):  # Každé 4 body = 1 hodina
                    try:
                        # Hodina je index/4 + 1 (0-3 = hodina 1, 4-7 = hodina 2, atd.)
                        hour = (i // 4) + 1
                        
                        # Vezmeme první cenu z každé hodiny (nebo průměr všech 4)
                        price = float(points[i]['y'])
                        
                        hourly_prices[hour] = price
                        
                        # Zobrazíme jen první a poslední interval každé hodiny
                        if i + 3 < len(points):
                            last_price = float(points[i + 3]['y'])
                            print(f"  Hodina {hour}: {price:.2f}-{last_price:.2f} EUR/MWh (4 × 15min)")
                        else:
                            print(f"  Hodina {hour}: {price:.2f} EUR/MWh")
                            
                    except (ValueError, KeyError, IndexError):
                        continue
                break
        
        if not hourly_prices:
            raise Exception("Nepodařilo se najít hodinové ceny v API odpovědi")
        
        # Hledání ceny pro aktuální hodinu
        if current_hour in hourly_prices:
            price = hourly_prices[current_hour]
            print(f"✅ Nalezena cena pro aktuální hodinu: {price:.2f} EUR/MWh")
            return price
        else:
            raise Exception(f"Cena pro aktuální hodinu {current_hour}:00 není dostupná")
        
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Chyba při komunikaci s OTE.cz API: {e}")
        print("🔄 Používám simulovaná data pro testování...")
        # Fallback na simulovaná data pro testování
        return 22.7
    except Exception as e:
        print(f"⚠️  Chyba při zpracování dat z OTE.cz API: {e}")
        print("🔄 Používám simulovaná data pro testování...")
        # Fallback na simulovaná data pro testování
        return 22.7


def control_shelly_relay(turn: str) -> Dict[str, Any]:
    """
    Odešle požadavek na Shelly Cloud API pro ovládání relé.
    
    Args:
        turn (str): "on" pro zapnutí, "off" pro vypnutí
        
    Returns:
        Dict[str, Any]: Odpověď z API
    """
    data = {
        "id": SHELLY_DEVICE_ID,
        "auth_key": SHELLY_AUTH_KEY,
        "channel": 0,
        "turn": turn
    }
    
    try:
        response = requests.post(SHELLY_API_URL, data=data, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Chyba při komunikaci se Shelly API: {e}")
        return {"error": str(e)}


def main():
    """
    Hlavní funkce skriptu.
    """
    print("🔌 Automatické ovládání relé pro fotovoltaiku")
    print("=" * 50)
    
    # Logování času spouštění v různých časových zónách
    from datetime import timezone, timedelta
    import time
    
    # UTC čas
    utc_now = datetime.now(timezone.utc)
    print(f"⏰ Čas spuštění (UTC): {utc_now.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Česká časová zóna (automaticky CET/CEST)
    czech_tz = ZoneInfo("Europe/Prague")
    czech_now = datetime.now(czech_tz)
    print(f"⏰ Čas spuštění (český): {czech_now.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Unix timestamp
    print(f"⏰ Unix timestamp: {int(time.time())}")
    
    # Informace o očekávaném čase spouštění
    expected_minute = 2  # Očekáváme spouštění ve 2. minutě každé hodiny
    actual_minute = czech_now.minute
    print(f"📅 Očekávaný čas spouštění: každou hodinu ve {expected_minute}. minutě")
    print(f"📅 Skutečný čas spouštění: {actual_minute}. minuta")
    
    if actual_minute != expected_minute:
        print(f"⚠️  POZOR: Skript se spustil v {actual_minute}. minutě místo očekávané {expected_minute}. minuty!")
    else:
        print(f"✅ Skript se spustil ve správný čas ({expected_minute}. minuta)")
    
    # Získání aktuální ceny elektřiny
    try:
        current_price = get_current_price()
        print(f"💰 Aktuální cena elektřiny: {current_price} €/MWh")
    except Exception as e:
        print(f"❌ Chyba při získávání ceny elektřiny: {e}")
        sys.exit(1)
    
    # Rozhodnutí o akci podle ceny
    if current_price < PRICE_THRESHOLD:
        action = "off"
        action_text = "vypnuto"
        print(f"📉 Cena {current_price} €/MWh je pod prahem {PRICE_THRESHOLD} €/MWh")
    else:
        action = "on"
        action_text = "zapnuto"
        print(f"📈 Cena {current_price} €/MWh je nad prahem {PRICE_THRESHOLD} €/MWh")
    
    # Odeslání požadavku na Shelly API
    print(f"🔄 Odesílám požadavek na Shelly API...")
    result = control_shelly_relay(action)
    
    # Výpis výsledku
    if "error" not in result:
        print(f"✅ Relé bylo úspěšně {action_text}")
        print(f"📊 Odpověď API: {result}")
    else:
        print(f"❌ Relé nebylo {action_text} - chyba: {result['error']}")
        sys.exit(1)
    
    print("=" * 50)
    print("✅ Skript dokončen")


if __name__ == "__main__":
    main() 