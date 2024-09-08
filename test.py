import matplotlib.pyplot as plt
import torch
from PIL import Image
from torchvision import transforms

from models import Generator

device = torch.device('cuda' if torch.cuda.is_available() else ('mps' if torch.backends.mps.is_available() else 'cpu'))
print(device)

checkpoint = torch.load('gan.pth', map_location=device)
model = Generator().to(device) # Change `out_channels` parameter for non 3-channel images
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()

def color_img(img, model, transform, device):
    img = transform(img).to(device).unsqueeze(0)

    with torch.no_grad():
        out = model(img)
        out = out.squeeze().permute(1, 2, 0).cpu().numpy()

    return out

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Resize((256, 256)),
    transforms.Normalize([0.5], [0.5])
])

test_img = Image.open('random.png').convert('L')
pred_img = color_img(test_img, model, transform, device)

# Visualize the result
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.imshow(test_img, cmap='gray')
plt.title('Input SAR Image (grayscale)')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow((pred_img+1)/2)
plt.title('Output Optical Image (RGB)')
plt.axis('off')

plt.show()
