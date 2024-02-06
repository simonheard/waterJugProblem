# import the priority queue module
import heapq
import math

# we store the state as a tuple of the volumn of each jug

# define heuristic function
# We define this function base on the minimal number of steps to reach the target volumn
def heu(largest_jug, current_state, target):
  return abs((sum(current_state) - target) / largest_jug)

# define gcd function of list of numbers
def gcd(a):
  result = a[0]
  for i in a[1:]:
    result = gcd2(result, i)
  return result

# define gcd function of two numbers
def gcd2(a, b):
  while b:
    a, b = b, a % b
  return a

# define the function to go to next state
def get_next_states(current, capacities):
  states = []
  for i in range(len(current) - 1):
    # we have four possible actions: fill, empty, fill infinite jug, and pour
    # fill the i-th jug
    new_state = list(current)
    new_state[i] = capacities[i]
    states.append((tuple(new_state)))

    # empty the i-th jug
    new_state = list(current)
    new_state[i] = 0
    states.append((tuple(new_state)))

    # pour from the i-th jug to the infinte jug
    new_state = list(current)
    new_state[-1] += current[i]
    new_state[i] = 0
    states.append((tuple(new_state)))

    # pour from the i-th jug to the j-th jug
    for j in range(len(current)-1):
      if i != j:
        amount = min(current[i], capacities[j] - current[j])
        new_state = list(current)
        new_state[i] -= amount
        new_state[j] += amount
        states.append((tuple(new_state)))
  return set(states) # remove duplicates

# define the function to solve the problem, using A* search
def astar(capacities, target):
  # Check solvable base on the modulo of target by the gcd of the volumn of each jug
  # This is based on the mathematical property of the water jug problem
  # This will help to reduce the search space
  cgcd = gcd(capacities)
  if target % cgcd != 0:
    return None
  
  largest_jug = max(capacities)

  open_set = []
  # store the cost, state, and path. In this problem, we simply treat the cost as 1 for each step
  heapq.heappush(open_set, (0, tuple([0] * (len(capacities) + 1)), []))
  closed_set = set()

  while open_set:
    cost, current, path = heapq.heappop(open_set)
    # if the infinte jug is the target, return the path
    if current[-1] == target:
      return path+[current]
    
    # if the infinite jug filled more than the target, continue
    if current[-1] > target:
      continue

    # if the difference between the infinite jug and the target mod gcd is not 0, continue
    if (target - current[-1]) % cgcd != 0:
      continue

    # if the current state is not the target state, expand the current state
    if current in closed_set:
      continue
    closed_set.add(current)

    for next_state in get_next_states(current, capacities):
      if next_state not in closed_set:
        total_cost = cost + 1 + heu(largest_jug, next_state, target)
        heapq.heappush(open_set, (total_cost, next_state, path + [current]))

    # if the open_set is empty, meaning no solution found, return None
  return None