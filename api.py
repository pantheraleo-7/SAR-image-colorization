import torch
from fastapi import FastAPI, Request, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, FileResponse
from torchvision import io, transforms

from models import Generator

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['post'],
    allow_headers=['*'],
)

device = torch.device('cuda' if torch.cuda.is_available() else ('mps' if torch.backends.mps.is_available() else 'cpu'))
print(device)

checkpoint = torch.load('gan.pth', map_location=device)
model = Generator().to(device) # Change `out_channels` parameter for non 3-channel images
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()

transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.Lambda(lambda img: img/255.0),
    transforms.Normalize([0.5], [0.5])
])

@app.get('/')
async def home(request: Request):
    return FileResponse('index.html')

@app.post('/')
async def sar_to_optical(file: UploadFile = File(...)):
    contents = await file.read()
    img = torch.frombuffer(contents, dtype=torch.uint8)
    img = io.decode_png(img, io.ImageReadMode.GRAY)
    img = transform(img).unsqueeze(0).to(device)

    with torch.no_grad():
        out = model(img).cpu().squeeze()
        out = (out+1)/2 * 255
        out = out.byte()

    png = io.encode_png(out).numpy()

    return Response(png.tobytes(), media_type='image/png')
