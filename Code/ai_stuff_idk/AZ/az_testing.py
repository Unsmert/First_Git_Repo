import numpy as np
import math
import time
import random
import matplotlib.pyplot as plt

print(np.__version__)

import torch
print(torch.__version__)
print(torch.version.cuda)
print(torch.cuda.is_available())

import torch.nn as nn
import torch.nn.functional as F

from tqdm import trange

torch.manual_seed(42)

class bcolors:
    RED = '\033[31m'
    YELLOW = '\033[33m'
    END = '\033[0m'

class TicTacToe:
    def __init__(self):
        # Pretty much just defining board size
        self.row_count = 3
        self.column_count = 3
        self.action_size = self.row_count * self.column_count

    def __repr__(self):
        return "TicTacToe"

    def get_initial_state(self):
        # Just the default board state, np.zero implement to make it easier to train model
        return np.zeros([self.row_count, self.column_count])

    def get_next_state(self, state, action, player):
        # Just returns the state after taking some action
        row = action // self.column_count
        column = action % self.row_count
        state[row, column] = player
        return state

    def get_valid_moves(self, state):
        # Flatten the state, returns where the action is possible as 1 and where it isn't as 0
        return (state.reshape(-1) == 0).astype(np.uint8)

    def check_win(self, state, action):
        # First case: if the previous action is None (root node)
        if action == None:
            return False
        # Obtains the player information
        row = action // self.column_count
        column = action % self.row_count
        player = state[row, column]

        # Logic intuition: since player is a specific number, if you sum the rows and columns
        # when there is 2 players, the sum is equal to the player * row/column count
        # same for the diagonals
        return (
            np.sum(state[row, :]) == player * self.column_count
            or np.sum(state[:, column]) == player * self.row_count
            or np.sum(np.diag(state)) == player * self.row_count
            or np.sum(np.diag(np.flip(state, axis = 0))) == player * self.row_count
        )

    def get_value_and_terminated(self, state, action):
        # Returns the value of the state and whether the game ended or not
        if self.check_win(state, action):
            return 1, True
        if np.sum(self.get_valid_moves(state)) == 0:
            return 0, True
        return 0, False

    def get_opponent(self, player):
        # Flips the player
        return -player

    def get_opponent_value(self, value):
        # Flips the value, for backpropagation
        return -value

    def change_perspective(self, state, player):
        # If player is -1, look at it from the opposite angle
        "Doesn't this cause problems since you are already looking at it from their perspective?"
        return state * player

    def get_encoded_state(self, state):
        # Converting the state of the game into 3 layers (player1, empty, player2)
        # This is for resNet architecture
        encoded_state = np.stack(
            (state == -1, state == 0, state == 1)
        ).astype(np.float32)

        # if len(state.shape) == 3:
        #     encoded_state = np.swapaxes(encoded_state, 0, 1)
        return encoded_state

