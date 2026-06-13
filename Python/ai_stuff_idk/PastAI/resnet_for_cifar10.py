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
        [transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]
    )

    batch_size = 128

    transform_norm = transforms.Compose(
        [transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]
    )

    transform_horizontal_flip = transforms.Compose(
        [transforms.RandomHorizontalFlip(1), transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]
    )

    transform_vertical_flip = transforms.Compose(
        [transforms.RandomVerticalFlip(1), transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]
    )

    transform_random_rotation = transforms.Compose(
        [transforms.RandomRotation(30), transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]
    )

    transform_rr_hflip = transforms.Compose(
        [transforms.RandomRotation(30), transforms.RandomHorizontalFlip(1), transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]
    )

    transform_rr_vflip = transforms.Compose(
        [transforms.RandomRotation(30), transforms.RandomVerticalFlip(1), transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]
    )

    transform_vhflip = transforms.Compose(
        [transforms.RandomVerticalFlip(1), transforms.RandomHorizontalFlip(1), transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]
    )

    batch_size = 64

    trainset_norm = datasets.CIFAR10(
        root='./data', train=True, download=True, transform=transform_norm
    )

    trainset_hflip = datasets.CIFAR10(
        root='./data', train=True, download=True, transform=transform_horizontal_flip
    )

    trainset_vflip = datasets.CIFAR10(
        root='./data', train=True, download=True, transform=transform_vertical_flip
    )

    trainset_rflip = datasets.CIFAR10(
        root='./data', train=True, download=True, transform=transform_random_rotation
    )

    trainset_rr_hflip = datasets.CIFAR10(
        root='./data', train=True, download=True, transform=transform_rr_hflip
    )

    trainset_rr_vflip = datasets.CIFAR10(
        root='./data', train=True, download=True, transform=transform_rr_vflip
    )

    trainset_vhflip = datasets.CIFAR10(
        root='./data', train=True, download=True, transform=transform_vhflip
    )

    trainset = torch.utils.data.ConcatDataset([trainset_norm, trainset_hflip, trainset_vflip, trainset_rflip, trainset_rr_hflip, trainset_rr_vflip, trainset_vhflip])

    trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size, shuffle=True, generator=dataloader_generator, num_workers=4)

    testset = datasets.CIFAR10(root='./data', train=False, download=True, transform=transform)

    testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size, shuffle=False, generator=dataloader_generator, num_workers=4)

    kernal_size = 3
    padding = kernal_size // 2

    class ResNet(nn.Module):
        def __init__(self, num_resBlocks, num_hidden, kernal_size, padding, device):
            super().__init__()

            self.device = device
            self.startBlock = nn.Sequential(
                nn.Conv2d(in_channels= 3, out_channels= num_hidden, kernel_size= kernal_size, padding= padding),
                nn.BatchNorm2d(num_hidden),
                nn.ReLU()
            )

            self.backBone = nn.ModuleList(
                [ResBlock(num_hidden) for i in range(num_resBlocks)]
            )

            self.end_layer = nn.Sequential(
                nn.Conv2d(in_channels= num_hidden, out_channels= 32, kernel_size = kernal_size, padding= padding),
                nn.BatchNorm2d(32),
                nn.ReLU(),
                nn.Flatten(),
                nn.Linear(in_features= 32*32*32, out_features= 10)
            )

            self.to(device)

        def forward(self, x):
            x = self.startBlock(x)
            for resBlock in self.backBone:
                x = resBlock(x)
            
            return self.end_layer(x)

    class ResBlock(nn.Module):
        def __init__(self, num_hidden):
            super().__init__()
            self.conv1 = nn.Conv2d(in_channels= num_hidden, out_channels= num_hidden, kernel_size = 3, padding= 1)
            self.bn1 = nn.BatchNorm2d(num_hidden)
            self.conv2 = nn.Conv2d(in_channels= num_hidden, out_channels= num_hidden, kernel_size = 3, padding= 1)
            self.bn2 = nn.BatchNorm2d(num_hidden)

        def forward(self, x):
            residual = x
            x = F.relu(self.bn1(self.conv1(x)))
            x = self.bn2(self.conv2(x))
            x += residual
            x = F.relu(x)
            return x


    model = ResNet(num_resBlocks= 6, num_hidden= 64, kernal_size= kernal_size, padding= padding, device= torch.device("cuda"))

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)

    train_losses = []
    train_accuracies = []
    val_losses = []
    val_accuracies = []
    num_epochs = 100

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
    plt.savefig(f"CIFAR10_RESNET_K{kernal_size}.png")
    plt.show()

if __name__ == "__main__":
    main()