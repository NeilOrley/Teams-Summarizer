from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
import os
import re
from conversation_utils import format_conversation, chunk_messages, summarize_and_analyze_sentiment
import openai
import configparser
from webvtt import WebVTT

# Load configurations from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# Set the certificate and OpenAI API key from the configuration
os.environ['REQUESTS_CA_BUNDLE'] = config['DEFAULT']['REQUESTS_CA_BUNDLE']
openai.api_key = config['DEFAULT']['OPENAI_API_KEY']

app = Flask(__name__)
CORS(app)  # <- Ajoutez cette ligne pour activer CORS pour toute l'application
socketio = SocketIO(app, debug=True, cors_allowed_origins="*")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Récupérer le fichier du formulaire
        file = request.files['file']
        if file:
            with app.app_context():
                socketio.emit('response', {'data': f'Sauvegarde temporaire du fichier {file.filename}'})
            # Sauvegarde temporaire du fichier
            temp_path = os.path.join("vtt_files", file.filename)  # Changez "temp_directory" par le chemin de votre choix
            file.save(temp_path)            
            # Lire le contenu du fichier VTT
            vtt = WebVTT().read(temp_path)
            # Suppression du fichier temporaire
            os.remove(temp_path)
            #summary="youhouh"
            #return render_template('index.html', summary=summary)
            # Process the source file, format its content, and break it into manageable chunks
            with app.app_context():
                socketio.emit('response', {'data': f'Mise en forme de la conversation'})
            conversation = format_conversation(vtt)       
            with app.app_context():
                socketio.emit('response', {'data': f'Découpage de la conversation en portions'})     
            chunks = list(chunk_messages(conversation))
            # Generate a summary with sentiment analysis for the chunks
            with app.app_context():
                socketio.emit('response', {'data': f'Résumé et analyse de sentiment en cours'})  
            summary = summarize_and_analyze_sentiment(chunks, socketio,app)

            # Affichez le résultat
            return render_template('index.html', summary=summary)
    
    return render_template('index.html', summary=None)

@socketio.on('message')
def handle_message(message):
    print('Received message:', message)
    # Vous pouvez émettre un message de retour ou effectuer d'autres opérations si nécessaire
    socketio.emit('response', {'data': 'Application connectée!'})


if __name__ == '__main__':
    #app.run(debug=True)
    socketio.run(app)