class ConnectFour:
    def __init__(self):
        # Pretty much just defining board size
        self.row_count = 6
        self.column_count = 7
        self.action_size = self.column_count
        self.in_a_row = 4

    def __repr__(self):
        return "ConnectFour"

    def get_initial_state(self):
        # Just the default board state, np.zero implement to make it easier to train model
        return np.zeros([self.row_count, self.column_count])

    def get_next_state(self, state, action, player):
        row = np.max(np.where(state[:, action] == 0))
        state[row, action] = player
        return state

    def get_valid_moves(self, state):
        # Flatten the state, returns where the action is possible as 1 and where it isn't as 0
        return (state[0] == 0).astype(np.uint8)

    def check_win(self, state, action):
        # First case: if the previous action is None (root node)
        if action == None:
            return False
        # Obtains the player information

        row = np.min(np.where(state[:, action] != 0))
        column = action
        player = state[row, column]

        def count(offset_row, offset_col):
            for i in range(1, self.in_a_row):
                r = row + offset_row * i
                c = column + offset_col * i
                if (r < 0 
                    or r >= self.row_count 
                    or c < 0 
                    or c >= self.column_count 
                    or state[r, c] != player
                ):
                    return i - 1
            
            return self.in_a_row - 1
        
        return (
            count(1, 0) >= self.in_a_row - 1
            or count(0, 1) + count(0, -1) >= self.in_a_row - 1
            or count(1, 1) + count(-1, -1) >= self.in_a_row - 1
            or count(1, -1) + count(-1, 1) >= self.in_a_row - 1
        )

    def get_value_and_terminated(self, state, action):
        # Returns the value of the state and whether the game ended or not
        if self.check_win(state, action):
            return 1, True
        if np.sum(self.get_valid_moves(state)) == 0:
            return 0, True
        return 0, False

    def get_opponent(self, player):
        # Flips the player
        return -player

    def get_opponent_value(self, value):
        # Flips the value, for backpropagation
        return -value

    def change_perspective(self, state, player):
        # If player is -1, look at it from the opposite angle
        "Doesn't this cause problems since you are already looking at it from their perspective?"
        return state * player

    def get_encoded_state(self, state):
        # Converting the state of the game into 3 layers (player1, empty, player2)
        # This is for resNet architecture
        encoded_state = np.stack(
            (state == -1, state == 0, state == 1)
        ).astype(np.float32)

        # if len(state.shape) == 3:
        #     encoded_state = np.swapaxes(encoded_state, 0, 1)
        return encoded_state

