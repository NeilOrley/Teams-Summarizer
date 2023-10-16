import os

def save_cleantext_to_file(filename, cleantext):
    """
    Save cleaned text to a specified file.
    
    Parameters:
    - filename (str): The name of the file where the cleaned text should be saved.
    - cleantext (str): The cleaned text to be saved.

    Returns:
    - str: The name of the file where the cleaned text was saved.
    """
    
    # Open the specified file in write mode and save the cleaned text.
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(cleantext)
    
    # Return the filename
    return filename

def save_summary_to_file(filename, summary):
    """
    Save summary to a specified file within the "summary" directory.
    
    Parameters:
    - filename (str): The base name of the file where the summary should be saved.
    - summary (str): The summary to be saved.

    Returns:
    - str: The path to the file where the summary was saved.
    """
    
    # Check if the "summary" directory exists; if not, create it.
    if not os.path.exists('summary'):
        os.makedirs('summary')

    # Prepare the full path for the summary file.
    output_file_path = os.path.join('summary', f'Summary-{filename}.txt')
    
    # Open the summary file in write mode and save the summary.
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(summary)
    
    # Return the path to the summary file.
    return output_file_path