from pathlib import Path
import pandas as pd
import ast

# get abs path of the file
abs_path = Path(__file__).resolve().parent
data_path = abs_path / 'train_v1.csv'
data_outpath = abs_path / 'train_v1_sampled.csv'

def main():
    df = pd.read_csv(data_path)
    df = df.iloc[:10, :]
    df.to_csv(data_outpath, index=False)
  
    
if __name__ == '__main__':
    main()