import tkinter as tk
from tkinter import filedialog
import pyaudio
import wave, sys, threading

import pygame

window = tk.Tk()
window.title("使用AI生成音樂")

window.minsize(width=375, height=667)  # 最小視窗大小
window.configure(background='white')  # 視窗背景顏色

label = tk.Label(window, text="Using AI to generate your music", font=('Arial', 24), bg='white', fg='#4F4F4F',
                 justify='left')
space = tk.Label(window, text=" ", font=('Arial', 18), bg='white', fg='#4F4F4F', justify='left')
space.grid(row=0, column=0, sticky='w', padx=20, pady=25)
label.grid(row=1, column=0, sticky='w', padx=20, pady=5)


# the function of upload the musie


def upload_file():
    path = filedialog.askopenfilename()
    if path:
        print(f"Uploading Music from file: {path}")
        # pygame.mixer.init()
        # pygame.mixer.music.load(path)
        # pygame.mixer.music.play()


event = threading.Event()  # 註冊錄音事件
event2 = threading.Event()  # 註冊停止錄音事件


# 錄製
def recording():
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 2
    fs = 44100
    seconds = 5
    global run, name, ok
    while True:
        event.wait()
        event.clear()
        run = True
        print('start recording...')
        p = pyaudio.PyAudio()
        stream = p.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True)
        frames = []
        while run:
            data = stream.read(chunk)
            frames.append(data)
        print('stop recording')
        stream.stop_stream()
        stream.close()
        p.terminate()
        event2.wait()
        event2.clear()
        # 儲存
        if ok:
            wf = wave.open(f'{name}.wav', 'wb')
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(sample_format))
            wf.setframerate(fs)
            wf.writeframes(b''.join(frames))
            wf.close()
        else:
            pass


record = threading.Thread(target=recording)
record.start()


def start_recording():
    print('recording...')
    event.set()  # 觸發錄音開始事件


def stop_recording():
    global run, name, ok
    run = False
    name = filedialog.asksaveasfilename()
    if name != '':
        ok = True
    event2.set()    # 觸發錄音停止事件

# 播放
def play_file():
    path = filedialog.askopenfilename()
    if path:
        # use pyaudio to open a stream
        # 讀取 .wav檔
        wf = wave.open(path, 'rb')  # 'rb' : 二進位讀取模式。'wb' : 二進位寫入模式。'r+b' : 二進位讀寫模式。
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        buf = 1024
        while True:
            data = wf.readframes(buf)
            if data == '':
                break
            stream.write(data)

        stream.close()
        p.terminate()


def save_mp3():
    # wait where the output  music
    print(f" wait where the output  music")


upload_button = tk.Button(window, background="#ea4462", fg="white", font=('Arial', 14), text="upload your muise",
                          width=50, height=4, borderwidth=0, highlightthickness=0, command=start_recording)
save_button = tk.Button(window, background="#fbabbb", fg="white", font=('Arial', 14), text="save muise", width=50,
                        height=4, borderwidth=0, highlightthickness=0, command=stop_recording)
button3 = tk.Button(window, background="#3e3e3e", fg="white", font=('Arial', 14), text="備用button3", width=50,
                    height=4, borderwidth=0, highlightthickness=0)
button4 = tk.Button(window, background="#fafafa", fg="black", font=('Arial', 14), text="備用button4", width=50,
                    height=4, borderwidth=0, highlightthickness=0)
upload_button.grid(row=2, column=0, sticky='w', padx=20, pady=5)
save_button.grid(row=3, column=0, sticky='w', padx=20, pady=5)
button3.grid(row=4, column=0, sticky='w', padx=20, pady=5)
button4.grid(row=5, column=0, sticky='w', padx=20, pady=5)
window.mainloop()
