from pydub import AudioSegment

def extract_text_from_audio(audio_path, length):
    audio = AudioSegment.from_file(audio_path)
    binary_text = ''

    for i in range(length):
        sample_value = audio.raw_data[i]
        binary_text += str(sample_value & 1)

    text = ''.join([chr(int(binary_text[i:i+8], 2)) for i in range(0, len(binary_text), 8)])
    return text

length_of_hidden_text = 1000
extracted_text = extract_text_from_audio("audio.wav", length_of_hidden_text)
print("Extracted Text:", extracted_text)
