from pathlib import Path

from PIL import Image
from torch.utils.data import Dataset

class SAROpticalDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        self.root_dir = Path(root_dir).expanduser()
        self.transform = transform
        self.data_pairs = []

        for item in self.root_dir.iterdir():
            if not item.is_dir():
                print(f'Skipped "{item}": not a directory')
                continue

            s1_imgs, s2_imgs = [], []
            category_dir = self.root_dir/item
            for s1 in category_dir.glob('s1*'):
                s1_dir = category_dir/s1
                s1_imgs.extend(s1_dir/img for img in s1_dir.glob('*.png'))
            for s2 in category_dir.glob('s2*'):
                s2_dir = category_dir/s2
                s2_imgs.extend(s2_dir/img for img in s2_dir.glob('*.png'))

            s1_imgs = sorted(s1_imgs, key=lambda path: path.stem)
            s2_imgs = sorted(s2_imgs, key=lambda path: path.stem)
            self.data_pairs.extend(zip(s1_imgs, s2_imgs))

    def __len__(self):
        return len(self.data_pairs)

    def __getitem__(self, idx):
        s1_img_path, s2_img_path = self.data_pairs[idx]
        s1_img = Image.open(s1_img_path).convert('L')
        s2_img = Image.open(s2_img_path).convert('RGB')

        if self.transform:
            s1_img = self.transform(s1_img)
            s2_img = self.transform(s2_img)

        return s1_img, s2_img
