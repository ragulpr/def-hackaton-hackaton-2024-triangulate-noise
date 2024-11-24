# def-hackaton
conda create -n hcktn2 python=3.10
conda activate hcktn2
conda install portaudio # or brew install portaudio
pip install -r audio_stream_listener/requirements.txt

python audio_stream_listener/main.py 4094 "./output.jsonl"
connect 192.168.0.55 4091 