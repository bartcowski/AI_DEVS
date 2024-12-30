import whisper
import os

def transcribeOrRead(file_name):
    # models downloaded to \Users\<user>\.cache\whisper
    model = whisper.load_model("medium")

    base_file_name, ext = os.path.splitext(file_name)
    transcription_file_name = base_file_name + '.txt'

    if not os.path.exists(transcription_file_name):
        print('READING transcription - ' + transcription_file_name)
        with open(transcription_file_name, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        print('STARTED transcribing - ' + file_name)
        transcription = model.transcribe(file_name)["text"]
        with open(transcription_file_name, 'w', encoding='utf-8') as f:
            f.write(transcription)
        print('FINISHED transcribing - ' + file_name)
        return transcription