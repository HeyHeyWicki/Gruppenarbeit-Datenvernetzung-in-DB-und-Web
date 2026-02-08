from server_schallplatten import app

if __name__ == '__main__':
    # Schallplatten-API Server
    # Läuft auf http://localhost:8080
    app.run(debug=True, host='0.0.0.0', port=8080)
