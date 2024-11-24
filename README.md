# Hackaton submission
For 2024 https://www.defense-tech-hackathon.com/ on USS Hornet Open space Museum.

## Idea: Localise location of noise from 3 interconnected listeners

The idea is that networked microphones are available everywhere (drones, burnerphones). By connecting them over local network and updating eachother on the arrival times of noise (from ex artillery, gunfire). 

### Demo
Start 3 laptops as listeners with:
```
conda create -n hcktn2 python=3.10
conda activate hcktn2
conda install portaudio # or brew install portaudio
pip install -r audio_stream_listener/requirements.txt

python audio_stream_listener/main.py 4094 './output.jsonl'
```

Organize them in an equilateral triangle. When script is started on the other device you can connect to them via
```
connect 192.168.0.55 4091 
```
This will stream coordinates to './output.jsonl'

Run the [notebook](./notebooks/plot-res.ipynb) to plot the results.

![Alt Text](./notebooks/bang_visualization.gif)


##### Comments
This ended up not working good at all, there's bugs everywhere. 
