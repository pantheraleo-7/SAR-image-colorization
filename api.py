import torch
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, FileResponse
from torchvision import io

from output import colorize

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['post'],
    allow_headers=['*'],
)

@app.get('/')
async def home(request: Request):
    return FileResponse('index.html')

@app.post('/')
async def sar_to_optical(file: UploadFile = File(...)):
    png_bytes = await file.read()

    png_arr = torch.frombuffer(png_bytes, dtype=torch.uint8)
    img_in = io.decode_png(png_arr, io.ImageReadMode.GRAY)

    img_out = colorize(img_in.unsqueeze(0)).squeeze()
    png_arr = io.encode_png(img_out)

    png_bytes = png_arr.numpy().tobytes()

    return Response(png_bytes, media_type='image/png')
