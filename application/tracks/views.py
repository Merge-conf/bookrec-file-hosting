from application import app, db
from flask import request, jsonify, send_file, abort
from flask_uuid import uuid
from application.tracks.models import Track
from io import BytesIO
import os

@app.route('/api/add', methods=['POST'])
def add_track():

    # Validate the audio file
    if request.files:
        file = request.files['track']
    else:
        return jsonify({'error': 'audio track required'}), 400

    if file.content_length > 15.250e+6:
        return jsonify({'error': 'audio file is too big'}), 413
    if file.content_type not in ['audio/mpeg', 'audio/mp3', 'audio/x-wav']:
        return jsonify({'error': 'only wav and mp3 accepted'}), 415

    random_uuid = str(uuid.uuid4())
    track = Track(uuid=random_uuid, data=file.read())
    url = 'https://bookrec-file-hosting.herokuapp.com/api/' + random_uuid

    db.session().add(track)
    db.session().commit()
    return jsonify({'url': url}), 201



@app.route('/api/<uuid>')
def get_track(uuid):
    track = Track.query.filter_by(uuid=uuid).first()
    if track:
        return send_file(BytesIO(track.data), attachment_filename='download',
                         as_attachment=True)
    else:
        return jsonify({'error': 'file not found'}), 404


@app.route('/api/<uuid>', methods=['DELETE'])
def delete_track(uuid):
    track = Track.query.filter_by(uuid=uuid).first()
    if track:
        db.session.delete(track)
        db.session.commit()
    else:
        return jsonify({'error': 'file not found'}), 404

    return jsonify({'success': 'file deleted'}), 204
