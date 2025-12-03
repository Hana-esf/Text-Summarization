import xml.etree.ElementTree as ET
import json
from pathlib import Path
from tqdm import tqdm  # Import tqdm for the progress bar

def find_xml_files(root_folder):
    """
    Recursively find all .xml files in the given folder.
    
    :param root_folder: The root directory to search for .xml files.
    :return: A list of paths to .xml files.
    """
    root_path = Path(root_folder)
    xml_files = list(root_path.rglob('*.xml'))
    return xml_files

def extract_text_with_spaces_and_newlines(section):
    """
    Extracts text from an XML section, preserving spaces and newlines.
    
    :param section: The XML element section to extract text from.
    :return: A formatted string with the extracted text.
    """
    text = []
    for elem in section.iter():
        if elem.text:
            text.append(elem.text.strip())
        if elem.tail:
            text.append(elem.tail.strip())
        if elem.tag in ['p', 'sec', 'abstract', 'body', 'title']:
            text.append('\n')
    
    return ' '.join(text).strip().replace(' \n ', '\n').replace('\n ', '\n').replace(' \n', '\n')

def process_xml_files(folder_path, json_filename='formatted_dataset.json'):
    """
    Processes all XML files in a given folder, extracting abstract and body text,
    and saving them to a JSON file with filenames included, with a progress display.
    
    :param folder_path: The path to the folder containing XML files.
    :param json_filename: The filename of the JSON file to save the data to.
    """
    xml_files = find_xml_files(folder_path)
    data = []
    not_valid = 0
    for file_path in tqdm(xml_files, desc="Processing XML files", unit="file"):
        tree = ET.parse(file_path)
        root = tree.getroot()

        abstract_section = root.find('.//abstract')
        body_section = root.find('.//body')

        abstract_text = extract_text_with_spaces_and_newlines(abstract_section) if abstract_section is not None else ""
        body_text = extract_text_with_spaces_and_newlines(body_section) if body_section is not None else ""
        if abstract_text and body_text:
            data.append({
                'Abstract': abstract_text,
                'Body': body_text
            })
        else:
            not_valid+=1


    # Write all data to JSON file at once
    with open(json_filename, 'w') as file:
        json.dump(data, file, indent=4)
    print(f'{not_valid=}')

# Example usage
folder_path = './article_data'  # Replace with the path to your folder
process_xml_files(folder_path)
