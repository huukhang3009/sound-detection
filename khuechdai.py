import librosa
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt


def load_audio(file_path):
    # Load audio file using librosa
    audio, sr = librosa.load(file_path, sr=None)
    return audio, sr


def amplify_audio(audio, factor):
    # Amplify audio by multiplying each sample by the amplification factor
    amplified_audio = audio * factor
    return amplified_audio


def save_amplified_audio(file_path, amplified_audio, sr):
    # Save the amplified audio using soundfile
    sf.write(file_path, amplified_audio, sr)


def plot_audio_comparison(original_audio, amplified_audio, sr, title):
    # Plot the original and amplified audio signals side by side
    plt.figure(figsize=(14, 6))

    time = np.arange(0, len(original_audio)) / sr

    plt.subplot(2, 1, 1)
    plt.plot(time, original_audio, label='Original Audio')
    plt.title('Original Audio')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(time, amplified_audio, label='Amplified Audio', color='orange')
    plt.title('Amplified Audio')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.legend()

    plt.tight_layout()
    plt.suptitle(title)
    plt.show()


if __name__ == "__main__":
    # Replace 'your_audio_file.wav' with the path to your audio file
    input_file = 'filtered_audio.wav'
    output_file = 'amplified_audio.wav'
    amplification_factor = 3.0  # Increase the amplification factor for stronger amplification

    # Load audio
    audio, sr = load_audio(input_file)

    # Amplify audio with increased amplification factor
    amplified_audio = amplify_audio(audio, amplification_factor)

    # Save amplified audio
    save_amplified_audio(output_file, amplified_audio, sr)

    # Plot original and amplified audio side by side for comparison
    plot_audio_comparison(audio, amplified_audio, sr, 'Original and Amplified Audio Comparison')
