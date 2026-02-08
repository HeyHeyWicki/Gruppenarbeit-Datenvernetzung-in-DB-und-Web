#!/usr/bin/env python3
"""Schneller API-Test ohne pytest"""
import requests
import json

BASE_URL = "http://localhost:8080"
API = f"{BASE_URL}/api/records"

print("=" * 60)
print("SCHALLPLATTEN-API QUICK TEST")
print("=" * 60)

# 1. GET - Alle Platten
print("\n1. GET /api/records (Alle Platten)")
try:
    resp = requests.get(API)
    print(f"   Status: {resp.status_code}")
    print(f"   Daten: {json.dumps(resp.json(), indent=2, ensure_ascii=False)}")
except Exception as e:
    print(f"   ❌ Fehler: {e}")

# 2. POST - Neue Platte
print("\n2. POST /api/records (Neue Platte)")
new_record = {
    "title": "Dark Side of the Moon",
    "artist": "Pink Floyd",
    "year": 1973,
    "genre": "Progressive Rock",
    "condition": "Excellent"
}
try:
    resp = requests.post(API, json=new_record)
    print(f"   Status: {resp.status_code}")
    if resp.status_code == 201:
        print(f"   ✓ Erfolgreich erstellt!")
        print(f"   Location Header: {resp.headers.get('Location')}")
        print(f"   Response: {json.dumps(resp.json(), indent=2, ensure_ascii=False)}")
        created_id = resp.json()['id']
    else:
        print(f"   ❌ Fehler: {resp.text}")
except Exception as e:
    print(f"   ❌ Fehler: {e}")

# 3. GET - Einzelne Platte
print("\n3. GET /api/records/1 (Einzelne Platte)")
try:
    resp = requests.get(f"{API}/1")
    print(f"   Status: {resp.status_code}")
    print(f"   Daten: {json.dumps(resp.json(), indent=2, ensure_ascii=False)}")
except Exception as e:
    print(f"   ❌ Fehler: {e}")

# 4. PUT - Platte aktualisieren
print("\n4. PUT /api/records/1 (Platte aktualisieren)")
update_data = {"condition": "Very Good"}
try:
    resp = requests.put(f"{API}/1", json=update_data)
    print(f"   Status: {resp.status_code}")
    if resp.status_code == 200:
        print(f"   ✓ Erfolgreich aktualisiert!")
        print(f"   Daten: {json.dumps(resp.json(), indent=2, ensure_ascii=False)}")
    else:
        print(f"   ❌ Fehler: {resp.text}")
except Exception as e:
    print(f"   ❌ Fehler: {e}")

# 5. DELETE - Platte löschen
print("\n5. DELETE /api/records/3 (Platte löschen)")
try:
    resp = requests.delete(f"{API}/3")
    print(f"   Status: {resp.status_code}")
    if resp.status_code == 200:
        print(f"   ✓ Erfolgreich gelöscht!")
        print(f"   Response: {json.dumps(resp.json(), indent=2, ensure_ascii=False)}")
    else:
        print(f"   ❌ Fehler: {resp.text}")
except Exception as e:
    print(f"   ❌ Fehler: {e}")

print("\n" + "=" * 60)
print("TEST ABGESCHLOSSEN")
print("=" * 60)
