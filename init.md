!apt -qq install ffmpeg
!ffmpeg -version
!pip install vosk -q

!pip install argparse



## Exec script code
# filename = "midudev1.mp3"
# model_path = "vosk-model-es-0.42"
python mi_script.py --filename "midudev1.mp3" --model_paht "vosk-model-es-0.42" 