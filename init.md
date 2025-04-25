!apt -qq install ffmpeg
!ffmpeg -version
!pip install vosk -q

!pip install argparse

# Download models
# !wget -q https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip
# !wget -q https://alphacephei.com/vosk/models/vosk-model-es-0.42.zip
!unzip \*.zip

## Exec script code
# filename = "midudev1.mp3"
# model_path = "vosk-model-es-0.42"
python3 vosk3.py --filename "midudev1.mp3" --model_paht "vosk-model-small-es-0.42"


#install pip 
curl -O https://bootstrap.pypa.io/get-pip.py
python3.9 get-pip.py
python3.9 -m pip --version