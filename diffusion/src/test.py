import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler

model_id = "stabilityai/stable-diffusion-2-1"

# Use the DPMSolverMultistepScheduler (DPM-Solver++) scheduler here instead
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float32)
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
pipe = pipe.to("cpu")

from fastapi import FastAPI, Request
import shutil
import os
from fastapi.responses import FileResponse
import socket
from pydantic import BaseModel

import os
from fastapi import FastAPI
from PIL import Image
import glob

app = FastAPI()

class Prompt(BaseModel):
    prompt: str

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
print("ip_address : ", ip_address)

@app.get('/health')
async def hi():
    return {"response": "server running"}

@app.post('/imageGen')
async def imageGen(request: Request, prompt: Prompt):

    out_path = 'result_images/*'

    # deleting result images
    for path in glob.glob(out_path):
        if os.path.exists(path):
            os.remove(path)

    folder_path = './result_images'

    prompt_text = prompt.prompt

    image = pipe(prompt_text).images[0]

    # Save the image with the given prompt as the filename
    image_path = os.path.join(folder_path, f'{prompt_text}.png')
    image.save(image_path)

    return FileResponse(image_path)
