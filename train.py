import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms
from torchvision.datasets import ImageFolder
import timm

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class Dataset(Dataset):
    def __init__(self, data_dir, transform=None):
        self.data = ImageFolder(data_dir, transform=transform)
    def __len__(self):
        return len(self.data)
    def __getitem__(self, idx):
        return self.data[idx]
    @property
    def classes(self):
        return self.data.classes
dataset = Dataset(data_dir=
          '[Path-To-Dataset]'
)
data_dir = '[Path-To-Data]'
target_to_class = {v : k for k, v in ImageFolder(data_dir).class_to_idx.items()}

transform = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor(),
])
data_dir = '[Path-To-Dataset]'
dataset = Dataset(data_dir, transform)

for image, label in dataset:
    break

dataloader = DataLoader(dataset, batch_size=64, shuffle=True)

for images, labels in dataloader:
    break

class Classifier(nn.Module):
    def __init__(self, num_classes = 2):
        super(Classifier, self).__init__()
        #where we define all parts of the model
        self.base_model = timm.create_model('efficientnet_b0', pretrained=True)
        self.features = nn.Sequential(*list(self.base_model.children())[:-1])
        #make a classifier
        enet_out_size = 1280
        #make a classifier
        self.classifier = nn.Linear(enet_out_size, num_classes)

    def forward(self, x):
        #connect these parts and return the output
        x = self.features(x)
        output = self.classifier(x)
        return output

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(),lr=0.001)

transform = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor(),
])

train_folder = '[Path]'
valid_folder = '[Path]'

train_dataset = Dataset(train_folder, transform=transform)
val_dataset = Dataset(valid_folder, transform=transform)

train_loader = DataLoader(train_dataset, batch_size=128, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=128, shuffle=False)

num_epoch = 500
train_loss, val_losses = [], []
model = Classifier(num_classes=2)
for epoch in range(num_epochs):
    #set model to train
    model.train()
    running_loss = 0.0
    for images, labels in train_loader:
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item() * inputs.size(0)
    train_loss = running_loss / len(train_loader.dataset)
    train_losses.append(train_loss)

    model.eval()
    running_loss = 0.0
    with torch.no_grad():
        for images, labels in val_loader:
            outputs = model(images)
            loss = criterion(outputs, labels)
            running_loss += loss.item() * inputs.size(0)
    val_loss = running_loss / len(val_loader.dataset)
    val_losses.append(val_loss)
    print(f"Epoch {epoch+1}/{num_epochs} - Train loss: {train_loss}, Validation loss: {val_loss}")
