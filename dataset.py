import os

from PIL import Image
from torch.utils.data import Dataset

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
        s1_img = Image.open(s1_path).convert("L")
        s2_img = Image.open(s2_path).convert("RGB")

        if self.transform:
            s1_img = self.transform(s1_img)
            s2_img = self.transform(s2_img)

        return s1_img, s2_img
