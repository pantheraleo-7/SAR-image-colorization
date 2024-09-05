import torch
import torch.nn.functional as F
from torch import nn

class UNet(nn.Module):
    def __init__(self, out_channels=3):
        super().__init__()

        # Encoder
        self.e11 = nn.Conv2d(1, 16, kernel_size=3, padding=1)
        self.e12 = nn.Conv2d(16, 16, kernel_size=3, padding=1)
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)

        self.e21 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.e22 = nn.Conv2d(32, 32, kernel_size=3, padding=1)
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)

        self.e31 = nn.Conv2d(32, 48, kernel_size=3, padding=1)
        self.e32 = nn.Conv2d(48, 48, kernel_size=3, padding=1)
        self.pool3 = nn.MaxPool2d(kernel_size=2, stride=2)

        self.e41 = nn.Conv2d(48, 64, kernel_size=3, padding=1)
        self.e42 = nn.Conv2d(64, 64, kernel_size=3, padding=1)
        self.pool4 = nn.MaxPool2d(kernel_size=2, stride=2)

        self.e51 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.e52 = nn.Conv2d(128, 128, kernel_size=3, padding=1)

        # Decoder
        self.upconv1 = nn.ConvTranspose2d(128, 64, kernel_size=2, stride=2)
        self.d11 = nn.Conv2d(128, 64, kernel_size=3, padding=1)
        self.d12 = nn.Conv2d(64, 64, kernel_size=3, padding=1)

        self.upconv2 = nn.ConvTranspose2d(64, 48, kernel_size=2, stride=2)
        self.d21 = nn.Conv2d(96, 48, kernel_size=3, padding=1)  # 48 + 48 channels
        self.d22 = nn.Conv2d(48, 48, kernel_size=3, padding=1)

        self.upconv3 = nn.ConvTranspose2d(48, 32, kernel_size=2, stride=2)
        self.d31 = nn.Conv2d(64, 32, kernel_size=3, padding=1)  # 32 + 32 channels
        self.d32 = nn.Conv2d(32, 32, kernel_size=3, padding=1)

        self.upconv4 = nn.ConvTranspose2d(32, 16, kernel_size=2, stride=2)
        self.d41 = nn.Conv2d(32, 16, kernel_size=3, padding=1)  # 16 + 16 channels
        self.d42 = nn.Conv2d(16, 16, kernel_size=3, padding=1)

        # Output layer
        self.outconv = nn.Conv2d(16, out_channels, kernel_size=1)

    def forward(self, x):
        # Encoder
        xe11 = F.relu(self.e11(x))
        xe12 = F.relu(self.e12(xe11))
        xp1 = self.pool1(xe12)

        xe21 = F.relu(self.e21(xp1))
        xe22 = F.relu(self.e22(xe21))
        xp2 = self.pool2(xe22)

        xe31 = F.relu(self.e31(xp2))
        xe32 = F.relu(self.e32(xe31))
        xp3 = self.pool3(xe32)

        xe41 = F.relu(self.e41(xp3))
        xe42 = F.relu(self.e42(xe41))
        xp4 = self.pool4(xe42)

        xe51 = F.relu(self.e51(xp4))
        xe52 = F.relu(self.e52(xe51))

        # Decoder
        xu1 = self.upconv1(xe52)
        xu11 = torch.cat([xu1, xe42], dim=1)
        xd11 = F.relu(self.d11(xu11))
        xd12 = F.relu(self.d12(xd11))

        xu2 = self.upconv2(xd12)
        xu22 = torch.cat([xu2, xe32], dim=1)
        xd21 = F.relu(self.d21(xu22))
        xd22 = F.relu(self.d22(xd21))

        xu3 = self.upconv3(xd22)
        xu33 = torch.cat([xu3, xe22], dim=1)
        xd31 = F.relu(self.d31(xu33))
        xd32 = F.relu(self.d32(xd31))

        xu4 = self.upconv4(xd32)
        xu44 = torch.cat([xu4, xe12], dim=1)
        xd41 = F.relu(self.d41(xu44))
        xd42 = F.relu(self.d42(xd41))

        # Output layer
        out = self.outconv(xd42)
        out = F.tanh(out)

        return out

# Generator for cGAN
class Generator(nn.Module):
    def __init__(self, out_channels=3):
        super().__init__()

        self.down1 = self.conv_block(1, 64, norm=False)
        self.down2 = self.conv_block(64, 128)
        self.down3 = self.conv_block(128, 256)
        self.down4 = self.conv_block(256, 512)

        self.upsample = nn.Upsample(scale_factor=2)

        self.up1 = self.conv_block(512, 256, transpose=True)
        self.up2 = self.conv_block(512, 128, transpose=True)
        self.up3 = self.conv_block(256, 64, transpose=True)

        self.final = nn.Sequential(
            nn.ConvTranspose2d(128, out_channels, kernel_size=4, stride=2, padding=1),
            nn.Tanh()
        )

    def conv_block(self, in_channels, out_channels, transpose=False, norm=True):
        block = nn.Sequential()

        if not transpose:
            block.append(nn.Conv2d(in_channels, out_channels, kernel_size=4, stride=2, padding=1))
        else:
            block.append(nn.ConvTranspose2d(in_channels, out_channels, kernel_size=4, stride=2, padding=1))

        if norm:
            block.append(nn.BatchNorm2d(out_channels))

        block.append(nn.LeakyReLU(0.2))

        return block

    def forward(self, x):
        d1 = self.down1(x)
        d2 = self.down2(d1)
        d3 = self.down3(d2)
        d4 = self.down4(d3)

        u1 = self.up1(self.upsample(d4))
        u2 = self.up2(self.upsample(torch.cat([u1, d3], 1)))
        u3 = self.up3(self.upsample(torch.cat([u2, d2], 1)))

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
