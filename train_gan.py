import torch
from torch import nn, optim
from torch.utils.data import DataLoader, random_split
from torchvision import transforms

from dataset import SAROpticalDataset
from models import Generator, Discriminator

transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor(),
    # transforms.Normalize((0.5,), (0.5,))
])

data = SAROpticalDataset(root_dir='~/Downloads/dataset', transform=transform)

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
train_loss = valid_loss = None
for epoch in range(1, num_epochs+1):
    generator.train()
    discriminator.train()

    train_loss = 0.0
    for i, (sar_img, opt_img) in enumerate(train_loader, start=1):
        real = torch.ones(BATCH_SIZE, 1, 1, 1).to(device)
        fake = torch.zeros(BATCH_SIZE, 1, 1, 1).to(device)
        sar_img, opt_img = sar_img.to(device), opt_img.to(device)

        # Train Generator
        optimizer_g.zero_grad()
        color_img = generator(sar_img)
        loss_g = criterion_bce(discriminator(sar_img, color_img), real) \
                 + 100*criterion_l1(color_img, opt_img)
        loss_g.backward()
        optimizer_g.step()

        # Train Discriminator
        optimizer_d.zero_grad()
        real_loss = criterion_bce(discriminator(sar_img, opt_img), real)
        fake_loss = criterion_bce(discriminator(sar_img, color_img.detach()), fake)
        loss_d = (real_loss+fake_loss)/2
        loss_d.backward()
        optimizer_d.step()

        train_loss += (loss_g.item()+loss_d.item())*BATCH_SIZE

        if i%10==0: print(f'Batch {i}/{len(train_loader)} | D loss: {loss_d:.4f} | G loss: {loss_g:.4f}')

    train_loss /= len(train_dataset)

    generator.eval()

    valid_loss = 0.0
    with torch.no_grad():
        for sar_img, opt_img in valid_loader:
            sar_img, opt_img = sar_img.to(device), opt_img.to(device)
            color_img = generator(sar_img)
            loss = criterion_bce(color_img, opt_img)

            valid_loss += loss.item()*BATCH_SIZE

    valid_loss /= len(valid_dataset)

    print(f'Epoch {epoch}/{num_epochs} | Train loss: {train_loss:.4f} | Validation loss: {valid_loss:.4f}')

# Save the model after training
torch.save({
    'epoch': num_epochs,
    'model_state_dict': generator.state_dict(),
    'optimizer_state_dict': optimizer_g.state_dict(),
    'train_loss': train_loss, # type: ignore
    'valid_loss': valid_loss, # type: ignore
}, 'gan.pth')

print(f'Model saved after {num_epochs} epochs')
