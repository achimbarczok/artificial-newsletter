# 🔒 Privacy Newsletter Generator

Ein automatischer Newsletter-Generator, der täglich die wichtigsten Datenschutz-News sammelt, mit KI zusammenfasst und per E-Mail versendet.

> **🤖 Transparenz-Hinweis:** Dieses Projekt wurde größtenteils in Zusammenarbeit mit Claude (Anthropic) entwickelt. Der Code, die Struktur und viele Features entstanden durch intensive Kollaboration mit der KI.

## ✨ Features

- 🤖 **KI-gestützte Zusammenfassung** mit Claude (Anthropic)
- 📰 **Automatische News-Sammlung** von verschiedenen RSS-Quellen
- 🎯 **Intelligente Filterung** nach Datenschutz-Relevanz
- 📧 **Schön gestaltete HTML-E-Mails**
- ⏰ **Automatischer Versand** via Cron-Job
- 🔌 **Google Alerts Integration** möglich
- ⚙️ **Vollständig konfigurierbar**

## 🚀 Quick Start

### 1. Repository klonen
```bash
git clone https://github.com/achimbarczok/artificial-newsletter.git
cd artificial-newsletter
```

### 2. Virtual Environment einrichten
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# oder: venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 3. Konfiguration erstellen
```bash
cp config.example.py config.py
nano config.py  # Deine echten Daten eintragen
```

### 4. Testen
```bash
python newsletter_generator.py
```

## ⚙️ Konfiguration

Alle Einstellungen erfolgen in der `config.py` Datei:

### API Keys
- **Anthropic Claude API**: Für intelligente Zusammenfassungen
- **E-Mail Credentials**: Gmail App-Passwort empfohlen

### RSS-Quellen
Standardmäßig enthalten:
- Heise.de, Golem.de, Netzpolitik.org
- Datenschutz-Notizen.de, Dr-Datenschutz.de
- Heise Security, Telepolis

### Google Alerts
Optional können Google Alerts RSS-Feeds hinzugefügt werden:
1. Gehe zu https://www.google.de/alerts
2. Erstelle Alerts für gewünschte Begriffe
3. Wähle "RSS-Feed" statt E-Mail
4. Füge die RSS-URLs in `config.py` hinzu

## 🤖 Automatisierung

### Linux/Mac (Cron)
```bash
# Täglich 7:00 Uhr - anpassen an deinen Pfad!
crontab -e

# Beispiel-Einträge:
0 7 * * * /home/USERNAME/artificial-newsletter/run_newsletter.sh >> /home/USERNAME/artificial-newsletter/newsletter.log 2>&1

# Oder absoluter Pfad:
0 7 * * * /vollständiger/pfad/zum/artificial-newsletter/run_newsletter.sh
```

**Tipp:** Das `run_newsletter.sh` Script erkennt automatisch sein Verzeichnis, du musst nur den Pfad zum Script anpassen.

### Windows (Taskplaner)
Erstelle eine geplante Aufgabe, die `newsletter_generator.py` täglich ausführt.

## 📁 Projektstruktur

```
artificial-newsletter/
├── newsletter_generator.py    # Hauptskript
├── config.example.py         # Konfigurationsvorlage  
├── config.py                 # Deine Konfiguration (nicht im Git)
├── requirements.txt          # Python Dependencies
├── run_newsletter.sh         # Wrapper-Script für Cron
├── .gitignore               # Git-Ausschlüsse
└── README.md                # Diese Datei
```

## 🔧 Anpassungen

### Newsletter-Layout
Das HTML-Layout kann in der `create_fallback_newsletter()` Funktion angepasst werden.

### Artikel-Auswahl
Die Anzahl der Artikel und Auswahlkriterien sind in `config.py` konfigurierbar.

### Keywords
Datenschutz-Keywords für die Filterung können in `config.py` erweitert werden.

## 🛠️ Entwicklung

### Neue RSS-Quellen hinzufügen
Einfach in `config.py` im `RSS_FEEDS` Dictionary ergänzen:
```python
RSS_FEEDS = {
    # ... bestehende Feeds
    "Neue Quelle": "https://example.com/rss.xml",
}
```

### E-Mail Provider ändern
SMTP-Einstellungen in `config.py` anpassen:
```python
SMTP_SERVER = "smtp.dein-provider.com"
SMTP_PORT = 587
```

## 📋 Voraussetzungen

- Python 3.8+
- Anthropic Claude API Key
- E-Mail-Account mit SMTP-Zugang
- Internetverbindung für RSS-Feeds

## 📝 Lizenz

MIT License - siehe [LICENSE](LICENSE) Datei.

## 🤝 Beitrag leisten

1. Fork das Repository
2. Erstelle einen Feature Branch
3. Committe deine Änderungen
4. Push zum Branch
5. Erstelle einen Pull Request

## 💡 Ideen für Erweiterungen

- [ ] Web-Interface für Konfiguration
- [ ] Mehrere Empfänger
- [ ] Newsletter-Archive
- [ ] Slack/Discord Integration
- [ ] Mobile App
- [ ] Docker Container

## 🐛 Bug Reports & Feature Requests

Bitte öffne ein [Issue](https://github.com/achimbarczok/artificial-newsletter/issues) für:
- Bug Reports
- Feature Requests  
- Fragen zur Nutzung

**Erstellt mit Claude AI**
