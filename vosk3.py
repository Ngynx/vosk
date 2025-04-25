import subprocess, sys, os, json
from datetime import datetime, timedelta
from vosk import Model, KaldiRecognizer
import pprint
import argparse

# init config
SAMPLE_RATE = 16000
CHUNK_SIZE = 4000

class Transcriber():
    def __init__(self, model_path):
        self.model = Model(model_path)

    def fmt(self, data):
        data = json.loads(data)

        start = min(r["start"] for r in data.get("result", [{ "start": 0 }]))
        end = max(r["end"] for r in data.get("result", [{ "end": 0 }]))

        return {
            "start": str(timedelta(seconds=start)), 
            "end": str(timedelta(seconds=end)), 
            "text": data["text"]
        }

    def transcribe(self, filename):
        rec = KaldiRecognizer(self.model, SAMPLE_RATE)
        rec.SetWords(True)

        if not os.path.exists(filename):
            raise FileNotFoundError(filename)

        transcription = []

        ffmpeg_command = [
                "ffmpeg",
                "-nostdin",
                "-loglevel",
                "quiet",
                "-i",
                filename,
                "-ar",
                str(SAMPLE_RATE),
                "-ac",
                "1",
                "-f",
                "s16le",
                "-",
            ]

        with subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE) as process:

            start_time = datetime.now() 
            while True:
                data = process.stdout.read(4000)
                if len(data) == 0:
                    break
                
                if rec.AcceptWaveform(data):
                    transcription.append(self.fmt(rec.Result()))

            transcription.append(self.fmt(rec.FinalResult()))
            end_time = datetime.now()

            time_elapsed = end_time - start_time
            print(f"Time elapsed  {time_elapsed}")

        return {
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "elapsed_time": time_elapsed,
            "transcription": transcription,
        }


def transcribe(filename, model_path):
    transcriber = Transcriber(model_path)
    transcription = transcriber.transcribe(filename)

    pprint.pprint(transcription)

## args:
# filename = "midudev1.mp3"
# model_path = "vosk-model-es-0.42"

parser = argparse.ArgumentParser(description='Descripción de tu script')
# Añadir argumentos
parser.add_argument('--filename', type=str, required=True, help='Nombre del archivo de audio')
parser.add_argument('--model_path', type=str, required=True, help='ubicacion del modelo')
parser.add_argument('--verbose', action='store_true', help='Mostrar información detallada')

# Parsear los argumentos
args = parser.parse_args()

transcribe(args.filename, args.model_path)