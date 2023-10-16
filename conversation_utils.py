
import openai
import tiktoken
import copy
from file_utils import save_cleantext_to_file
import configparser

# Load configurations from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

openai.api_key = config['DEFAULT']['OPENAI_API_KEY']

# Set maximum message size and chunk length from configuration
MAX_MESSAGE_SIZE = int(config['DEFAULT']['MAX_MESSAGE_SIZE'])
MAX_CHUNK_LENGTH = MAX_MESSAGE_SIZE / 7

def format_conversation(vtt):
    """Converts a VTT file to a conversation transcript format and saves it."""
    transcript = ""
    lines = []
    last_speaker = None
    
    # Extracting speaker and their respective messages
    for line in vtt:
        speaker = line.lines[0].split('>')[0].split('v ')[1]
        if last_speaker != speaker:
            lines.append('\n' + speaker + ': ')
        lines.extend(line.text.strip().splitlines())
        last_speaker = speaker

    # Construct the transcript without repeated lines
    previous = None
    for line in lines:
        if line == previous:
            continue
        transcript += f"{line}"
        previous = line

    return transcript

def chunk_messages(messages):
    """Breaks messages into chunks based on a maximum length."""
    chunk = []
    current_length = 0

    for message in messages:
        if current_length + len(message) > MAX_CHUNK_LENGTH:
            yield " ".join(chunk)
            chunk = []
            current_length = 0
        chunk.append(message)
        current_length += len(message)

    # Yield the last chunk if it's not empty
    if chunk:
        yield " ".join(chunk)


def check_payload_size(messages, model="gpt-3.5-turbo-16k"):

    """Return the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
        }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model:
        #print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
        return check_payload_size(messages, model="gpt-3.5-turbo-0613")
    elif "gpt-3.5-turbo-16k" in model:
        #print("Warning: gpt-3.5-turbo-16k may update over time. Returning num tokens assuming gpt-3.5-turbo-16k-0613.")
        return check_payload_size(messages, model="gpt-3.5-turbo-16k-0613")
    elif "gpt-4" in model:
        #print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
        return check_payload_size(messages, model="gpt-4-0613")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )
    num_tokens = 0
    for message in messages['messages']:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens


def summarize_and_analyze_sentiment(chunks,socketio=None,app=None):
    """Summarizes and analyzes sentiment of conversation chunks using OpenAI."""

    # Initialize counter for excerpts
    excerpt_counter = 1
    
    # Define the introduction message
    base_message = {
        "role": "system",
        "content": "Tu vas recevoir plusieurs extraits d'une conversation Teams dont le format est <orateur>: <message>."
    }
    
    # Define the next message structure
    next_message = {
        "role": "system",
        "content": "Ceci est la partie #{excerpt_counter} de la conversation. Peux-tu réaliser un résumé de cet échange?"
    }

    # Define a sentiment analysis request message
    sentiment_message = {
        "role": "user",
        "content": "Réalise une analyse de sentiment de la conversation?"
    }

    # List to hold all the summaries
    summaries = []

    # Start with a base message as the initial conversation payload
    conversation_payload = {
        "messages": [base_message]
    }
    
    test_conversation_payload = conversation_payload

    # Loop through each message chunk to generate summaries
    for message in chunks:
        # Check if adding the current message would exceed the token limit
        if check_payload_size(test_conversation_payload, "gpt-3.5-turbo-16k") > MAX_MESSAGE_SIZE :
            if socketio is not None:
                with app.app_context():
                    print(app)
                    socketio.emit('response', {'data': f'API Call #{excerpt_counter}. Expected payload {check_payload_size(test_conversation_payload)}!'})                  
            print(f"API Call #{excerpt_counter}. Expected payload {check_payload_size(test_conversation_payload)}!")    

            conversation_payload["messages"].append({
                "role": "system",
                "content": f"Ceci est la partie #{excerpt_counter} de la conversation. Peux-tu réaliser un résumé de cet échange?"
            })  

            # Send the current payload to OpenAI for summarization
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k",
                messages=conversation_payload["messages"],
                temperature=0
            )
            excerpt_counter += 1

            # Extract the summary from the AI's response and append to summaries list
            summary = response.choices[0].message["content"].strip()
            summaries.append(summary)

            # Reset the conversation payload for the next chunk
            conversation_payload = {
                "messages": [next_message]
            }
            
            # Add the current message to the new payload
            conversation_payload["messages"].append({
                "role": "user",
                "content": f"Conversation: {message}"
            })

            # Copy the current state of the conversation payload for further checks
            test_conversation_payload = copy.deepcopy(conversation_payload)

        else:
            # If token limit not reached, add the current message to the payload
            conversation_payload["messages"].append({
                "role": "user",
                "content": f"Conversation: {message}"
            })
            test_conversation_payload["messages"].append({
                "role": "user",
                "content": f"Conversation: {message}"
            })

    # Process the final chunks of conversation
    if socketio is not None:
        with app.app_context():
            socketio.emit('response', {'data': f'API Call #{excerpt_counter}. Expected payload {check_payload_size(test_conversation_payload)}!'})  
    print(f"API Call #{excerpt_counter}. Expected payload {check_payload_size(test_conversation_payload)}!")
    conversation_payload["messages"].append({
        "role": "system",
        "content": f"Ceci est la partie #{excerpt_counter} de la conversation. Peux-tu réaliser un résumé de cet échange?"
    }) 
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=conversation_payload["messages"],
        temperature=0
    )
    excerpt_counter += 1

    # Extract the summary from the AI's response for the final chunks
    summary = response.choices[0].message["content"].strip()   
    summaries.append(summary)

    # Add sentiment analysis request to the payload
    test_conversation_payload["messages"].append(sentiment_message)
    conversation_payload["messages"].append(sentiment_message)
    if socketio is not None:
        with app.app_context():
            socketio.emit('response', {'data': f'Last API Call #{excerpt_counter}. Expected payload {check_payload_size(test_conversation_payload)}!'})  
    print(f"Last API Call #{excerpt_counter}. Expected payload {check_payload_size(test_conversation_payload)}!")
    excerpt_counter += 1
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=conversation_payload["messages"],
        temperature=0
    )

    # Extract the sentiment analysis from the AI's response
    summary = response.choices[0].message["content"].strip()
    summaries.append(summary)

    # Combine all generated summaries into one
    combined_summary = " ".join(summaries)

    return combined_summary