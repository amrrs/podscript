import gradio as gr 
import whisper
from whisper.utils import write_vtt
import requests
import os
import re

model = whisper.load_model("medium")

def inference(link):
  content = requests.get(link)
  podcast_url = re.findall("(?P<url>\;https?://[^\s]+)", content.text)[0].split(';')[1]
  print(podcast_url)
  

  download = requests.get(podcast_url)

  with open('podcast.mp3', 'wb') as f:
    f.write(download.content)

  result = model.transcribe('podcast.mp3')

  with open('sub.vtt', "w") as txt:
    write_vtt(result["segments"], file=txt)

  return (result['text'], 'sub.vtt')

  


title="PodScript"
description="Get Podcast Transcript"
block = gr.Blocks()

with block:
    gr.HTML(
        """     <center> 
                <h1>PodScript</h1>
                <img src = 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.newbreedmarketing.com%2Fhs-fs%2Fhubfs%2Fshutterstock_1125707303.jpg%3Fwidth%3D5000%26name%3Dshutterstock_1125707303.jpg&f=1&nofb=1&ipt=0ba3d9b639d63b0b737ea63cd81b241cc47f46cb519ac4ca18fd3ce6fc1376ad&ipo=images' width = '20%'></img>
                </center>
        """
    )
    with gr.Group():
        with gr.Box():
          
          link = gr.Textbox(label="Google Podcasts Link")

          with gr.Row().style(mobile_collapse=False, equal_height=True): 
              btn = gr.Button("Get PodScript 🪄")
          
          text = gr.Textbox(
              label="PodScript", 
              placeholder="PodScript Output",
              lines=5)
          
          file = gr.File()
       
          
          btn.click(inference, inputs=[link], outputs=[text,file])

block.launch(debug=True, enable_queue = True)
