from flask import Flask, jsonify, request, Response
from records_repository import RecordsRepository

app = Flask(__name__)

records_repository = RecordsRepository()

basePath = '/api/records'

@app.route(basePath, methods=['GET'])
def get_records():
    records = records_repository.get_all()
    return jsonify(records), 200


@app.route(basePath+'/<int:record_id>', methods=['GET'])
def get_record(record_id):
    record = records_repository.get(record_id)
    if record:
        return jsonify(record), 200
    return jsonify({"error": "Record not found"}), 404


@app.route(basePath, methods=['POST'])
def create_record():
    data = request.get_json()

    if not data or 'title' not in data or 'artist' not in data:
        return jsonify({"error": "Title and Artist are required"}), 400

    new_record = records_repository.create(
        title=data["title"],
        artist=data["artist"],
        year=data.get("year"),
        genre=data.get("genre"),
        condition=data.get("condition", "Good")
    )

    response = jsonify(new_record)
    response.status_code = 201
    response.headers['Location'] = f"{basePath}/{new_record['id']}"

    return response


@app.route(basePath+'/<int:record_id>', methods=['PUT'])
def update_record(record_id):
    data = request.get_json()

    updated_record = records_repository.update(
        record_id=record_id,
        title=data.get("title"),
        artist=data.get("artist"),
        year=data.get("year"),
        genre=data.get("genre"),
        condition=data.get("condition")
    )

    if not updated_record:
        return jsonify({"error": "Record not found"}), 404

    return jsonify(updated_record), 200


@app.route(basePath+'/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    success = records_repository.delete(record_id)
    # Make DELETE idempotent: always return 200 and a descriptive message
    if success:
        return jsonify({"message": "Record deleted"}), 200

    return jsonify({"message": "Record not found (idempotent)"}), 200
