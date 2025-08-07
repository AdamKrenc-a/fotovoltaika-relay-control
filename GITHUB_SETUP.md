# Nastavení GitHub Actions

## GitHub Secrets

Pro správné fungování GitHub Action je potřeba nastavit následující secrets v repository:

### 1. SHELLY_AUTH_KEY
- **Hodnota**: `MzQxOTU2dWlkE68406B9DA8511CF2F40693C563A099F43A2992A3FCF1C2D6E26CC980FDAD353C2A4A6F09E0D1705`
- **Popis**: Auth key pro Shelly Cloud API

### 2. SHELLY_DEVICE_ID
- **Hodnota**: `2cbcbba4373c`
- **Popis**: Device ID pro Shelly zařízení

## Jak nastavit Secrets

1. Jděte do vašeho GitHub repository
2. Klikněte na **Settings** tab
3. V levém menu klikněte na **Secrets and variables** → **Actions**
4. Klikněte na **New repository secret**
5. Přidejte oba secrets s hodnotami uvedenými výše

## Workflow Funkce

- **Automatické spouštění**: Každou hodinu v 5. minutě
- **Manuální spouštění**: Možné přes GitHub Actions tab
- **Environment**: Ubuntu latest s Python 3.10
- **Logy**: Dostupné v GitHub Actions tab

## Testování

Po nastavení secrets můžete:
1. Jít do **Actions** tab
2. Vybrat **Fotovoltaika Relay Control** workflow
3. Kliknout **Run workflow** pro manuální test 