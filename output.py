import torch
from torchvision import transforms

from models import Generator


device = torch.device('cuda' if torch.cuda.is_available() else ('mps' if torch.backends.mps.is_available() else 'cpu'))
print('Device:', device)

checkpoint = torch.load('gan.pth', map_location=device)
model = Generator().to(device)
model.load_state_dict(checkpoint['generator_state'])
model.eval()

transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ConvertImageDtype(torch.float32),
    transforms.Normalize([0.5], [0.5])
])

inverse_transform = transforms.Compose([
    transforms.Normalize([-1], [2]),
    transforms.ConvertImageDtype(torch.uint8)
])


def colorize(sar_imgs):
    sar_imgs = transform(sar_imgs)

    with torch.no_grad():
        color_imgs = model(sar_imgs.to(device))
        color_imgs = inverse_transform(color_imgs.cpu())

    return color_imgs
