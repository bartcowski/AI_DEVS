import whisper
import os

mp3_files = ['2024-11-12_report-10-sektor-C1.mp3', '2024-11-12_report-11-sektor-C2.mp3', '2024-11-12_report-12-sektor_A1.mp3']

#models downloaded to C:\Users\barto\.cache\whisper
model = whisper.load_model("medium")

for file_name in mp3_files:
    base_file_name, ext = os.path.splitext(file_name)
    transcription_file_name = base_file_name + '.txt'
    if not os.path.exists(transcription_file_name):
        print('STARTED transcribing - ' + file_name)
        transcription = model.transcribe('./data/' + file_name)["text"]
        with open(transcription_file_name, 'w', encoding='utf-8') as f:
            f.write(transcription)
        print('FINISHED transcribing - ' + file_name)