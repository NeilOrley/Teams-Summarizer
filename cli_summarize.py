# Import necessary libraries
import os
import argparse
from conversation_utils import format_conversation, chunk_messages, summarize_and_analyze_sentiment
from file_utils import save_summary_to_file, save_cleantext_to_file
import openai
import configparser
from webvtt import WebVTT

# Load configurations from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# Set the certificate and OpenAI API key from the configuration
os.environ['REQUESTS_CA_BUNDLE'] = config['DEFAULT']['REQUESTS_CA_BUNDLE']
openai.api_key = config['DEFAULT']['OPENAI_API_KEY']

# Main script execution starts here
if __name__ == '__main__':
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Génère un résumé à partir d’un fichier VTT.')
    parser.add_argument('--file_path', type=str, required=True, help='Chemin vers le fichier VTT à résumer.')

    # Parse the arguments
    args = parser.parse_args()

    # Extract file name from the given path and determine the path for the cleaned file
    source_file = args.file_path
    filename = os.path.basename(source_file)
    clean_file = os.path.join('clean_files', f'CleanText-{filename}.txt')

    vtt = WebVTT().read(source_file)

    # Process the source file, format its content, and break it into manageable chunks
    conversation = format_conversation(vtt)    
    #print(f"format_conversation Output : {conversation}")

    # Save the transcript to a file
    save_cleantext_to_file(clean_file, conversation)

    #chunks = list(chunk_messages(conversation))
    #print(f"chunk_messages Output : {chunks}")
    messages = conversation.strip().split('\n')
    # Generate a summary with sentiment analysis for the chunks
    summary = summarize_and_analyze_sentiment(messages)

    # Save the summary to a file
    save_summary_to_file(filename, summary)
