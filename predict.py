import torch
import torch.nn as nn
from model import CNN

model_path = "./model/cnn.pth"

# Captcha Alphabet (0-9, a-z, A-Z) 
source = [str(i) for i in range(0, 10)]
source += [chr(i) for i in range(97, 97 + 26)]
source += [chr(i) for i in range(65, 65 + 26)]
alphabet = "".join(source)

def predict_captcha(device: str, img_tensor: torch.Tensor, cnn) -> str:
    if device == "cuda":
        img_tensor = img_tensor.cuda()
    img_tensor = img_tensor.view(1, 1, 50, 200)
    output = cnn(img_tensor)
    output = output.view(-1, 62)
    output = nn.functional.softmax(output, dim=1)
    output = torch.argmax(output, dim=1)
    output = output.view(-1, 4)[0]
    label = "".join([alphabet[i] for i in output.cpu().numpy()])
    return label

def preload_model(device: str):
    cnn = CNN()
    if device == "cuda":
        cnn = cnn.cuda()
        cnn.eval()
        cnn.load_state_dict(torch.load(model_path))
    elif device == "cpu":
        cnn.eval()
        model = torch.load(model_path, map_location=device)
        cnn.load_state_dict(model)
    return cnn
