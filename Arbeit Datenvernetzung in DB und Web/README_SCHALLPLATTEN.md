# Schallplatten-Datenbank REST-API

Eine einfache REST-API zur Verwaltung einer Schallplatten-Sammlung mit Flask und SQLite.

## Features

- **GET /api/records** - Alle Schallplatten abrufen
- **GET /api/records/<id>** - Eine spezifische Schallplatte abrufen
- **POST /api/records** - Neue Schallplatte hinzufügen
- **PUT /api/records/<id>** - Schallplatte aktualisieren
- **DELETE /api/records/<id>** - Schallplatte löschen

## Installation

### Voraussetzungen
- Python 3.7+
- pip

### Abhängigkeiten installieren

```bash
pip install flask requests pytest
```

SQLite ist bereits in Python integriert (kein zusätzliches pip-Paket nötig).

## Datenbank-Schema

Die SQLite-Datenbank wird automatisch beim ersten Start erstellt:

```
records (
    id: INTEGER PRIMARY KEY AUTOINCREMENT
    title: TEXT (erforderlich)
    artist: TEXT (erforderlich)
    year: INTEGER (optional)
    genre: TEXT (optional)
    condition: TEXT (Default: "Good")
)
```

## Verwendung

### Server starten

```bash
python main_schallplatten.py
```

Die API ist dann verfügbar unter: `http://localhost:8080`

### Beispiel-Requests mit curl

#### GET - Alle Platten abrufen
```powershell
curl http://localhost:8080/api/records
```

#### GET - Eine spezifische Platte abrufen
```powershell
curl http://localhost:8080/api/records/1
```

#### POST - Neue Platte hinzufügen
```powershell
curl -X POST http://localhost:8080/api/records -H "Content-Type: application/json" -d "{""title"":""Dark Side of the Moon"",""artist"":""Pink Floyd"",""year"":1973,""genre"":""Progressive Rock"",""condition"":""Excellent""}"
```

**Oder als PowerShell-Variante (eleganter):**
```powershell
$headers = @{"Content-Type"="application/json"}
$body = '{"title":"Dark Side of the Moon","artist":"Pink Floyd","year":1973,"genre":"Progressive Rock","condition":"Excellent"}'
Invoke-WebRequest -Uri "http://localhost:8080/api/records" -Method POST -Headers $headers -Body $body
```

#### PUT - Eine Platte aktualisieren
```powershell
curl -X PUT http://localhost:8080/api/records/1 -H "Content-Type: application/json" -d "{""condition"":""Very Good""}"
```

#### DELETE - Eine Platte löschen
```powershell
curl -X DELETE http://localhost:8080/api/records/1
```

## Tests ausführen

Starten Sie zuerst den Server in einem anderen Terminal. Dann:

```bash
pytest test_api_schallplatten.py -v
```

## Dateistruktur

- `records_repository.py` - Datenbank-Zugriffslayer (SQLite)
- `server_schallplatten.py` - Flask-API mit Endpunkten
- `main_schallplatten.py` - Entry-Point zum Starten des Servers
- `test_api_schallplatten.py` - Pytest-Tests für die API
- `schallplatten.db` - SQLite-Datenbankdatei (wird automatisch erstellt)

## Wichtige Hinweise

- Die Datenbank-Datei `schallplatten.db` wird im selben Verzeichnis wie `records_repository.py` erstellt
- Beim ersten Start werden 2 Sample-Platten eingefügt (Beatles & Michael Jackson)
- Alle Datenbankoperationen sind automatisch committed/rolled back
- Die API gibt konsistente JSON-Fehlermeldungen zurück
 - DELETE ist idempotent: Löschen einer nicht vorhandenen Ressource gibt ebenfalls Status 200 mit einer erklärenden Nachricht

## Endpunkt-Übersicht

| Methode | Route | Beschreibung | Status |
|---------|-------|-------------|--------|
| GET | `/api/records` | Alle Platten | 200 |
| GET | `/api/records/<id>` | Platte abrufen | 200/404 |
| POST | `/api/records` | Neue Platte erstellen | 201/400 |
| PUT | `/api/records/<id>` | Platte aktualisieren | 200/404 |
| DELETE | `/api/records/<id>` | Platte löschen (idempotent) | 200 |

## Beispiel-Daten beim Start

```json
[
  {
    "id": 1,
    "title": "Abbey Road",
    "artist": "The Beatles",
    "year": 1969,
    "genre": "Rock",
    "condition": "Excellent"
  },
  {
    "id": 2,
    "title": "Thriller",
    "artist": "Michael Jackson",
    "year": 1982,
    "genre": "Pop",
    "condition": "Very Good"
  }
]
```
