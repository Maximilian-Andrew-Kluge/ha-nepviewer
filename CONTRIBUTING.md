# Mitwirken / Contributing

Danke dass du zu diesem Projekt beitragen möchtest! 🎉

## Wie du helfen kannst

- 🐛 **Bugs melden** → [Issue erstellen](../../issues/new?template=bug_report.md)
- 💡 **Feature vorschlagen** → [Issue erstellen](../../issues/new?template=feature_request.md)
- 🔧 **Code beitragen** → Pull Request erstellen
- 📖 **Dokumentation verbessern** → auch kleine Fixes sind willkommen
- 🌍 **Übersetzungen** → weitere Sprachen in `translations/` hinzufügen

## Pull Request Prozess

1. Fork erstellen
2. Feature-Branch anlegen: `git checkout -b feature/mein-feature`
3. Änderungen committen: `git commit -m "feat: kurze Beschreibung"`
4. Branch pushen: `git push origin feature/mein-feature`
5. Pull Request öffnen

## Neue Geräte / Marken

Wenn du die Integration mit einem anderen NEP-basierten Gerät getestet hast, erstelle bitte ein Issue oder PR mit:
- Gerätemodell und Marke
- Ob es funktioniert hat
- Ggf. Unterschiede in der API-Antwort

## Neue API-Antworten debuggen

Falls NEP die API ändert, hilft es den aktuellen Response zu teilen:

1. Chrome öffnen → `user.nepviewer.com` → F12 → Netzwerk-Tab
2. Seite neu laden → Request `overview` anklicken → Response kopieren
3. **Passwörter und Tokens entfernen!**
4. Als Issue einstellen

## Code-Stil

- Python: PEP 8, Type Hints wo sinnvoll
- Docstrings für alle Klassen und Methoden
- Keine hardcodierten Strings – Konstanten in `const.py`
