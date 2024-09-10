from pathlib import Path

import torch
from torch import nn, optim
from torch.utils.data import DataLoader, random_split
from torchvision import transforms

from dataset import SAROpticalDataset
from models import Generator, Discriminator


DATASET_PATH = '~/Downloads/dataset'
BATCH_SIZE = 32
EPOCHS = 5

transform = transforms.Compose([
    transforms.ConvertImageDtype(torch.float32),
    transforms.Normalize([0.5], [0.5])
])

dataset = SAROpticalDataset(root_dir=DATASET_PATH, transform=transform)
train_data, valid_data = random_split(dataset, [0.8, 0.2])

train_loader = DataLoader(train_data, batch_size=BATCH_SIZE, shuffle=True, pin_memory=True, drop_last=True)
valid_loader = DataLoader(valid_data, batch_size=BATCH_SIZE, shuffle=False, pin_memory=True, drop_last=True)

device = torch.device('cuda' if torch.cuda.is_available() else ('mps' if torch.backends.mps.is_available() else 'cpu'))
print('Device:', device)

generator = Generator().to(device)
discriminator = Discriminator().to(device)

optimizer_g = optim.Adam(generator.parameters(), lr=0.0002, betas=(0.5, 0.999))
optimizer_d = optim.Adam(discriminator.parameters(), lr=0.0002, betas=(0.5, 0.999))

criterion_bce = nn.BCEWithLogitsLoss()
criterion_l1 = nn.L1Loss()

fake = torch.zeros(BATCH_SIZE, 1, 13, 13).to(device)
real = torch.ones(BATCH_SIZE, 1, 13, 13).to(device)

epochs_trained = 0
if Path('gan.pth').exists():
    checkpoint = torch.load('gan.pth', map_location=device)

    epochs_trained += checkpoint['epochs_trained']
    generator.load_state_dict(checkpoint['generator_state'])
    discriminator.load_state_dict(checkpoint['discriminator_state'])
    optimizer_g.load_state_dict(checkpoint['optimizer_g_state'])
    optimizer_d.load_state_dict(checkpoint['optimizer_d_state'])

train_loss = valid_loss = None
for epoch in range(1, EPOCHS+1):
    generator.train()
    discriminator.train()

    train_loss = 0.0
    for i, (sar_imgs, opt_imgs) in enumerate(train_loader, start=1):
        sar_imgs, opt_imgs = sar_imgs.to(device), opt_imgs.to(device)

        # Train Generator
        optimizer_g.zero_grad()
        color_imgs = generator(sar_imgs)
        loss_g = criterion_bce(discriminator(sar_imgs, color_imgs), real) \
                 + 100*criterion_l1(color_imgs, opt_imgs)
        loss_g.backward()
        optimizer_g.step()

        # Train Discriminator
        optimizer_d.zero_grad()
        real_loss = criterion_bce(discriminator(sar_imgs, opt_imgs), real)
        fake_loss = criterion_bce(discriminator(sar_imgs, color_imgs.detach()), fake)
        loss_d = (real_loss+fake_loss)/2
        loss_d.backward()
        optimizer_d.step()

        train_loss += (loss_g.item()+loss_d.item())*BATCH_SIZE

        if i%100==0: print(f'Batch {i}/{len(train_loader)} | G loss: {loss_g:.4f} | D loss: {loss_d:.4f}')

    train_loss /= len(train_data)

    generator.eval()

    with torch.no_grad():
        valid_loss = 0.0
        for sar_imgs, opt_imgs in valid_loader:
            sar_imgs, opt_imgs = sar_imgs.to(device), opt_imgs.to(device)
            color_imgs = generator(sar_imgs)
            loss = criterion_bce(color_imgs, opt_imgs)

            valid_loss += loss.item()*BATCH_SIZE

    valid_loss /= len(valid_data)

    # Save Model
    torch.save({
        'epochs_trained': epochs_trained+epoch,
        'train_loss': train_loss,
        'valid_loss': valid_loss,
        'generator_state': generator.state_dict(),
        'discriminator_state': discriminator.state_dict(),
        'optimizer_g_state': optimizer_g.state_dict(),
        'optimizer_d_state': optimizer_d.state_dict()
    }, 'gan.pth')

    print(f'Epoch {epoch}/{EPOCHS} | Train loss: {train_loss:.4f} | Validation loss: {valid_loss:.4f}')
