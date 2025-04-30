import numpy as np
import matplotlib.pyplot as plt

# A: rows
# B: columns
# Number of strategies for each player
n_strat_A = 2
n_strat_B = 2

# Random payoff matrices for each player
A = np.random.randn(n_strat_A, n_strat_B)
B = np.random.randn(n_strat_A, n_strat_B)

print(A)
print(B)

def best_response(payoff_matrix, axis):
    best = np.zeros(payoff_matrix.shape, dtype=bool)
    if axis == 0:
        for i in range(payoff_matrix.shape[0]):
            row = payoff_matrix[i, :]
            max_val = row.max()
            best[i, :] = row == max_val
    else:
        for j in range(payoff_matrix.shape[1]):
            col = payoff_matrix[:, j]
            max_val = col.max()
            best[:, j] = col == max_val
    return best

best_response_P1 = best_response(A, axis=0)
best_response_P2 = best_response(B, axis=1)
print("The best response for Player 1 is", best_response_P1)
print("The best response for Player 2 is", best_response_P2)

# Nash Equilibrium
nash_eqs = []
for i in range(A.shape[0]):
    for j in range(A.shape[1]):
        # Check if (i,j) is a best response for both players
        if best_response_P1[i, j] and best_response_P2[i, j]:
            nash_eqs.append((i, j))

if nash_eqs:
    for eq in nash_eqs:
        print(f"Nash Equilibrium: Player 1 = {eq[0]}, Player 2 = {eq[1]}")
else:
    print("There's no Nash Equilibrium")


# Plot Nash Equilibrium

# Strategy grid
plt.figure(figsize=(5, 5))
plt.xlim(-0.5, A.shape[1] - 0.5)
plt.ylim(-0.5, A.shape[0] - 0.5)
plt.xticks(range(A.shape[1]), [f"B{j}" for j in range(A.shape[1])])
plt.yticks(range(A.shape[0]), [f"A{i}" for i in range(A.shape[0])])
plt.grid(True)

# Plot Nash Equilibria as purple dots
for eq in nash_eqs:
    plt.scatter(eq[1], eq[0], color='purple', s=100)
    plt.text(eq[1], eq[0], '★', color='purple', ha='center', va='center', fontsize=18)

plt.title("Nash Equilibria")
plt.xlabel("Player B Strategies")
plt.ylabel("Player A Strategies")
plt.gca().invert_yaxis()
plt.show()


# Pareto efficiency (no player can be made better off without making another worse off)
# Check which strategy combinations are Pareto efficient

def is_pareto_efficient(A, B):
    rows, col = A.shape
    pareto = np.zeros((rows,col), dtype=bool)
    for i in range(rows):
        for j in range(col):
            efficient = True
            for i2 in range(rows):
                for j2 in range(col):
                    if (A[i2, j2] >= A[i, j] and B[i2, j2] >= B[i, j]) and \
                       (A[i2, j2] > A[i, j] or B[i2, j2] > B[i, j]):
                        efficient = False
                        break
                if not efficient:
                    break
            if efficient:
                pareto[i, j] = True
    return pareto

pareto = is_pareto_efficient(A,B)
print("Pareto Efficient Outcomes:")
found = False
for i in range(A.shape[0]):  # Player A strategies
    for j in range(A.shape[1]):  # Player B strategies
        if pareto[i, j]:
            print(f"A strategy {i}, B strategy {j} -> Payoffs (A: {A[i,j]:.2f}, B: {B[i,j]:.2f})")
            found = True
if not found:
    print("No Pareto efficient outcomes found.")


# Check if each game is zero-sum (one player's gain is exactly the other player's loss)

if np.allclose(A + B, 0):
    print("The game is zero-sum.")
else:
    print("The game is not zero-sum.")
