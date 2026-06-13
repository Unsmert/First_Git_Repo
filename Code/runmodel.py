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

