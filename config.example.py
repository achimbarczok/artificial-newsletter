# config.example.py - Konfiguration für Privacy Newsletter Generator
# Kopiere diese Datei zu config.py und trage deine echten Daten ein

# =============================================================================
# API KONFIGURATION
# =============================================================================

# Anthropic Claude API Key
# Erhältlich unter: https://console.anthropic.com/
ANTHROPIC_API_KEY = "dein-anthropic-api-key-hier"

# =============================================================================
# E-MAIL KONFIGURATION
# =============================================================================

# E-Mail-Account von dem gesendet wird
EMAIL_USER = "deine-email@gmail.com"

# E-Mail-Passwort (für Gmail: App-Passwort verwenden!)
# Gmail App-Passwort erstellen: https://myaccount.google.com/security
EMAIL_PASSWORD = "dein-email-passwort-oder-app-passwort"

# Empfänger des Newsletters
RECIPIENT_EMAIL = "empfaenger@example.com"

# SMTP-Konfiguration (Gmail Standard - anpassen für andere Provider)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Andere Provider Beispiele:
# Outlook/Hotmail: smtp.live.com, Port 587
# Web.de: smtp.web.de, Port 587
# GMX: smtp.gmx.net, Port 587

# =============================================================================
# RSS FEED QUELLEN
# =============================================================================

RSS_FEEDS = {
    # Deutsche Tech-News Seiten
    "Heise": "https://www.heise.de/rss/heise-atom.xml",
    "Golem": "https://www.golem.de/rss.php?feed=RSS2.0",
    "Netzpolitik": "https://netzpolitik.org/feed/",
    
    # Datenschutz-Spezialisten
    "Datenschutz-Notizen": "https://www.datenschutz-notizen.de/feed/",
    "Dr. Datenschutz": "https://dr-datenschutz.de/feed/",
    
    # Security & Tech
    "Heise Security": "https://www.heise.de/security/rss/news-atom.xml",
    "Telepolis": "https://www.telepolis.de/rss/news/atom.xml",
    
    # Google Alerts (optional - RSS-URLs von Google Alerts hier eintragen)
    # Anleitung: https://www.google.de/alerts → Alert erstellen → RSS-Feed wählen
    # "Google Alerts DSGVO": "https://www.google.de/alerts/feeds/DEINE_URL_HIER",
    # "Google Alerts Privacy": "https://www.google.de/alerts/feeds/DEINE_ZWEITE_URL",
    
    # Weitere internationale Quellen (optional)
    # "Privacy International": "https://privacyinternational.org/rss.xml",
    # "Electronic Frontier Foundation": "https://www.eff.org/rss/updates.xml",
}

# =============================================================================
# NEWSLETTER KONFIGURATION
# =============================================================================

# Anzahl Artikel im Newsletter
MAX_ARTICLES = 10

# Maximales Alter der Artikel in Stunden
MAX_ARTICLE_AGE_HOURS = 24

# Keywords für Datenschutz-Relevanz (wird automatisch gefiltert)
PRIVACY_KEYWORDS = [
    'datenschutz', 'privacy', 'dsgvo', 'gdpr', 'überwachung',
    'tracking', 'cookies', 'surveillance', 'verschlüsselung',
    'encryption', 'biometrie', 'gesichtserkennung', 'whatsapp',
    'meta', 'facebook', 'google', 'amazon', 'apple', 'microsoft',
    'datenschutzbeauftragte', 'bfdi', 'datenschutzbehörde',
    'datenschutzverstoß', 'bußgeld', 'privacy policy', 'consent',
    'ki', 'artificial intelligence', 'machine learning'
]
