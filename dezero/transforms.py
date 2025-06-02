import numpy as np

class Compose:
    def __init__(self, transforms):
        self.transforms = transforms

    def __call__(self, x):
        for t in self.transforms:
            x = t(x)
        return x

class Flatten:
    def __call__(self, x):
        return x.reshape(x.shape[0], -1)

class ToFloat:
    def __call__(self, x):
        return x.astype(np.float32)

class Normalize:
    def __init__(self, mean, std):
        self.mean = mean
        self.std = std

    def __call__(self, x):
        return (x - self.mean) / self.std

class ToInt:
    def __init__(self, dtype=int): 
        self.dtype = dtype

    def __call__(self, x):
        return x.astype(self.dtype)