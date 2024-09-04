import torch
import torch.nn as nn
from torchvision import models
from torch.nn.functional import relu
from torch.utils.data import DataLoader
from torchvision import transforms
from torch.utils.data import Dataset
from PIL import Image
import torch.optim as optim
import os
from glob import glob
import torch.nn.functional as F
from sklearn.model_selection import train_test_split
from torch.utils.data import Subset

from model import UNet
from customDataset import SAROpticalDataset

transform = transforms.Compose([
    transforms.Resize((256, 256)),  # Adjust to your model's input size
    transforms.ToTensor()
])

from torch.utils.data import random_split

dataset = SAROpticalDataset(root_dir="/dataset/", transform=transform)

train_size = int(0.8 * len(dataset))  # 80% training
val_size = len(dataset) - train_size  # 20% validation

train_dataset, val_dataset = random_split(dataset, [train_size, val_size])

train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
valid_loader = DataLoader(val_dataset, batch_size=16, shuffle=False)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(device)
model = UNet(n_class=3).to(device)
criterion = nn.BCEWithLogitsLoss()
optimizer = optim.Adam(model.parameters(), lr = 0.001)

num_epochs = 10

for epoch in range(num_epochs):
    model.train()
    train_loss = 0.0
    
    for images, masks in train_loader:
        images, masks = images.to(device), masks.to(device)
        
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, masks)
        loss.backward()
        optimizer.step()
        
        train_loss += loss.item() * images.size(0)
    
    train_loss = train_loss / len(train_loader.dataset)
    
    model.eval()
    valid_loss = 0.0
    with torch.no_grad():
        for images, masks in valid_loader:
            images, masks = images.to(device), masks.to(device)
            outputs = model(images)
            loss = criterion(outputs, masks)
            valid_loss += loss.item() * images.size(0)
            
    valid_loss = valid_loss / len(valid_loader.dataset)
    
    print(f'Epoch {epoch+1}/{num_epochs} | Train_loss: {train_loss:.4f} | Validation loss: {valid_loss:.4f}')

# Save the model after all epochs are completed
torch.save({
    'epoch': num_epochs,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'train_loss': train_loss,
    'valid_loss': valid_loss,
}, 'final_model.pth')

print(f"Model saved after {num_epochs} epochs")
