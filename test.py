import torch
from torch.utils.data import DataLoader, Subset
from torchvision import io, utils

from dataset import SAROpticalDataset
from output import colorize


DATASET_PATH = '~/Downloads/dataset'
TEST_SIZE = 9

dataset = SAROpticalDataset(root_dir=DATASET_PATH)
test_data = Subset(dataset, range(1, len(dataset), len(dataset)//TEST_SIZE))

test_loader = DataLoader(test_data, batch_size=len(test_data), shuffle=False, drop_last=True)

for sar_imgs, opt_imgs in test_loader:
    color_imgs = colorize(sar_imgs)

    mse = torch.mean(torch.pow(opt_imgs-color_imgs, 2), dtype=torch.float32)
    print('Mean Squared Error:', mse.item())

    imgs = [img for pair in zip(opt_imgs, color_imgs) for img in pair]
    nrow = half+1 if (half:=TEST_SIZE//2)%2==1 else half+2
    io.write_png(utils.make_grid(imgs, nrow), 'test_grid.png')
