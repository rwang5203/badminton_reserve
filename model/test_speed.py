from cnn import CNN
import torch
from time import time
import numpy as np

path = "cnn.pth"
device = 'cpu'
cnn = CNN().to(device)
state_dict = torch.load(path, map_location=device)
cnn.load_state_dict(state_dict)
cnn.eval()

t = np.random.rand(1, 1, 64, 96)

input = torch.from_numpy(t).float().to(device)
start = time()
for i in range(1000):
    out = cnn(input)
print(time() - start)
