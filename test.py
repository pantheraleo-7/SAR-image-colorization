import matplotlib.pyplot as plt
import torch
from PIL import Image
from torchvision import transforms

from models import *

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Choose model to test (unet or cgan)
path = 'unet.pth'
model = UNet().to(device) # Change `out_channels` parameter for non 3-channel images

checkpoint = torch.load(path, map_location=device)
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()

def color_img(img, model, transform, device):
    img = transform(img).to(device).unsqueeze(0)

    with torch.no_grad():
        out = model(img)
        out = out.squeeze().permute(1, 2, 0).cpu().numpy()

    return out

transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor()
])

test_img_path = 'random.png'
test_img = Image.open(test_img_path).convert('L')
pred_img = color_img(test_img, model, transform, device)

# Visualize the result
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.imshow(test_img, cmap='gray')
plt.title('Input B/W Image (SAR)')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow((pred_img+1)/2)
plt.title('Output RGB Image (Optical)')
plt.axis('off')

plt.show()
