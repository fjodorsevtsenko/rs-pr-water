from torch import nn

class MultiOutputNetv1(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(11, 50)
        self.relu1 = nn.ReLU()
        self.fc2 = nn.Linear(50, 100)
        self.relu2 = nn.ReLU()
        self.fc3 = nn.Linear(100, 50)
        self.relu3 = nn.ReLU()
        self.fc4 = nn.Linear(50, 11)  # Output layer with 11 neurons

    def forward(self, x):
        x = self.relu1(self.fc1(x))
        x = self.relu2(self.fc2(x))
        x = self.relu3(self.fc3(x))
        x = self.fc4(x)
        return x