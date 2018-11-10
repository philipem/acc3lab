import matplotlib.pyplot as plt

def plot_bars(noun_count):
    plt.figure(1)
    plt.bar(list(noun_count.keys()), noun_count.values(), color='g')
