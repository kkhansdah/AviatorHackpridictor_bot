import matplotlib.pyplot as plt

def generate_graph(data, filename="graph.png"):
    plt.figure(figsize=(6, 3))
    plt.plot(range(1, len(data) + 1), data, marker='o', color='blue')
    plt.title("📈 Aviator Live Graph")
    plt.xlabel("Rounds")
    plt.ylabel("Multiplier")
    plt.grid(True)
    plt.savefig(filename)
    plt.close()
