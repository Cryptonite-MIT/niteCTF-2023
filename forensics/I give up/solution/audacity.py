from pydub import AudioSegment
import binascii

def text_to_binary(text):
    binary_data = ''.join(format(ord(char), '08b') for char in text)
    return binary_data

def hide_text_in_audio(audio_path, output_path, text_to_hide):
    audio = AudioSegment.from_file(audio_path)
    binary_text = text_to_binary(text_to_hide)

    if len(binary_text) > len(audio.raw_data):
        raise ValueError("Text is too long to be hidden in the given audio file.")
    
    audio_samples = bytearray(audio.raw_data)

    for i in range(len(binary_text)):
        audio_samples[i] = (audio_samples[i] & 0b11111110) | int(binary_text[i])

    modified_audio = AudioSegment(audio_samples, frame_rate=audio.frame_rate, sample_width=audio.sample_width, channels=audio.channels)
    modified_audio.export(output_path, format="wav")

hide_text_in_audio("original_audio.wav", "audio.wav", "nite{n3v3r_g0nn4_g1ve_u_+he_fl4g!}")
