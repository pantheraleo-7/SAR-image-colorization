import matplotlib.pyplot as plt
import torch
from PIL import Image
from torchvision import transforms

from dataset import SAROpticalDataset
from models import *

# Choose model to test (unet or cgan)
path = 'unet.pth'
model = UNet() # Change `out_channels` parameter for non 3-channel images

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
checkpoint = torch.load(path, map_location=device)
model.load_state_dict(checkpoint['model_state_dict'])
model.to(device)
model.eval()

transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor()
])

def predict_single_image(img_path, model, transform, device):
    img = Image.open(img_path).convert('L')
    img = transform(img).unsqueeze(0).to(device)

    with torch.no_grad():
        out = model(img)
        out = out.squeeze().permute(1, 2, 0).cpu().numpy()

    return out

test_img_path = 'random.png'
test_img = Image.open(test_img_path)
pred_img = predict_single_image(test_img_path, model, transform, device)

# Visualize the result
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.imshow(test_img.convert('L'), cmap='gray')
plt.title('Original Image (SAR)')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow((pred_img+1)/2)
plt.title('Predicted Image (Optical)')
plt.axis('off')

plt.show()
