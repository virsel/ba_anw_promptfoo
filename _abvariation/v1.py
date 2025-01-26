from pathlib import Path
import pandas as pd
import ast
import json

# get abs path of the file
abs_path = Path(__file__).resolve().parent
data_path = abs_path / '../_input/test_v1.csv'
data_outpath = abs_path / 'test_v1old.csv'

def main():
    df = pd.read_csv(data_path)
    df_impfeat = df[['actual_moreoften', 'expected_moreoften', 'root_cause', 'metrics_of_affectedpods', 'nezha_rank_050_correct', 'abnormal_time']]
    
    # rename root cause column
    df_impfeat.rename(columns={'root_cause': 'root_cause_bynezha'}, inplace=True)
    
    # convert string to list
    df_impfeat.actual_moreoften = df_impfeat.actual_moreoften.apply(ast.literal_eval)
    df_impfeat.expected_moreoften = df_impfeat.expected_moreoften.apply(ast.literal_eval)
    df_impfeat.metrics_of_affectedpods = df_impfeat.metrics_of_affectedpods.apply(ast.literal_eval)
    
    # convert root cause to readable format
    df_impfeat['root_cause'] = df_impfeat['root_cause_bynezha'].apply(categorize_root_cause)
    
    # format expected more often
    df_impfeat.expected_moreoften = df_impfeat.expected_moreoften.apply(resultlist_2_prompt)
    
    # format actual more often
    df_impfeat.actual_moreoften = df_impfeat.actual_moreoften.apply(resultlist_2_prompt)
    
    # format metrics
    df_impfeat.metrics_of_affectedpods = df_impfeat.metrics_of_affectedpods.apply(metrics_2_prompt)
    
    df_impfeat.to_csv(data_outpath, index=False)
    
def categorize_root_cause(root_cause):
    if 'CpuUsageRate(%)' in root_cause:
        return 'cpu_usage'
    elif 'NetworkP90(ms)' in root_cause:
        return 'network_delay'
    else:
        return 'code_bug'
    
def metrics_2_prompt(metrics):
    prompt = ""
    for key, value in metrics.items():
        prompt += f"{key}: {value}\n"
    return prompt

err_indicators = ['exception', 'error', 'fail', 'failure']
    
# Create a detailed prompt
def resultlist_2_prompt(event_patterns):
    prompt = ""
    max_patterns = 5
    for idx, pattern in enumerate(event_patterns, 1):
        if max_patterns < 1:
            # event_str = ' '.join(pattern['events'])
            # if 'events_inreferenz' in pattern:
            #     event_str += ' '.join(pattern['events_inreferenz'])
            # event_str = event_str.lower()
            # if any(indicator in event_str for indicator in err_indicators):
            #     print(event_str)
            # else:
            #     continue
            continue
        # Basic pattern description
        prompt += f"Pattern on Rank {idx}:\n"
        # Score interpretation
        prompt += f"Deviation Score: {pattern['score']:.2f} = "
        if abs(pattern['score']) > 0.9:
            prompt += f"a big anomaly.\n"
        elif abs(pattern['score']) > 0.7:
            prompt += f"a moderate anomaly.\n"
        else:
            prompt += f"a minor anomaly.\n"
        
        # Depth information
        prompt += f"Event Depth: {pattern['deepth']}\n"
        
        # Pod information
        if 'pod' in pattern:
            prompt += f"Affected Pod: {pattern['pod']}\n"
        
        # Actual vs Expected Events
        prompt += f"Event Comparison:\n"
        
        if 'events' in pattern:
            prompt += f"  Event Trace Pattern in current fokused System:\n"
            prompt += f"    From: ({pattern['events'][0]})\n"
            prompt += f"    To: ({pattern['events'][1]})\n"
        
        if 'events_inreferenz' in pattern:
            prompt += f"  Event Trace Pattern appeared in referenced System:\n"
            prompt += f"    From: ({pattern['events_inreferenz'][0]})\n"
            prompt += f"    To: ({pattern['events_inreferenz'][1]})\n"
        
        prompt += f"\n"

        max_patterns -= 1
    
    return prompt
    
    
if __name__ == '__main__':
    main()