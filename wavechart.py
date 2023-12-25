import os
import numpy as np
import matplotlib.pyplot as plt
import wave

def plot_and_save_audio_waveform(file_path, output_directory):
    with wave.open(file_path, 'rb') as wav_file:
        params = wav_file.getparams()
        num_channels = params.nchannels
        sample_width = params.sampwidth
        sample_rate = params.framerate
        num_frames = params.nframes

        wave_data = wav_file.readframes(num_frames)
        wave_array = np.frombuffer(wave_data, dtype=np.int16)

        if num_channels == 2:
            wave_array = wave_array[::2]

        duration = num_frames / sample_rate
        time = np.linspace(0, duration, len(wave_array))

        plt.figure(figsize=(10, 4))
        plt.plot(time, wave_array)
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.title('Audio Waveform')
        plt.grid(True)

        # Lưu biểu đồ vào thư mục output_directory
        filename = os.path.splitext(os.path.basename(file_path))[0] + ".png"
        output_path = os.path.join(output_directory, filename)
        plt.savefig(output_path)
        plt.close()  # Đóng biểu đồ để tránh hiển thị nếu đang chạy trong môi trường không có GUI

def plot_and_save_audio_waveforms_in_directory(input_directory, output_directory):
    # Tạo thư mục output_directory nếu nó chưa tồn tại
    os.makedirs(output_directory, exist_ok=True)

    # Lặp qua tất cả các tệp trong thư mục input_directory
    for filename in os.listdir(input_directory):
        if filename.endswith(".wav"):
            file_path = os.path.join(input_directory, filename)
            print(f"Plotting and saving waveform for {file_path}")
            plot_and_save_audio_waveform(file_path, output_directory)

# Thay đổi đường dẫn đến thư mục của bạn
audio_directory = "sample"
output_chart_directory = "chart"

# Vẽ và lưu biểu đồ sóng cho tất cả các tệp âm thanh trong thư mục và lưu vào thư mục chart
plot_and_save_audio_waveforms_in_directory(audio_directory, output_chart_directory)
