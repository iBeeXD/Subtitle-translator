import argparse
import pysrt
import requests
from tqdm import tqdm

def translate_subtitle(input_file, target_language, output_file):
    # Load subtitle file
    subtitle = pysrt.open(input_file)

    # Translate and replace each subtitle text
    for sub in tqdm(subtitle, desc="Translating", unit="subtitle"):
        # Translate subtitle text to target language using MyMemory API
        translated_text = translate_text(sub.text, target_language)
        
        # Update the subtitle text with translated text
        sub.text = translated_text

    # Save the translated subtitle file
    subtitle.save(output_file)

def translate_text(text, target_language):
    # MyMemory API endpoint
    url = "https://api.mymemory.translated.net/get"
    
    # Request parameters
    params = {
        "q": text,
        "langpair": f"en|{target_language}"
    }

    # Send request to MyMemory API
    response = requests.get(url, params=params)
    
    # Parse response JSON and get translated text
    translated_text = response.json()["responseData"]["translatedText"]
    
    return translated_text

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Translate subtitles using MyMemory API')
    parser.add_argument('-f', '--file', type=str, required=True, help='Input subtitle file path')
    parser.add_argument('-to', '--to_language', type=str, required=True, help='Target language code (e.g., "id" for Indonesian)')
    parser.add_argument('-o', '--output_file', type=str, required=True, help='Output subtitle file path')
    args = parser.parse_args()

    # Translate subtitle
    translate_subtitle(args.file, args.to_language, args.output_file)

if __name__ == '__main__':
    main()

