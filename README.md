# acc3lab
Cloud computing lab3 

## notes:

 - This project is written in Python 3.6.
 - Plot bars is not implemented here but it works and only needs the following in the main function to produce the plot               locally: 
 - Just create a Data folder in the working directory where you add the files you want to use.
 - The requirements file is bigger than it needs to be. Just a heads up!
 
 ```python
 def main(file_path): 
    df, rows = read_to_df(file_path)
    # print(df)

    tot_count, dict_of_rowcount = count_pronouns(df, pronouns, row_dict)
    print('Number of pronouns: ', tot_count)

    plot_bars(tot_count, rows)
    plt.show()
```
