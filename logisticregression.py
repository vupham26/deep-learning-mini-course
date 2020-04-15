# -*- coding: utf-8 -*-
"""MattsLogisticRegression.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1eLsE90jDzB58Vb6SuVQqrRgvmkUcKKtm
"""

# Import all the packages
import torch
import torch.nn as nn
import torchvision.datasets as dSets
import torchvision.transforms as transforms


# Step 1 - Create Dataset
# We will be using the MNIST dataset for training
# These are images that are a number 1 through 9
train_dataset = dSets.MNIST(root='./data', train=True, transform=transforms.ToTensor(), download=True)
test_dataset = dSets.MNIST(root='./data', train=False, transform=transforms.ToTensor())

# Step 2 - Make Dataset Iterable
train_loader = torch.utils.data.DataLoader(dataset=train_dataset, batch_size=100, shuffle=True)
test_loader = torch.utils.data.DataLoader(dataset=test_dataset, batch_size=100, shuffle=False)

# Step 3 - Create Model Class
class LogisticRegressionModel(nn.Module):
  def __init__(self, input_size, output_size):
    super(LogisticRegressionModel, self).__init__()
    self.linear = nn.Linear(input_size, output_size)

  def forward(self, x):
    y_predict = self.linear(x)
    return y_predict

# Step 4 - Instantiate Model Class
input_dim = 784
output_dim = 10

model = LogisticRegressionModel(input_dim,output_dim)

# Step 5 - Instantiate Loss Class
loss_fn = nn.CrossEntropyLoss()

#Step 6 - Instantiate Optimizer Class
learning_rate = 0.001
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

# Step 7 - Train model
iter = 0
for epoch in range(1):
    for i, (images, labels) in enumerate(train_loader):
        # Load images as Variable
        images = images.view(-1, 28*28).requires_grad_()
        labels = labels

        # Clear gradients w.r.t. parameters
        optimizer.zero_grad()

        # Forward pass to get output/logits
        outputs = model(images)

        # Calculate Loss: softmax --> cross entropy loss
        loss = loss_fn(outputs, labels)

        # Computes the sum of gradients of given tensors w.r.t. graph leaves
        loss.backward()

        # Updating parameters
        optimizer.step()

        iter += 1

        if iter % 100 == 0:
            # Calculate Accuracy         
            correct = 0
            total = 0
            # Iterate through test dataset
            for images, labels in test_loader:
                # Load images to a Torch Variable
                images = images.view(-1, 784).requires_grad_()

                # Forward pass only to get logits/output
                outputs = model(images)

                # Get predictions from the maximum value
                _, predicted = torch.max(outputs.data, 1)

                # Total number of labels
                total += labels.size(0)

                # Total correct predictions
                correct += (predicted == labels).sum()

            accuracy = 100 * correct / total

            # Print Loss
            print('Iteration: {}. Loss: {}. Accuracy: {}'.format(iter, loss.item(), accuracy))