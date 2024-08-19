import pandas as pd

df = pd.read_csv("./final_files/csvs/tabela_jogadores.csv")
df['Goals'] = df['Goals'].astype(int)
print(df['Goals'])