import os
import sounddevice
from scipy.io.wavfile import write
import tensorflowjs
import scipy.io.wavfile as wf
import numpy as np
from python_speech_features import fbank
import pandas as pd

LENGTH = 43
NUM_FBANKS = 232
EXT = 'wav'

def recordAudio():
    fs = 44100
    seconds = 1
    print("Bắt đầu ghi âm")
    myrecording = sounddevice.rec(int(seconds * fs), samplerate=fs, channels=2)
    sounddevice.wait()
    print("Kết thúc ghi âm")
    write('audio.wav', fs, myrecording)

def read_mfcc(input_filename):
    sample_rate, audio = wf.read(input_filename)
    audio = audio / 2  # Convert to Mono
    energy = np.abs(audio)
    silence_threshold = np.percentile(energy, 95)
    offsets = np.where(energy > silence_threshold)[0]

    vad = VoiceActivityDetection()
    vad.process(audio)
    voice_samples = vad.get_voice_samples()
    audio_voice_only = voice_samples

    mfcc = mfcc_fbank(audio_voice_only, sample_rate)
    return mfcc


# Apply to remove silence
class VoiceActivityDetection:

    def __init__(self):
        self.__step = 160
        self.__buffer_size = 160
        self.__buffer = np.array([], dtype=np.int16)
        self.__out_buffer = np.array([], dtype=np.int16)
        self.__n = 0
        self.__VADthd = 0.
        self.__VADn = 0.
        self.__silence_counter = 0

    def vad(self, _frame):
        frame = np.array(_frame) ** 2.
        result = True
        threshold = 0.1
        thd = np.min(frame) + np.ptp(frame) * threshold
        self.__VADthd = (self.__VADn * self.__VADthd + thd) / float(self.__VADn + 1.)
        self.__VADn += 1.

        if np.mean(frame) <= self.__VADthd:
            self.__silence_counter += 1
        else:
            self.__silence_counter = 0

        if self.__silence_counter > 20:
            result = False
        return result

    def add_samples(self, data):
        self.__buffer = np.append(self.__buffer, data)
        result = len(self.__buffer) >= self.__buffer_size
        return result

    def get_frame(self):
        window = self.__buffer[:self.__buffer_size]
        self.__buffer = self.__buffer[self.__step:]
        return window

    def process(self, data):
        if self.add_samples(data):
            while len(self.__buffer) >= self.__buffer_size:
                window = self.get_frame()
                if self.vad(window):
                    self.__out_buffer = np.append(self.__out_buffer, window)

    def get_voice_samples(self):
        return self.__out_buffer

def pad_mfcc(mfcc, max_length):
    if len(mfcc) < max_length:
        mfcc = np.vstack((mfcc, np.tile(np.zeros(mfcc.shape[1]), (max_length - len(mfcc), 1))))
    return mfcc

def mfcc_fbank(signal: np.array, sample_rate: int):
    filter_banks, energies = fbank(signal, samplerate=sample_rate, nfilt=NUM_FBANKS)
    frames_features = normalize_frames(filter_banks)
    return np.array(frames_features, dtype=np.float32)

def normalize_frames(m, epsilon=1e-12):
    return [(v - np.mean(v)) / max(np.std(v), epsilon) for v in m]


def audio_detection(input_filename, results_df):
    audio = read_mfcc(input_filename)
    model = tensorflowjs.converters.load_keras_model("model.json")

    # Đảm bảo kích thước của audio là đủ lớn để chứa vào batch
    if audio.shape[0] < LENGTH:
        audio = pad_mfcc(audio, LENGTH)

    input_data = np.expand_dims(audio[:LENGTH], -1)

    # Chuyển đổi kích thước nếu cần
    if input_data.shape[0] != LENGTH:
        input_data = np.pad(input_data, ((0, LENGTH - input_data.shape[0]), (0, 0), (0, 0)), mode='constant',
                            constant_values=0)

    batch = np.empty((1, 43, 232, 1), dtype=np.float32)
    batch[0] = input_data

    prediction = model.predict(batch)
    name = ["Background noise", "Eating"]
    index = -1
    max_value = -1
    for i in range(0, len(prediction[0])):
        if max_value < prediction[0][i]:
            max_value = prediction[0][i]
            index = i

    print("Ket Qua: ", name[index])
    print("Chinh Xac: ", max_value)

    results_df = results_df.append({"File": input_filename, "Prediction": name[index], "Accuracy": max_value},
                                   ignore_index=True)

    return results_df


if __name__ == "__main__":
    # Tạo một DataFrame để lưu trữ kết quả
    results_df = pd.DataFrame(columns=["File", "Prediction", "Accuracy"])

    input_folder = "sample"  # Thay đổi đường dẫn tới thư mục của bạn

    # Sắp xếp danh sách các tệp theo thứ tự tăng dần
    sorted_files = sorted(
        os.listdir(input_folder),
        key=lambda x: int(x.split('.')[0]) if x.split('.')[0].isdigit() else float('inf')
    )

    for i, filename in enumerate(sorted_files, start=1):
        if filename.endswith(".wav"):
            input_filepath = os.path.join(input_folder, filename)
            results_df = audio_detection(input_filepath, results_df)

    # Lưu DataFrame vào một tệp Excel
    results_df.to_excel("results.xlsx", index=False)