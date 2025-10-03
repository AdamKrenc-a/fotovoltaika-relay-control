# Alternativní řešení pro časování (zdarma)

## 1. Uptime Robot (doporučeno)
- **Zdarma**: 50 monitorů
- **Frekvence**: Každých 5 minut
- **Webhook**: Může volat váš skript přes HTTP
- **Výhody**: Spolehlivé, přesné časování, notifikace

### Nastavení:
1. Zaregistrujte se na uptimerobot.com
2. Vytvořte "HTTP(s)" monitor
3. URL: `https://your-domain.com/webhook/fotovoltaika`
4. Interval: 5 minut
5. Webhook URL: Váš server s endpointem

## 2. Cron-job.org
- **Zdarma**: 3 úlohy
- **Frekvence**: Každých 5 minut
- **HTTP požadavky**: Může volat váš skript
- **Výhody**: Jednoduché, spolehlivé

## 3. GitHub Actions s lepším časováním
- **Zdarma**: 2000 minut/měsíc
- **Výhody**: Integrované s kódem
- **Nevýhody**: Může mít zpoždění

### Vylepšený cron:
```yaml
# Spouštět každých 5 minut pro lepší přesnost
- cron: '*/5 * * * *'
```

## 4. Vlastní server s cron
- **Zdarma**: Pokud máte vlastní server
- **Výhody**: Plná kontrola
- **Nevýhody**: Potřebujete server

## 5. Railway/Render (zdarma tier)
- **Zdarma**: 500 hodin/měsíc
- **Cron**: Vlastní cron job
- **Výhody**: Spolehlivé, jednoduché

## Doporučení:
1. **Nejlepší**: Uptime Robot + vlastní server
2. **Nejjednodušší**: Vylepšený GitHub Actions
3. **Nejspolehlivější**: Vlastní server s cron
