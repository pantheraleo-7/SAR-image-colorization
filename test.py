import torch
from torch.utils.data import DataLoader, Subset
from torchvision import io, utils

from dataset import SAROpticalDataset
from output import colorize

dataset = SAROpticalDataset(root_dir='~/Downloads/dataset')

test_size = 10
test_data = Subset(dataset, range(1, len(dataset), len(dataset)//test_size))

test_loader = DataLoader(test_data, batch_size=test_size, shuffle=False, drop_last=True)

for sar_imgs, opt_imgs in test_loader:
    color_imgs = colorize(sar_imgs)

    mse = torch.mean(torch.pow(opt_imgs-color_imgs, 2), dtype=torch.float32)
    print('Mean Squared Error:', mse.item())

    imgs = [img for pair in zip(opt_imgs, color_imgs) for img in pair]
    nrow = half if (half:=test_size//2)%2==0 else half-1
    io.write_png(utils.make_grid(imgs, nrow), 'test_grid.png')
