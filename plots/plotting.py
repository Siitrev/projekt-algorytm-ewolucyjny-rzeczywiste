import matplotlib.pyplot as plt
from database.DbController import DbController

def plot_column(db_object : DbController, choice : int):
    if choice == 1:
        ypoints = db_object.get_column('najlepszy')
        # print(ypoints)
        length = len(ypoints)
        xpoints = [i for i in range(1, length + 1)]  # liczba epok = liczba najlepszych

        plt.plot(xpoints, ypoints)
        plt.title("Best specimes throught epochs")
        plt.savefig(fname="plots/best_graph.png")
        

    if choice == 2:
        ypoints = db_object.get_column('srednia_populacji')
        # print(ypoints)
        length = len(ypoints)
        xpoints = [i for i in range(1, length + 1)]

        plt.plot(xpoints, ypoints)
        plt.title("Average of values throught epochs")
        plt.savefig(fname="plots/avg_graph.png")

    if choice == 3:
        ypoints = db_object.get_column('odchylenie_standardowe_populacji')
        # print(ypoints)
        length = len(ypoints)
        xpoints = [i for i in range(1, length + 1)]

        plt.plot(xpoints, ypoints)
        plt.title("Standard deviation of values throught epochs")
        plt.savefig(fname="plots/std_graph.png")
    
    plt.clf()