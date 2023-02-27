import random

# Define the parameters of the model
n_hours = 24
inventory = 1000
elasticity = 0.2
n_iter = 1000
gamma = 0.9
alpha = 0.1
epsilon = 0.1

# Define the initial prices for each hour
prices = [20] * n_hours

# Define the Q table
Q = [[0 for j in range(2)] for i in range(n_hours)]

# Define the objective function to maximize
def objective(prices):
    demand = [100 - p * elasticity for p in prices]
    total_demand = sum(demand)
    sales = min(total_demand, inventory)
    purchases = max(0, total_demand - inventory)
    selling_prices = [p + 1 for p in prices]
    buying_prices = [p - 1 for p in prices]
    profit = sum([(s - p) * (sales - purchases) for s, p in zip(selling_prices, buying_prices)])
    return profit

# Iterate over the specified number of iterations
for i in range(n_iter):
    # Choose an initial hour randomly
    hour = random.randint(0, n_hours - 1)

    # Choose an action according to the epsilon-greedy policy
    if random.uniform(0, 1) < epsilon:
        action = random.randint(0, 1)
    else:
        action = Q[hour].index(max(Q[hour]))

    # Calculate the demand for the chosen hour and action
    price = prices[hour] + (2 * action - 1) * 1
    demand = 100 - price * elasticity

    # Calculate the total demand for the day
    total_demand = sum([100 - p * elasticity for p in prices])

    # Calculate the sales and purchases
    sales = min(total_demand, inventory)
    purchases = max(0, total_demand - inventory)

    # Calculate the reward
    reward = (sales - purchases) * (price - 19)

    # Update the Q table
    new_action = Q[hour].index(max(Q[hour]))
    Q[hour][action] += alpha * (reward + gamma * Q[hour][new_action] - Q[hour][action])

    # Update the prices
    prices[hour] = price

# Print the optimal prices
print(prices)
print(total_demand)
