import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

# Đường dẫn đến tệp WAV
file_path = 'amplified_audio.wav'

# Đọc tệp WAV
sample_rate, data = wavfile.read(file_path)

# Tạo trục thời gian
duration = len(data) / sample_rate
time = np.linspace(0., duration, len(data))

# Vẽ biểu đồ âm thanh
plt.figure(figsize=(10, 4))
plt.plot(time, data)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('Audio Waveform')
plt.grid(True)
plt.show()