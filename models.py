import torch
from torch import nn


class Generator(nn.Module):

    def __init__(self, out_channels=3):
        super().__init__()

        self.down1 = self.conv_block(1, 64, norm=False)
        self.down2 = self.conv_block(64, 128)
        self.down3 = self.conv_block(128, 256)
        self.down4 = self.conv_block(256, 512)

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

        u1 = self.up1(d4)
        u2 = self.up2(torch.cat([u1, d3], 1))
        u3 = self.up3(torch.cat([u2, d2], 1))

        return self.final(torch.cat([u3, d1], 1))


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
