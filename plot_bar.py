import matplotlib.pyplot as plt

def plot_bars(noun_count, rows):
    plt.figure(1)
    
    factor = 1/rows 
    
    for i in noun_count.keys():
        noun_count[i] = noun_count[i]*factor
        
    plt.bar(list(noun_count.keys()), noun_count.values(), color='g')
