from translate import Translator
import re

def translate_srt(input_file, output_file):
    translator = Translator(from_lang='pt', to_lang='en')

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    with open(output_file, 'w', encoding='utf-8') as f:
        for line in lines:
            if re.match(r'^\d+$', line.strip()):
                f.write(line)  # Write subtitle index
            elif re.match(r'^\d+:\d+:\d+,\d+ --> \d+:\d+:\d+,\d+$', line.strip()):
                f.write(line)  # Write subtitle timing
            else:
                translated = translator.translate(line)
                f.write(translated + '\n')  # Write translated subtitle

if __name__ == "__main__":
    input_file = './subtitle/transcription.srt'
    output_file = './subtitle/output_english.srt'

    translate_srt(input_file, output_file)
    print(f"Translation completed. Translated subtitles saved to '{output_file}'.")