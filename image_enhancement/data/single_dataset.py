import os.path
import torchvision.transforms as transforms
from data.base_dataset import BaseDataset, get_transform
from data.image_folder import make_dataset
from PIL import Image
import numpy as np

class SingleDataset(BaseDataset):
    def initialize(self, opt):
        self.opt = opt
        self.root = opt.dataroot
        self.dir_A = os.path.join(opt.dataroot)

        self.A_paths = make_dataset(self.dir_A)

        self.A_paths = sorted(self.A_paths)

        self.transform = get_transform(opt)

    def __getitem__(self, index):
        A_path = self.A_paths[index]

        A_img = Image.open(A_path).convert('RGB')

        A_img_256 = A_img.resize((np.int32(self.opt.loadSizeX / 2), np.int32(self.opt.loadSizeY / 2)), Image.BICUBIC)
        A_img = A_img.resize((self.opt.loadSizeX,self.opt.loadSizeY), Image.BICUBIC)
        A_img = self.transform(A_img)
        A_img_256 = self.transform(A_img_256)
        return {'A': A_img, 'A_256': A_img_256,'A_paths': A_path}

    def __len__(self):
        return len(self.A_paths)

    def name(self):
        return 'SingleImageDataset'
