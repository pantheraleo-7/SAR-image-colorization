from pathlib import Path

from torch.utils.data import Dataset
from torchvision import io


class SAROpticalDataset(Dataset):

    def __init__(self, root_dir, transform=None):
        self.root_dir = Path(root_dir).expanduser()
        self.transform = transform
        self.data_pairs = []

        for item in self.root_dir.iterdir():
            if not item.is_dir():
                print(f'Skipped "{item.name}": not a directory')
                continue

            s1_imgs = [img for s1 in item.glob('s1*') for img in s1.glob('*.png')]
            s2_imgs = [img for s2 in item.glob('s2*') for img in s2.glob('*.png')]

            s1_imgs = sorted(s1_imgs, key=lambda path: path.stem)
            s2_imgs = sorted(s2_imgs, key=lambda path: path.stem)

            self.data_pairs.extend(zip(s1_imgs, s2_imgs))

    def __len__(self):
        return len(self.data_pairs)

    def __getitem__(self, idx):
        s1_img_path, s2_img_path = self.data_pairs[idx]
        s1_img = io.read_image(s1_img_path, io.ImageReadMode.GRAY)
        s2_img = io.read_image(s2_img_path, io.ImageReadMode.RGB)

        if self.transform is not None:
            s1_img = self.transform(s1_img)
            s2_img = self.transform(s2_img)

        return s1_img, s2_img
