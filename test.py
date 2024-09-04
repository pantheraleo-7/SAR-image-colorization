import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
import matplotlib.pyplot as plt
from model import UNet 
from customDataset import SAROpticalDataset  
import numpy as np

model_path = 'final_model.pth'
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Use n_class=3 if predicting RGB images
model = UNet(n_class=3) 
checkpoint = torch.load(model_path, map_location=device)
model.load_state_dict(checkpoint['model_state_dict'])
model.to(device)
model.eval()

transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor(),
])

def predict_single_image(img_path, model, transform, device):
    image = Image.open(img_path).convert('L') 
    image = transform(image).unsqueeze(0).to(device)
    
    with torch.no_grad():
        output = model(image)
        output = torch.tanh(output)  
        output = output.squeeze().permute(1, 2, 0).cpu().numpy() 
        
    # plt.figure(figsize=(8, 8))
    # plt.imshow((output + 1) / 2)  
    # plt.axis('off')
    # plt.show()
    return output

test_image_path = 'random.png' 
predicted_image = predict_single_image(test_image_path, model, transform, device)

# Visualize the result
original_image = Image.open(test_image_path)
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(original_image.convert('L'), cmap='gray')
plt.title('Original Image (SAR)')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow((predicted_image + 1) / 2) 
plt.title('Predicted Image (Optical)')
plt.axis('off')

plt.show()
