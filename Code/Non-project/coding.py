num_rows, num_cols = map(int, input().split())

territories = [list(map(int, input().split())) for _ in range(num_rows)]
minimum = min([min(row) for row in territories])
maximum = max([max(row) for row in territories])

# print(minimum)

states = []
for row in range(num_rows):
  for col in range(num_cols):
    if territories[row][col] == minimum:
      states.append((row, col, minimum))

loops = 2

directions = ((0, 1), (0, -1), (1, 0), (-1, 0))

ans = 0

while states:
#   input()
#   print(states)
#   print(ans)
  copied_states = states
  states = []

  for state in copied_states:
    for dRow, dCol in directions:
      new_row = state[0] + dRow
      new_col = state[1] + dCol

      if (0 <= new_row < num_rows) and (0 <= new_col < num_cols) and state[2] < territories[new_row][new_col]:
        states.append((new_row, new_col, territories[new_row][new_col]))
        if territories[new_row][new_col] == maximum:
          ans = loops

  loops += 1

print(ans)