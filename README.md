# Automatické ovládání relé pro fotovoltaiku

Skript pro automatické ovládání relé podle aktuální ceny elektřiny z OTE.cz API.

## Funkce

- Získává aktuální cenu elektřiny z OTE.cz API
- Pokud je cena < 23 €/MWh → vypne relé
- Pokud je cena ≥ 23 €/MWh → zapne relé
- Komunikuje se Shelly Cloud API
- Fallback na simulovaná data při chybě API

## Instalace

1. Nainstalujte závislosti:
```bash
pip install -r requirements.txt
```

## Použití

Spusťte skript:
```bash
python3 main.py
```

## Automatické spouštění

Pro automatické spouštění každou hodinu použijte cron:

```bash
# Otevřete crontab editor
crontab -e

# Přidejte řádek pro spouštění každou hodinu
0 * * * * cd /cesta/k/skriptu && python3 main.py >> /var/log/fotovoltaika.log 2>&1
```

## Konfigurace

Skript je nakonfigurován pro:
- **Prahová cena**: `23.0 €/MWh`
- **OTE.cz API**: `https://www.ote-cr.cz/cs/kratkodobe-trhy/elektrina/denni-trh/@@chart-data`
- **Shelly Cloud API**: `https://shelly-193-eu.shelly.cloud/device/relay/control`
- **Device ID**: `2cbcbba4373c`
- **Auth key**: `MzQxOTU2dWlkE68406B9DA8511CF2F40693C563A099F43A2992A3FCF1C2D6E26CC980FDAD353C2A4A6F09E0D1705`
- **Channel**: `0`

## Poznámky

- Skript automaticky hledá cenu pro aktuální hodinu v datech OTE.cz
- Ceny jsou získávány v centech a automaticky převáděny na EUR
- Při chybě OTE.cz API se použijí simulovaná data (22.7 €/MWh) pro testování
- Logy se zapisují do konzole s časovými razítky
- Skript je připraven pro produkční nasazení s cron úlohou 