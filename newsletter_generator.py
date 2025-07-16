#!/usr/bin/env python3
"""
Privacy Newsletter Generator
============================

Automatischer Newsletter-Generator für Datenschutz-News mit KI-Unterstützung.

Sammelt täglich News von verschiedenen RSS-Quellen, filtert nach Datenschutz-Relevanz,
lässt sie von Claude AI zusammenfassen und versendet sie als schön formatierten Newsletter.

Autor: Achim Barczok (achim@barczok.de)
Entwickelt in Zusammenarbeit mit Claude (Anthropic)

GitHub: https://github.com/achimbarczok/artificial-newsletter
Lizenz: MIT
"""

import requests
from bs4 import BeautifulSoup
import feedparser
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import anthropic
import re
import os

class PrivacyNewsletterGenerator:
    def __init__(self):
        # Lade Konfiguration
        try:
            from config import (
                ANTHROPIC_API_KEY, 
                EMAIL_USER, 
                EMAIL_PASSWORD,
                RECIPIENT_EMAIL,
                SMTP_SERVER,
                SMTP_PORT,
                RSS_FEEDS,
                MAX_ARTICLES,
                MAX_ARTICLE_AGE_HOURS,
                PRIVACY_KEYWORDS
            )
            self.anthropic_api_key = ANTHROPIC_API_KEY
            self.email_user = EMAIL_USER
            self.email_password = EMAIL_PASSWORD
            self.recipient = RECIPIENT_EMAIL
            self.smtp_server = SMTP_SERVER
            self.smtp_port = SMTP_PORT
            self.feeds = RSS_FEEDS
            self.max_articles = MAX_ARTICLES
            self.max_age_hours = MAX_ARTICLE_AGE_HOURS
            self.privacy_keywords = PRIVACY_KEYWORDS
        except ImportError as e:
            print("❌ Fehler: config.py nicht gefunden oder unvollständig!")
            print("📝 Erstelle eine config.py Datei basierend auf config.example.py")
            print(f"🔍 Fehlender Import: {e}")
            print("\n💡 Schnellstart:")
            print("   cp config.example.py config.py")
            print("   nano config.py  # Deine echten Daten eintragen")
            return
        
        # Für dynamische Betreff-Themen
        self.subject_topics = ""
        
    def fetch_privacy_articles(self, max_age_hours=None):
        """Sammelt Datenschutz-relevante Artikel der letzten X Stunden"""
        articles = []
        # Verwende Konfigurationswert falls nicht explizit angegeben
        if max_age_hours is None:
            max_age_hours = self.max_age_hours
            
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        
        # Verwende Keywords aus Konfiguration
        privacy_keywords = self.privacy_keywords
        
        for source, feed_url in self.feeds.items():
            try:
                print(f"Lade Feed von {source}...")
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries:
                    # Zeitcheck
                    if hasattr(entry, 'published_parsed'):
                        pub_date = datetime(*entry.published_parsed[:6])
                        if pub_date < cutoff_time:
                            continue
                    
                    # Datenschutz-Relevanz prüfen
                    title_lower = entry.title.lower()
                    summary_lower = getattr(entry, 'summary', '').lower()
                    
                    if any(keyword in title_lower or keyword in summary_lower 
                           for keyword in privacy_keywords):
                        
                        article = {
                            'source': source,
                            'title': entry.title,
                            'link': entry.link,
                            'summary': getattr(entry, 'summary', ''),
                            'published': getattr(entry, 'published', 'Unbekannt')
                        }
                        articles.append(article)
                        
            except Exception as e:
                print(f"Fehler beim Laden von {source}: {e}")
                
        return articles
    
    def generate_newsletter_content(self, articles):
        """Erstellt Newsletter-Content mit Claude"""
        if not articles:
            return "Heute keine relevanten Datenschutz-News gefunden."
            
        # Artikel-Infos für Claude vorbereiten
        articles_text = ""
        for i, article in enumerate(articles, 1):
            # Datum formatieren falls vorhanden
            pub_date = article.get('published', 'Unbekannt')
            if pub_date != 'Unbekannt':
                try:
                    # Versuche das Datum zu parsen und zu formatieren
                    from dateutil import parser
                    parsed_date = parser.parse(pub_date)
                    formatted_date = parsed_date.strftime('%d.%m.%Y %H:%M')
                except:
                    formatted_date = pub_date
            else:
                formatted_date = 'Unbekannt'
                
            articles_text += f"""
Artikel {i}:
Quelle: {article['source']}
Titel: {article['title']}
Veröffentlicht: {formatted_date}
Link: {article['link']}
Zusammenfassung: {article['summary'][:500]}...
---
"""
        
        prompt = f"""
Du bist ein Tech-affiner Datenschutz-Journalist und erstellst einen informativen aber lockeren Newsletter über Datenschutz-News. 

Hier sind die heutigen Artikel:
{articles_text}

AUFGABE:
1. Wähle die {self.max_articles} INTERESSANTESTEN und DATENSCHUTZ-RELEVANTESTEN Artikel aus
2. Sortiere sie nach Datenschutz-Relevanz und Wichtigkeit (wichtigster zuerst)
3. Erstelle einen Newsletter mit:
   - Einer lockeren, einladenden Einleitung (kein steifes "Sehr geehrte Damen und Herren")
   - Für jeden der {self.max_articles} ausgewählten Artikel: eine verständliche, lockere Zusammenfassung (2-3 Sätze) mit Quelle, Veröffentlichungsdatum und Link
   - KEINE Nummerierung der Artikel
   - Am Ende einen sympathischen Hinweis, dass dieser Newsletter automatisch von der KI Claude (Anthropic) erstellt wurde

WICHTIG: Schreibe ALLE {self.max_articles} Artikel vollständig aus. Verwende KEINE Platzhalter wie "weitere Artikel..." oder Abkürzungen. Jeder Artikel muss komplett geschrieben werden.

Format als HTML für E-Mail mit ansprechendem, aber nicht zu förmlichem Styling.
Jeder Artikel MUSS die Quelle und das Veröffentlichungsdatum enthalten.

Zusätzlich: Gib mir am Ende eine separate Zeile mit den 3 wichtigsten Themen der ersten 3 Artikel für den E-Mail-Betreff aus, Format:
BETREFF-THEMEN: Thema1, Thema2, Thema3
"""

        try:
            import anthropic
            
            # Robuste Client-Initialisierung ohne problematische Parameter
            try:
                client = anthropic.Anthropic(api_key=self.anthropic_api_key)
            except TypeError as e:
                # Fallback für ältere Library-Versionen
                print(f"Anthropic Client Fehler: {e}")
                client = anthropic.Client(api_key=self.anthropic_api_key)
            
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.content[0].text
            
            # Extrahiere Betreff-Themen falls vorhanden
            if "BETREFF-THEMEN:" in content:
                lines = content.split('\n')
                for line in lines:
                    if line.startswith("BETREFF-THEMEN:"):
                        self.subject_topics = line.replace("BETREFF-THEMEN:", "").strip()
                        # Entferne diese Zeile aus dem Content
                        content = content.replace(line, "").strip()
                        break
            
            return content
            
        except Exception as e:
            print(f"Fehler bei Claude API: {e}")
            print("Verwende Fallback-Newsletter...")
            return self.create_fallback_newsletter(articles)
    
    def create_fallback_newsletter(self, articles):
        """Erstellt einen schön gestylten Newsletter falls Claude nicht verfügbar ist"""
        # Sortiere zufällig und nimm nur die ersten 10
        import random
        selected_articles = random.sample(articles, min(self.max_articles, len(articles)))
        
        html_content = """
        <html>
        <head>
            <style>
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }
                .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 12px; text-align: center; margin-bottom: 30px; }
                .header h1 { margin: 0; font-size: 28px; }
                .header p { margin: 10px 0 0 0; opacity: 0.9; font-size: 16px; }
                .article { background: #f8f9fa; border-left: 4px solid #667eea; padding: 25px; margin-bottom: 25px; border-radius: 10px; box-shadow: 0 2px 6px rgba(0,0,0,0.08); transition: transform 0.2s; }
                .article:hover { transform: translateY(-2px); }
                .article h3 { margin-top: 0; font-size: 20px; line-height: 1.4; }
                .article h3 a { color: #667eea; text-decoration: none; }
                .article h3 a:hover { text-decoration: underline; color: #5a67d8; }
                .meta { color: #666; font-size: 14px; margin-bottom: 15px; }
                .source { font-weight: bold; color: #764ba2; }
                .date { font-style: italic; }
                .summary { font-size: 16px; line-height: 1.7; }
                .footer-note { margin-top: 40px; padding: 20px; background: linear-gradient(135deg, #f1f3f4 0%, #e8eaf6 100%); border-radius: 10px; text-align: center; font-size: 14px; color: #555; }
                .footer-note p { margin: 5px 0; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Datenschutz News</h1>
                <p>Was heute in der Datenschutz-Welt passiert ist</p>
            </div>
        """
        
        for article in selected_articles:
            # Datum formatieren
            pub_date = article.get('published', 'Unbekannt')
            if pub_date != 'Unbekannt':
                try:
                    from dateutil import parser
                    parsed_date = parser.parse(pub_date)
                    formatted_date = parsed_date.strftime('%d.%m.%Y %H:%M')
                except:
                    formatted_date = pub_date
            else:
                formatted_date = 'Unbekannt'
                
            html_content += f"""
            <div class="article">
                <h3><a href="{article['link']}">{article['title']}</a></h3>
                <div class="meta">
                    <span class="source">{article['source']}</span> | 
                    <span class="date">{formatted_date}</span>
                </div>
                <div class="summary">{article['summary'][:400]}...</div>
            </div>
            """
        
        html_content += '''
            <div class="footer-note">
                <p>Hey! Dieser Newsletter wurde von Claude (Anthropic) zusammengestellt.</p>
                <p>Die KI hat die Artikel ausgewählt, zusammengefasst und schick formatiert. Ziemlich cool, oder?</p>
            </div>
        </body>
        </html>
        '''
        return html_content
    
    def send_newsletter(self, content):
        """Verschickt den Newsletter per E-Mail"""
        try:
            # Dynamischer Betreff mit Themen
            base_subject = f"🔒 Datenschutz Newsletter - {datetime.now().strftime('%d.%m.%Y')}"
            if self.subject_topics:
                subject = f"{base_subject} | {self.subject_topics}"
            else:
                subject = base_subject
                
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.email_user
            msg['To'] = self.recipient
            
            # HTML Content
            html_part = MIMEText(content, 'html')
            msg.attach(html_part)
            
            # E-Mail senden
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_user, self.email_password)
            server.send_message(msg)
            server.quit()
            
            print(f"Newsletter erfolgreich an {self.recipient} gesendet!")
            return True
            
        except Exception as e:
            print(f"Fehler beim E-Mail-Versand: {e}")
            return False
    
    def run(self):
        """Führt den kompletten Newsletter-Prozess aus"""
        print("🔍 Sammle Datenschutz-News...")
        articles = self.fetch_privacy_articles()
        
        print(f"📰 {len(articles)} relevante Artikel gefunden")
        
        if articles:
            print("✍️ Erstelle Newsletter mit Claude...")
            content = self.generate_newsletter_content(articles)
            
            print("📧 Sende Newsletter...")
            success = self.send_newsletter(content)
            
            if success:
                print("✅ Newsletter-Prozess abgeschlossen!")
            else:
                print("❌ Fehler beim Versenden")
        else:
            print("ℹ️ Keine relevanten Artikel gefunden")

def main():
    generator = PrivacyNewsletterGenerator()
    generator.run()

if __name__ == "__main__":
    main()