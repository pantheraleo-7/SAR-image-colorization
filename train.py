import torch
import torch.nn as nn
from torchvision import models
from torch.nn.functional import relu
from torch.utils.data import DataLoader
from torchvision import transforms
from torch.utils.data import Dataset,random_split
from PIL import Image
import torch.optim as optim
import os
from glob import glob
import torch.nn.functional as F
from sklearn.model_selection import train_test_split
from torch.utils.data import Subset

import torch
import torch.nn.functional as F
from torch import nn

# Generator for cGAN
class Generator(nn.Module):
    def __init__(self, out_channels=3):
        super().__init__()

        # Downsampling (encoder) path
        self.down1 = self.conv_block(1, 64, norm=False)
        self.down2 = self.conv_block(64, 128)
        self.down3 = self.conv_block(128, 256)
        self.down4 = self.conv_block(256, 512)

        # Upsampling (decoder) path
        self.up1 = self.conv_block(512, 512, transpose=True, norm=False)  # Adjust channels here
        self.up2 = self.conv_block(512 + 256, 256, transpose=True)  # Concatenate u1 with d3
        self.up3 = self.conv_block(256 + 128, 128, transpose=True)  # Concatenate u2 with d2

        self.final = nn.Sequential(
            nn.ConvTranspose2d(128 + 64, out_channels, kernel_size=4, stride=2, padding=1),  # Concatenate u3 with d1
            nn.Tanh()
        )

    def conv_block(self, in_channels, out_channels, transpose=False, norm=True):
        block = nn.Sequential()

        if not transpose:
            block.add_module('conv', nn.Conv2d(in_channels, out_channels, kernel_size=4, stride=2, padding=1))
        else:
            block.add_module('conv_transpose', nn.ConvTranspose2d(in_channels, out_channels, kernel_size=4, stride=2, padding=1))

        if norm:
            block.add_module('batch_norm', nn.BatchNorm2d(out_channels))

        block.add_module('leaky_relu', nn.LeakyReLU(0.2))

        return block

    def forward(self, x):
        # Encoder (downsampling)
        d1 = self.down1(x)
        d2 = self.down2(d1)
        d3 = self.down3(d2)
        d4 = self.down4(d3)

        # Decoder (upsampling) with skip connections
        u1 = self.up1(d4)
        u2 = self.up2(torch.cat([u1, d3], 1))  # Concatenate upsampled and downsampled features
        u3 = self.up3(torch.cat([u2, d2], 1))

        # Final layer with concatenation of u3 and d1
        return self.final(torch.cat([u3, d1], 1))

# Discriminator for cGAN
class Discriminator(nn.Module):
    def __init__(self, out_channels=3):
        super().__init__()

        self.model = nn.Sequential(
            self.conv_block(out_channels+1, 64, norm=False),
            self.conv_block(64, 128),
            self.conv_block(128, 256),
            self.conv_block(256, 512),
            nn.Conv2d(512, 1, kernel_size=4, stride=1, padding=0),
            nn.Sigmoid()
        )

    def conv_block(self, in_channels, out_channels, norm=True):
        block = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=4, stride=2, padding=1)
        )

        if norm:
            block.append(nn.BatchNorm2d(out_channels))

        block.append(nn.LeakyReLU(0.2))

        return block

    def forward(self, x, y):
        return self.model(torch.cat([x, y], 1))
    
class SAROpticalDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.data_pairs = []
        

        for category in ['agri', 'barrenland', 'grassland', 'urban']:
            s1_dir = os.path.join(root_dir, category, 's1')
            s2_dir = os.path.join(root_dir, category, 's2')
            
            s1_images = sorted(os.listdir(s1_dir))
            s2_images = sorted(os.listdir(s2_dir))
            
            for s1_img, s2_img in zip(s1_images, s2_images):
                s1_path = os.path.join(s1_dir, s1_img)
                s2_path = os.path.join(s2_dir, s2_img)
                self.data_pairs.append((s1_path, s2_path))
                
    def __len__(self):
        return len(self.data_pairs)
    
    def __getitem__(self, idx):
        s1_path, s2_path = self.data_pairs[idx]
        s1_image = Image.open(s1_path).convert("L")  # Load as grayscale
        s2_image = Image.open(s2_path).convert("RGB")  # Load as color
        
        if self.transform:
            s1_image = self.transform(s1_image)
            s2_image = self.transform(s2_image)
        
        return s1_image, s2_image

