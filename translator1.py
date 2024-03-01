import argparse
import pysrt
import requests
from tqdm import tqdm
import time

def translate_subtitle(input_file, target_language, output_file):
    # Load subtitle file
    subtitle = pysrt.open(input_file)

    # Translate and replace each subtitle text
    for sub in tqdm(subtitle, desc="Translating", unit="subtitle"):
        try:
            # Translate subtitle text to target language
            translated_text = translate_text(sub.text, target_language)
            
            # Update the subtitle text with translated text
            sub.text = translated_text
        except Exception as e:
            print(f"Error translating subtitle: {e}")
        
        # Sleep for a short interval to avoid rate limiting
        time.sleep(1)
        
    # Save the translated subtitle file
    subtitle.save(output_file)

def translate_text(text, target_language):
    url = "https://itrans.xfyun.cn/v2/iat"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json,version=1.0",
        "Host": "itrans.xfyun.cn",
        "Date": time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime())
    }
    api_key = "f32185d386372b0f7f0a50e6158aecb2"
    api_secret = "1e3d89c1c78fc27e92c7ee95e2f8c111"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        translated_text = data["responseData"]["translatedText"]
        return translated_text
    except Exception as e:
        print(f"Error translating text: {e}")
        return text

def main():
    parser = argparse.ArgumentParser(description='Translate subtitles using MyMemory API')
    parser.add_argument('-f', '--file', type=str, required=True, help='Input subtitle file path')
    parser.add_argument('-to', '--to_language', type=str, required=True, help='Target language code (e.g., "id" for Indonesian)')
    parser.add_argument('-o', '--output_file', type=str, required=True, help='Output subtitle file path')
    args = parser.parse_args()

    translate_subtitle(args.file, args.to_language, args.output_file)

if __name__ == '__main__':
    main()

