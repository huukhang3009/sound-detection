import librosa
import scipy.signal
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt


def load_audio(file_path):
    # Load audio file using librosa
    audio, sr = librosa.load(file_path, sr=None)
    return audio, sr


def apply_median_filter(audio, window_size):
    # Apply median filter to the audio signal
    filtered_audio = scipy.signal.medfilt(audio, kernel_size=window_size)
    return filtered_audio


def save_audio(file_path, audio, sr):
    # Save the filtered audio using soundfile
    sf.write(file_path, audio, sr)


def plot_audio_comparison(original_audio, filtered_audio, sr, title):
    # Plot the original and filtered audio signals side by side
    plt.figure(figsize=(14, 6))

    time = np.arange(0, len(original_audio)) / sr

    plt.subplot(2, 1, 1)
    plt.plot(time, original_audio, label='Original Audio')
    plt.title('Original Audio')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(time, filtered_audio, label='Filtered Audio', color='orange')
    plt.title('Filtered Audio')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.legend()

    plt.tight_layout()
    plt.suptitle(title)
    plt.show()


if __name__ == "__main__":
    # Replace 'your_audio_file.wav' with the path to your audio file
    input_file = 'all.wav'
    output_file = 'filtered_audio.wav'
    window_size = 15  # Increase the window size for stronger noise filtering

    # Load audio
    audio, sr = load_audio(input_file)

    # Apply median filter with increased window size
    filtered_audio = apply_median_filter(audio, window_size)

    # Save filtered audio
    save_audio(output_file, filtered_audio, sr)

    # Plot original and filtered audio side by side for comparison
    plot_audio_comparison(audio, filtered_audio, sr, 'Original and Filtered Audio Comparison')
