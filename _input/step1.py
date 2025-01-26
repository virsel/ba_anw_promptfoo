from pathlib import Path
import pandas as pd
import ast
import re

# get abs path of the file
abs_path = Path(__file__).resolve().parent
data_path = abs_path / 'features_labeled_4llm_vnew.csv'
data_outpath = abs_path / 'step1_vnew.csv'


def main():
    df = pd.read_csv(data_path)

    # convert string to list
    df.actual_moreoften = df.actual_moreoften.apply(ast.literal_eval)
    df.expected_moreoften = df.expected_moreoften.apply(ast.literal_eval)
    
    # clean result lists
    df.actual_moreoften = df.actual_moreoften.apply(clean_resultlists)
    df.expected_moreoften = df.expected_moreoften.apply(clean_resultlists)
    
    df.to_csv(data_outpath, index=False)
 
 
def clean_pattern(p):
    # network delay
    p = p.replace('P90(ms)', 'Delay')
    
    p = p.replace('NetworkDelay', 'NetworkDelay Alarm')
    p = p.replace('CpuUsageRate(%)', 'CpuUsageRate(%) Alarm')
    p = p.replace('MemoryUsageRate(%)', 'MemoryUsageRate(%) Alarm')
    
    # Remove anything within angle brackets
    p = re.sub(r'<[^>]*>', '', p)
    
    # Remove anything within angle brackets
    p = re.sub(r'\([^)]*\)', '', p)
    
    # Remove words followed by colons or equal
    p = re.sub(r'\w+[:=]', '', p)
    
    # Remove special characters
    p = re.sub(r'[^\w\s-]', '', p)
    
    # Reduce multiple spaces to a single space
    p = re.sub(r'\s+', ' ', p)
    
    # Strip leading and trailing whitespace
    p = p.strip()
    
    return p
    
# Create a detailed prompt
def clean_resultlists(rl):
    for ep in rl:
        if 'events' in ep:
            ep['events'] = [clean_pattern(e) for e in ep['events']]
        if 'events_inreferenz' in ep:
            ep['events_inreferenz'] = [clean_pattern(e) for e in ep['events_inreferenz']]
    
    return rl
    
    
if __name__ == '__main__':
    main()