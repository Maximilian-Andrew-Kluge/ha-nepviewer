# NEPViewer Solar – Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/release/Maximilian-Andrew-Kluge/ha-nepviewer.svg)](https://github.com/Maximilian-Andrew-Kluge/ha-nepviewer/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Eine inoffizielle Custom Integration für [Home Assistant](https://www.home-assistant.io/), die Echtzeit-Solardaten von **NEP Mikro-Wechselrichtern** (auch: Anker SOLIX, NuaSol, Renesola u.a.) über die [NEPViewer Cloud](https://user.nepviewer.com) abruft.

> **Hinweis:** Dies ist kein offizielles Produkt von Northern Electric & Power (NEP). Die Integration nutzt die inoffizielle NEPViewer Web-API.

---

## Screenshots

<!-- Füge hier Screenshots deines Dashboards ein -->

---

## Funktionen

- ✅ Echtzeit-Leistungsanzeige (W)
- ✅ Energieertrag: Heute, Monat, Jahr, Gesamt (kWh)
- ✅ Umweltnutzen: CO₂, Bäume, km, Stunden, Öl
- ✅ Einrichtung über UI (kein YAML nötig)
- ✅ Unterstützung des HA Energie-Dashboards
- ✅ Konfigurierbares Abfrageintervall
- ✅ Automatisches Token-Refresh

---

## Sensoren

| Sensor | Beschreibung | Einheit |
|---|---|---|
| `sensor.aktuelle_leistung` | Aktuelle PV-Leistung | W |
| `sensor.ertrag_heute` | Erzeugter Strom heute | kWh |
| `sensor.ertrag_diesen_monat` | Erzeugter Strom diesen Monat | kWh |
| `sensor.ertrag_dieses_jahr` | Erzeugter Strom dieses Jahr | kWh |
| `sensor.gesamtertrag` | Gesamtertrag seit Inbetriebnahme | kWh |
| `sensor.co2_eingespart` | Eingesparte CO₂-Emissionen | kg |
| `sensor.baume_gepflanzt_aquivalent` | Entspricht gepflanzten Bäumen | Bäume |
| `sensor.autofahrt_eingespart` | Eingesparte Autokilometer | km |
| `sensor.haushalt_versorgt` | Stunden Haushaltsversorgung | h |
| `sensor.ol_eingespart` | Eingesparte Ölmenge | BBL |

---

## Kompatibilität

Getestet mit folgenden Geräten / Marken (alle über NEPViewer):

- NEP BDM Mikro-Wechselrichter (z.B. BDM-600X)
- Anker SOLIX (NEP-basiert)
- NuaSol Nuawandler
- Renesola (NEP-basiert)

---

## Installation

### Option A – HACS (empfohlen)

1. HACS öffnen → **Integrationen** → drei Punkte oben rechts → **Benutzerdefinierte Repositories**
2. URL eingeben: `https://github.com/Maximilian-Andrew-Kluge/ha-nepviewer`
3. Kategorie: **Integration** → **Hinzufügen**
4. Integration suchen: „NEPViewer Solar" → **Herunterladen**
5. Home Assistant **neu starten**

### Option B – Manuell

1. Den Ordner [`custom_components/nepviewer`](custom_components/nepviewer) herunterladen
2. Nach `/config/custom_components/nepviewer/` kopieren (z.B. via Samba, SSH oder File Editor Add-on)
3. Home Assistant **neu starten**

---

## Einrichtung

1. **Einstellungen → Geräte & Dienste → + Integration hinzufügen**
2. „NEPViewer Solar" suchen
3. Eingeben:
   - **E-Mail**: deine NEPViewer-Login-E-Mail
   - **Passwort**: dein NEPViewer-Passwort
   - **Anlagen-ID**: steht in der URL auf `user.nepviewer.com`, z.B. `DE_XXXXXXXX_XXXX`

Die Anlagen-ID findest du hier:
```
https://user.nepviewer.com/pvPlant/detail?id=DE_XXXXXXXX_XXXX
                                               ^^^^^^^^^^^^^^^^
                                               das ist deine ID
```

---

## Dashboard-Beispiele

### Einfache Entities-Karte

```yaml
type: entities
title: ☀️ Solar NEPViewer
entities:
  - entity: sensor.aktuelle_leistung
    name: Aktuelle Leistung
  - entity: sensor.ertrag_heute
    name: Heute
  - entity: sensor.ertrag_diesen_monat
    name: Diesen Monat
  - entity: sensor.ertrag_dieses_jahr
    name. Dieses Jahr
  - entity: sensor.gesamtertrag
    name: Gesamt
```

### Gauge für aktuelle Leistung

```yaml
type: gauge
entity: sensor.aktuelle_leistung
name: Solar jetzt
min: 0
max: 800
needle: true
severity:
  green: 400
  yellow: 200
  red: 0
```

### Umweltnutzen-Karte

```yaml
type: entities
title: 🌿 Umweltnutzen
entities:
  - entity: sensor.co2_eingespart
    name: CO₂ eingespart
  - entity: sensor.baume_gepflanzt_aquivalent
    name: 🌳 Bäume
  - entity: sensor.autofahrt_eingespart
    name: 🚗 km eingespart
  - entity: sensor.haushalt_versorgt
    name: 🏠 Stunden versorgt
  - entity: sensor.ol_eingespart
    name: 🛢 Öl eingespart
```

### Energie-Dashboard

Die Sensoren `sensor.ertrag_heute` und `sensor.gesamtertrag` können direkt im HA **Energie-Dashboard** unter **Solaranlage** eingetragen werden.

---

## Optionen

Das Abfrageintervall lässt sich anpassen unter:  
**Einstellungen → Geräte & Dienste → NEPViewer Solar → Konfigurieren**

Standard: 300 Sekunden (5 Minuten). Minimum: 30 Sekunden.

---

## Fehlerbehebung

**„Ungültige Anmeldedaten"**  
→ E-Mail und Passwort prüfen (dieselben wie auf user.nepviewer.com)

**„Keine Verbindung"**  
→ Internetverbindung prüfen. Die NEPViewer-API ist manchmal kurz nicht erreichbar.

**Sensoren zeigen `unavailable`**  
→ Logs prüfen unter **Einstellungen → System → Protokolle**, nach `nepviewer` filtern.

**NEP hat die API geändert**  
→ Bitte ein [Issue erstellen](../../issues) mit dem neuen API-Response (Passwort/Token natürlich entfernen).

---

## Mitwirken

Pull Requests und Issues sind herzlich willkommen! Bitte lies vorher [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Lizenz

MIT License – siehe [LICENSE](LICENSE)

---

## Danksagung

- Inspiriert durch [NEPviewerCR](https://github.com/DE-cr/NEPviewerCR) von DE-cr
- API-Erkenntnisse aus der [Home Assistant Community](https://community.home-assistant.io/t/microinverter-integration-nuasol-northern-electric/591399)
