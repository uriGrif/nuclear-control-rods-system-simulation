import matplotlib.pyplot as plt
import time

def run_graficador(q):
    plt.ion()
    fig, ax = plt.subplots()
    error_history = []

    while True:
        while not q.empty():
            error = q.get()
            error_history.append(error)
            if len(error_history) > 500:
                error_history.pop(0)

        ax.clear()
        ax.plot(error_history, label="Error")
        ax.axhline(0, color="gray", linestyle="--")
        ax.set_ylim(-1000, 1000)
        ax.legend()
        plt.pause(0.1)
        time.sleep(0.1)
