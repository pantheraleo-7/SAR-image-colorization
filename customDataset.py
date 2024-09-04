import torch
import torch.nn as nn
from torchvision import models
from torch.nn.functional import relu
from torch.utils.data import DataLoader
from torchvision import transforms
from torch.utils.data import Dataset
from PIL import Image
import torch.optim as optim
import os
from glob import glob
import torch.nn.functional as F
from sklearn.model_selection import train_test_split
from torch.utils.data import Subset

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