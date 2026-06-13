def main():
    import numpy as np
    import torch

    import torch.nn as nn
    import torch.nn.functional as F
    import torch.optim as optim
    from torchvision import datasets, transforms
    import matplotlib.pyplot as plt

    from tqdm import tqdm
    
    dataloader_generator = torch.Generator()
    seed = 42
    dataloader_generator.manual_seed(seed)

    transform = transforms.Compose(
        [transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))]
    )

    batch_size = 32
    # Note that 4 seems optimal here due to simplistic data set
    # Could try with the Cifar-10 data set

    trainset = datasets.MNIST(
        root='./data', train=True, download=True, transform=transform
    )

    trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size, shuffle=True, generator=dataloader_generator, num_workers=2)

    testset = datasets.MNIST(root='./data', train=False, download=True, transform=transform)

    testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size, shuffle=False, generator=dataloader_generator, num_workers=2)
    kernal_size = 3
    # Notes about 3:
    #   - It seems to use the first ~2000 training batches to figure out how to adjust it's weights
    #   - Does not actually train until Epoch 2 for batch size 32 and epoch 3/4 for batch size 64
    #   - Tapers out at around 98.5% accuracy
    #   - Interestingly, MaxPool2d seems to improve accuracy slightly compared to AdaptiveAvgPool2d
    #   - Is it possible to find out the reason by looking at individual feature maps?
    # Notes about 5:
    #   - "Training" starts earlier compared to 3x3 (epoch 1)
    #   - Actually seems to train faster compared to 3x3
    #   - Perhaps this is acctually due to extra model params?
    #   - Tapers at 98.8% accuracy
    #   - Train acc gets 99.5%
    #   - How much of this is due to model architecture?
    # Idea: Find minimal model size that can reach 98.5% accuracy with 3x3 and 5x5

    class Model(nn.Module):
        def __init__(self, kernel_size, device):
            padding = (kernel_size - 1) // 2

            super().__init__()
            self.device = device

            self.model = nn.Sequential(
                nn.Conv2d(in_channels=1, out_channels=16, kernel_size=kernel_size, padding=padding),
                nn.ReLU(),
                nn.Conv2d(in_channels=16, out_channels=16, kernel_size=kernel_size, padding=padding),
                nn.ReLU(),
                nn.MaxPool2d(kernel_size=2, stride=2),

                nn.Conv2d(in_channels=16, out_channels=32, kernel_size=kernel_size, padding=padding),
                nn.ReLU(),
                nn.Conv2d(in_channels=32, out_channels=32, kernel_size=kernel_size, padding=padding),
                nn.ReLU(),
                nn.MaxPool2d(kernel_size=2, stride=2),

                nn.Flatten(),
                nn.Linear(in_features=7*7*32, out_features=128),
                nn.ReLU(),
                nn.Linear(in_features=128, out_features=128),
                nn.ReLU(),
                nn.Linear(in_features= 128, out_features= 10),
            )

            self.to(self.device)
        
        def forward(self, x):
            return self.model(x)

    model = Model(kernel_size=kernal_size, device=torch.device("cuda" if torch.cuda.is_available() else "cpu"))

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)

    train_losses = []
    train_accuracies = []
    val_losses = []
    val_accuracies = []
    num_epochs = 20

    for epoch in range(num_epochs):
        running_train_loss = 0.0
        running_train_correct = 0
        running_train_total = 0

        for data in tqdm(trainloader):
            inputs, labels = data
            inputs, labels = inputs.to(model.device), labels.to(model.device)

            optimizer.zero_grad()

            outputs = model(inputs)
            _, predicted = torch.max(outputs.data, 1)

            running_train_total += labels.size(0)
            running_train_correct += (predicted == labels).sum().item()

            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_train_loss += loss.item()
        train_acc = running_train_correct * 100 / running_train_total
        train_losses.append(running_train_loss / len(trainloader))
        train_accuracies.append(train_acc)

        running_test_loss = 0.0
        running_test_correct = 0
        running_test_total = 0
        for data in tqdm(testloader):
            inputs, labels = data
            inputs, labels = inputs.to(model.device), labels.to(model.device)

            outputs = model(inputs)
            _, predicted = torch.max(outputs.data, 1)
            running_test_total += labels.size(0)
            running_test_correct += (predicted == labels).sum().item()
            loss = criterion(outputs, labels)

            running_test_loss += loss.item()
        val_acc = running_test_correct * 100 / running_test_total
        val_losses.append(running_test_loss / len(testloader))
        val_accuracies.append(val_acc)

        print(f"""Epoch {epoch + 1}: 
        Train Loss: {running_train_loss / len(trainloader):.3f}, Train Acc: {train_acc:.1f}%, 
        Val Loss: {running_test_loss / len(testloader):.3f}, Val Acc: {val_acc:.1f}%""")

    plt.plot(range(num_epochs), train_accuracies, label='Train Accuracy')
    plt.plot(range(num_epochs), val_accuracies, label='Validation Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.ylim(0, 100)
    plt.yticks([y for y in range(0, 101, 10)])
    plt.savefig(f"MNIST_CNN_K{kernal_size}.png")
    plt.show()

if __name__ == "__main__":
    main()