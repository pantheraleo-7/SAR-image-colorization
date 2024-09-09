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
    bytes = await file.read()

    arr = torch.frombuffer(bytes, dtype=torch.uint8)
    img_sar = io.decode_image(arr, io.ImageReadMode.GRAY)

    img_opt = colorize(img_sar.unsqueeze(0)).squeeze()
    arr = io.encode_png(img_opt)

    bytes = arr.numpy().tobytes()

    return Response(bytes, media_type='image/png')