class ResNet(nn.Module):
    def __init__(self, game, num_resBlocks, num_hidden, device):
        super().__init__()

        self.device = device
        self.startBlock = nn.Sequential(
            nn.Conv2d(in_channels= 3, out_channels= num_hidden, kernel_size= 3, padding= 1),
            nn.BatchNorm2d(num_hidden),
            nn.ReLU()
        )

        self.backBone = nn.ModuleList(
            [ResBlock(num_hidden) for i in range(num_resBlocks)]
        )

        self.policyHead = nn.Sequential(
            nn.Conv2d(in_channels= num_hidden, out_channels= 32, kernel_size = 3, padding= 1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(32 * game.row_count * game.column_count, game.action_size)
        )

        self.valueHead = nn.Sequential(
            nn.Conv2d(in_channels= num_hidden, out_channels= 3, kernel_size = 3, padding= 1),
            nn.BatchNorm2d(3),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(3 * game.row_count * game.column_count, 1),
            nn.Tanh()
        )

        self.to(device)

    def forward(self, x):
        x = self.startBlock(x)
        for resBlock in self.backBone:
            x = resBlock(x)

        policy = self.policyHead(x)
        value = self.valueHead(x)
        return policy, value

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

class Node:
  def __init__(self, game, args, state, parent=None, action_taken = None, prior= 0, visit_count= 0):
    # Defines the key args (game necessary, args for mcts necessary)
    # State for evaluation, parent because tree search, action taken to track nodes
    self.game = game
    self.args = args
    self.state = state
    self.parent = parent
    self.action_taken = action_taken
    self.prior = prior

    # List of the children
    # Seems like children are added here after each search iteration
    self.children = []

    self.visit_count = visit_count
    self.value_sum = 0

  def is_fully_expanded(self):
    # Returns whether the node is fully expanded or not
    # Note: does not consider terminal nodes fully expanded nodes.
    return len(self.children) > 0

  def select(self):
    # Initializes the best child and ucb as a variable to track
    best_child = None
    best_ucb = -np.inf

    # Loops through self.children to find the best child/ucb
    for child in self.children:
      ucb = self.get_ucb(child)
      if ucb > best_ucb:
        best_child = child
        best_ucb = ucb
    return best_child

  def get_ucb(self, child):
    q_value = 0
    if child.visit_count > 0:
        q_value = 1 - ((child.value_sum / child.visit_count + 1) / 2)

    return q_value + self.args['C'] * (math.sqrt(self.visit_count) / (child.visit_count + 1)) * child.prior

  def expand(self, policy):
    for action, prob in enumerate(policy):
      if prob > 0:
        # Initializes the child_state for expansion (state after taking random expansion action)
        child_state = self.state.copy()
        child_state = self.game.get_next_state(child_state, action, 1)
        child_state = self.game.change_perspective(child_state, player=-1)

        # Creates a connected node with the below parameters
        child = Node(self.game, self.args, child_state, self, action, prob)

        # Adds it to the list of children
        self.children.append(child)

  def backpropagate(self, value):
    # This is the backpropagation step for MCTS
    # Pretty simple recursion, first adds the value/visit count
    self.value_sum += value
    self.visit_count += 1

    # Flips the value when backpropagating
    value = self.game.get_opponent_value(value)

    # Only propagate further if the node is not the root node
    if self.parent != None:
      # Note: the value is not added to parent here because it would be added through the function
      self.parent.backpropagate(value)

# Note: This MCTS does not take advantage of importing the tree search results from the previous search
class Alpha_MCTS:
    # Importing the game as well as the MCTS args (likely updated per type of game)
    def __init__(self, game, args, model):
        self.game = game
        self.args = args
        self.model = model

    @torch.no_grad()
    # Actually runs the MCTS here
    def search(self, state):
        # Makes a new root node with the current state
        root = Node(self.game, self.args, state, visit_count= 1)

        policy, _ = self.model(
            torch.tensor(self.game.get_encoded_state(state), device= self.model.device).unsqueeze(0)
        )
        policy = torch.softmax(policy, axis=1).squeeze(0).cpu().numpy()

        # Introduces noise to the model
        # Reason: When we initialize the model and it doesn't know much, 
        # we should encourage exploration
        policy = (1 - self.args['dirichlet_epsilon']) * policy + self.args['dirichlet_epsilon'] * np.random.dirichlet([self.args['dirichlet_alpha']] * self.game.action_size)
        
        valid_moves = self.game.get_valid_moves(state)
        policy *= valid_moves
        policy /= np.sum(policy)

        root.expand(policy)

        # Preforms the MCTS steps the amount of times specified by the arg below
        for _ in range(self.args['num_searches']):
            # This resets the node to the root for each step
            node = root

            # Preparation for the MCTS expansion step
            # If the node is fully expanded, select the best child
            # Once again, note terminal nodes aren't considered fully expanded
            while node.is_fully_expanded():
                node = node.select()

            # Obtain the value + whether the game ended
            value, is_terminal = self.game.get_value_and_terminated(node.state, node.action_taken)
            value = self.game.get_opponent_value(value)

            # Note: can only expand if the node isn't terminal
            # The actual MCTS expansion, importantly allows for selection of terminal Nodes
            if not is_terminal:
                policy, value = self.model(
                    torch.tensor(self.game.get_encoded_state(node.state), device = self.model.device).unsqueeze(0)
                )

                value = value.item()
                policy = torch.softmax(policy, axis= 1).squeeze(0).cpu().numpy()
                valid_moves = self.game.get_valid_moves(node.state)
                policy *= valid_moves
                policy /= np.sum(policy)

                node.expand(policy)

            # Backpropagation step
            # The value backpropagated should be flipped for consistency with perspective
            node.backpropagate(value)

        action_probs = np.zeros(self.game.action_size)

        for child in root.children:
            action_probs[child.action_taken] = child.visit_count
        action_probs /= np.sum(action_probs)
        return action_probs

class AlphaZero:
    def __init__(self, model, optimizer, game, args):
        self.model = model
        self.optimizer = optimizer
        self.game = game
        self.args = args
        self.mcts = Alpha_MCTS(game, args, model)

    def update_args(self, args):
        self.args = args

    def selfPlay(self):
        # Stores the selfplay games, initializes the player as player 1 to start, intializes the start board
        memory = []
        player = 1
        state = self.game.get_initial_state()

        while True:
            # First switches the state perspective to the player
            neutral_state = self.game.change_perspective(state, player)
            # Run the current alpha mcts implement on it, returns the visit count distribution
            action_probs = self.mcts.search(neutral_state)

            # Store the state as a tuple with the state perspective, prob distribution, and player
            "Confirmation: Are you actually supposed to use neutral state here as opposed to regular state? "
            # Ans: Yes, because the model is trained to predict from the neutral perspective

            memory.append((neutral_state, action_probs, player))
            # Pick a random choice based on action prob distribution

            temperature_action_probs = action_probs ** (1 / self.args['temperature'])
            temperature_action_probs /= np.sum(temperature_action_probs)
            action = np.random.choice(self.game.action_size, p= temperature_action_probs)

            # Go to next state
            state = self.game.get_next_state(state, action, player)
            value, is_terminal = self.game.get_value_and_terminated(state, action)

            # If the game has terminated:
            if is_terminal:
                # Store all states from the self-play games
                returnMemory = []

                # For each element in the tuples stored in memory:
                for hist_neutral_state, hist_action_probs, hist_player in memory:
                # Flip the outcome value every other node starting from terminal
                    hist_outcome = value if hist_player == player else self.game.get_opponent_value(value)
                    returnMemory.append((
                        self.game.get_encoded_state(hist_neutral_state),
                        hist_action_probs,
                        hist_outcome
                    ))

                return returnMemory

            player = self.game.get_opponent(player)

    def train(self, memory):
        random.shuffle(memory)
        for batchIdx in range(0, len(memory), self.args['batch_size']):
            sample = memory[batchIdx:min(len(memory) - 1, batchIdx + self.args['batch_size'])]
            state, policy_targets, value_targets = zip(*sample)

            state, policy_targets, value_targets = np.array(state), np.array(policy_targets), np.array(value_targets).reshape(-1, 1)

            state = torch.tensor(state, dtype = torch.float32, device = self.model.device)
            policy_targets = torch.tensor(policy_targets, dtype = torch.float32, device = self.model.device)
            value_targets = torch.tensor(value_targets, dtype = torch.float32, device = self.model.device)

            predicted_policy, predicted_value = self.model(state)

            # policy_loss = -torch.mean(torch.sum(policy_targets * predicted_policy_logsoftmax, dim=1))
            # policy_loss = F.cross_entropy(predicted_policy, torch.argmax(policy_targets, dim=1))
            # policy_loss = F.kl_div(predicted_policy_logsoftmax, policy_targets, reduction='batchmean')

            policy_loss = F.cross_entropy(predicted_policy, policy_targets)
            value_loss = F.mse_loss(predicted_value, value_targets)
            loss = policy_loss + value_loss

            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

    def learn(self):
        start_time = time.time()
        total_memory = []
        for iteration in range(1, self.args['num_iterations'] + 1):
            memory = []
            print(f"Iteration {iteration} started")
            start_time = time.time()

            self.model.eval()
            selfplay_start_time = time.time()

            # Amount of selplay games you want to add per iteration
            for _ in trange(1, self.args['num_selfPlay_iterations'] + 1):
                memory += self.selfPlay()
            print(f"Self_play states added: {len(memory)}")

            total_memory += memory
            if len(total_memory) > self.args['num_state_storage']:
                total_memory = total_memory[-self.args['num_state_storage']:]

            seconds_taken =  time.time() - selfplay_start_time
            print(f"Self_play completed: {int(seconds_taken // 60)}:{(seconds_taken%60):0.2f}")

            self.model.train()
            training_start_time = time.time()
            # Number of epochs per training session
            for _ in trange(self.args['num_epochs']): 
                self.train(total_memory)
            seconds_taken = time.time() - training_start_time
            print(f"Training completed: {int(seconds_taken // 60)}:{(seconds_taken%60):0.2f}")

            torch.save(self.model.state_dict(), f"model_{iteration}_{self.game}.pt")
            torch.save(self.optimizer.state_dict(), f"optimizer_{iteration}_{self.game}.pt")
            seconds_taken = time.time() - start_time
            print(f"Iteration {iteration} completed: {int(seconds_taken // 60)}:{(seconds_taken%60):0.2f}\n")
        seconds_taken = time.time() - start_time
        print(f"Total time taken: {int(seconds_taken // 60)}:{(seconds_taken%60):0.2f}")

game = ConnectFour()

model_args = {
    'TicTacToe': (TicTacToe(), 4, 64, torch.device("cpu")),
    'ConnectFour': (ConnectFour(), 9, 128, torch.device("cuda" if torch.cuda.is_available() else "cpu"))
}

if type(game) == TicTacToe:
    args = {
        'C': 2,
        'num_searches': 30,
        'num_iterations': 6,
        'num_selfPlay_iterations': 500,
        'num_parallel_games': 10,
        'num_epochs': 6,
        'batch_size': 128,
        'temperature': 1,
        'dirichlet_epsilon': 0.25,
        'dirichlet_alpha': 0.8
    }

    args['num_state_storage'] = args['num_selfPlay_iterations'] * game.row_count * game.column_count * 2

    device = torch.device("cpu")

    model = ResNet(*model_args['TicTacToe'])
    # model.load_state_dict(torch.load("model_6.pt"))

    optimizer = torch.optim.Adam(model.parameters(), lr= 0.001, weight_decay = 0.0001)

    alphaZ = AlphaZero(model, optimizer, game, args)

    # alphaZ.learn()

    state = game.get_initial_state()
    state = game.get_next_state(state, 2, 1)
    state = game.get_next_state(state, 1, -1)
    state = game.get_next_state(state, 6, 1)
    state = game.get_next_state(state, 7, -1)
    # 0, -1, 1
    # 0, 0, 0
    # 1, -1, 0

    print(state)

    encoded_state = game.get_encoded_state(state)

    print(encoded_state)

    tensor_state = torch.tensor(encoded_state).unsqueeze(0).to(device)

    model = alphaZ.model
    model.load_state_dict(torch.load(f"model_p_6_{game}.pt"))

    model.eval()
    policy, value = model(tensor_state)
    value = value.item()
    policy = torch.softmax(policy, axis = 1).squeeze(0).detach().cpu().numpy()

    print(value, policy)

    # plt.bar(range(game.action_size), policy)
    # plt.show()

if type(game) == ConnectFour:
    args = {
            'C': 2,
            'num_searches': 100,
            'num_iterations': 1,
            'num_selfPlay_iterations': 500,
            'num_parallel_games': 10,
            'num_epochs': 6,
            'batch_size': 256,
            'temperature': 1,
            'dirichlet_epsilon': 0.25,
            'dirichlet_alpha': 0.8
        }
    
    args['num_state_storage'] = args['num_selfPlay_iterations'] * game.row_count * game.column_count * 2

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = ResNet(*model_args['ConnectFour'])
    # model.load_state_dict(torch.load(f"model_6_{game}.pt"))

    optimizer = torch.optim.Adam(model.parameters(), lr= 0.001, weight_decay = 0.0001)

    alphaZ = AlphaZero(model, optimizer, game, args)

    # alphaZ.learn()

def pretty_print_board(board):
    list_pieces = ["*", bcolors.YELLOW + "O" + bcolors.END, bcolors.RED + "O" + bcolors.END]
    for row in board:
        print("[", end = " ")
        for element in row:
            print(list_pieces[int(element)], end = " ")
        print("]")

player = 1

model = ResNet(*model_args[game.__repr__()])
model.load_state_dict(torch.load(f"model_p_8_{game}.pt"))
model.eval()

mcts = Alpha_MCTS(game, args, model)

state = game.get_initial_state()

while True:
    pretty_print_board(state)
    if player == 1:
        valid_moves = game.get_valid_moves(state)
        print("valid moves", [i + 1 for i in range(game.action_size) if valid_moves[i] == 1])
        try:
            action = int(input(f"{player}: "))
            if not (0 < action < 8):
                print("invalid move")
                continue
            action -= 1
        except:
            print("Input an integer")
            continue
        if valid_moves[action] == 0:
            print("action not valid")
            continue
    else:
        neutral_state = game.change_perspective(state, player)
        mcts_probs = mcts.search(neutral_state)
        action = np.argmax(mcts_probs)
        print(f"-1: {action + 1}")

    state = game.get_next_state(state, action, player)

    value, is_terminal = game.get_value_and_terminated(state, action)

    if is_terminal:
        pretty_print_board(state)
        if value == 1:
            print(player, "won")
        else:
            print("draw")
        break

    player = game.get_opponent(player)