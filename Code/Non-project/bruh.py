n = int(input())
seen = []

def is_prime(x):
  for i in range(2, x**(.5)):
    if x % i == 0:
      return False
  return True

for num in range(4, n):
  if is_prime(num):
    if n - num in seen:
      print(f"{n}={n-num}+{num}")
      break
    seen.append(num)