from pathlib import Path
import pandas as pd

# get abs path of the file
abs_path = Path(__file__).resolve().parent
data_path = abs_path / 'step1_vnew.csv'
train_outpath = abs_path / 'train_vnew.csv'
test_outpath = abs_path / 'test_vnew.csv'

def main():
    df = pd.read_csv(data_path)
    
    mask = df.inject_comp_tdiff == 2
    df.drop(columns=['inject_comp_tdiff'], inplace=True)
    df_test = df[mask]
    df_train = df[~mask]
    df_train.to_csv(train_outpath, index=False)
    df_test.to_csv(test_outpath, index=False)
    
    
if __name__ == '__main__':
    main()