transform = transforms.Compose([
    transforms.Resize((256, 256)),  # Adjust to your model's input size
    transforms.ToTensor()
])


data = SAROpticalDataset(root_dir='/kaggle/input/sentinel12-image-pairs-segregated-by-terrain/v_2/', transform=transform)

train_dataset, valid_dataset = random_split(data, [0.8, 0.2])

BATCH_SIZE = 16
train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
valid_loader = DataLoader(valid_dataset, batch_size=BATCH_SIZE, shuffle=False)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(device)

generator = Generator().to(device)
discriminator = Discriminator().to(device)

criterion_bce = nn.BCELoss()
criterion_l1 = nn.L1Loss()

optimizer_g = optim.Adam(generator.parameters(), lr=0.0002, betas=(0.5, 0.999))
optimizer_d = optim.Adam(discriminator.parameters(), lr=0.0002, betas=(0.5, 0.999))

num_epochs = 10
for epoch in range(1, num_epochs + 1):
    generator.train()
    discriminator.train()

    train_loss_g = 0.0
    train_loss_d = 0.0

    for i, (sar_img, opt_img) in enumerate(train_loader, start=1):
        real = torch.ones(sar_img.size(0), 1, 13, 13).to(device)  # Adjust real and fake to match discriminator output size
        fake = torch.zeros(sar_img.size(0), 1, 13, 13).to(device)
        sar_img, opt_img = sar_img.to(device), opt_img.to(device)

        # Train Generator
        optimizer_g.zero_grad()
        color_img = generator(sar_img)
        loss_g = criterion_bce(discriminator(sar_img, color_img), real) + 100 * criterion_l1(color_img, opt_img)
        loss_g.backward()
        optimizer_g.step()

        # Train Discriminator
        optimizer_d.zero_grad()
        real_loss = criterion_bce(discriminator(sar_img, opt_img), real)
        fake_loss = criterion_bce(discriminator(sar_img, color_img.detach()), fake)
        loss_d = (real_loss + fake_loss) / 2
        loss_d.backward()
        optimizer_d.step()

        train_loss_g += loss_g.item() * sar_img.size(0)
        train_loss_d += loss_d.item() * sar_img.size(0)

        if i % 100 == 0:
            print(f'Batch {i}/{len(train_loader)} | D loss: {loss_d:.4f} | G loss: {loss_g:.4f}')

    train_loss_g /= len(train_dataset)
    train_loss_d /= len(train_dataset)

    generator.eval()

    valid_loss_g = 0.0
    with torch.no_grad():
        for sar_img, opt_img in valid_loader:
            sar_img, opt_img = sar_img.to(device), opt_img.to(device)
            color_img = generator(sar_img)

            valid_loss_bce = criterion_bce(discriminator(sar_img, color_img), real[:color_img.size(0)])  # Same shape for real
            valid_loss_l1 = criterion_l1(color_img, opt_img)
            valid_loss_g += (valid_loss_bce + 100 * valid_loss_l1).item() * sar_img.size(0)

    valid_loss_g /= len(valid_dataset)

    print(f'Epoch {epoch}/{num_epochs} | Train G loss: {train_loss_g:.4f} | Train D loss: {train_loss_d:.4f} | Validation G loss: {valid_loss_g:.4f}')

# Save the model after training
torch.save({
    'epoch': num_epochs,
    'model_state_dict': generator.state_dict(),
    'optimizer_state_dict': optimizer_g.state_dict(),
    'train_loss_g': train_loss_g,  # type: ignore
    'valid_loss_g': valid_loss_g,  # type: ignore
}, 'gan.pth')

print(f'Model saved after {num_epochs} epochs')