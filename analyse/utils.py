import json
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns

def load_promptfoo_results(file_path):
    """
    Load promptfoo results from a JSON file.
    
    Args:
        file_path (str): Path to the JSON file
    
    Returns:
        list: List of test results
    """
    with open(file_path, 'r') as f:
        results = json.load(f)
    return results.get('results', []).get('results', [])

def extract_results_from_json(results):
    """
    Extract ground truth and predicted labels from promptfoo results.
    
    Args:
        results (list): List of test results from promptfoo
    
    Returns:
        tuple: (y_true, y_pred) lists of ground truth and predicted labels
    """
    y_true = []
    y_pred = []
    
    for result in results:
        # Assuming the ground truth is in 'testCase.vars.root_cause'
        # and the prediction is in 'response.output'
        true_label = result.get('testCase', {}).get('vars', {}).get('root_cause')
        pred_label = result.get('response', {}).get('output')
        
        if true_label and pred_label:
            y_true.append(true_label)
            y_pred.append(pred_label)
    
    return y_true, y_pred

def generate_classification_metrics(y_true, y_pred):
    """
    Generate classification metrics.
    
    Args:
        y_true (list): Ground truth labels
        y_pred (list): Predicted labels
    
    Returns:
        dict: Classification metrics
    """
    metrics = {
        'accuracy': accuracy_score(y_true, y_pred),
        'confusion_matrix': confusion_matrix(y_true, y_pred).tolist(),
        'classification_report': classification_report(y_true, y_pred, output_dict=True)
    }
    return metrics

def analyze_promptfoo_results(file_path):
    """
    Comprehensive analysis of promptfoo results.
    
    Args:
        file_path (str): Path to the JSON file
    
    Returns:
        dict: Comprehensive analysis results
    """
    # Load results
    results = load_promptfoo_results(file_path)
    
    # Extract labels
    y_true, y_pred = extract_results_from_json(results)
    
    # Generate metrics
    metrics = generate_classification_metrics(y_true, y_pred)
    
    return metrics

# Example usage in notebook
def print_classification_metrics(metrics):
    """
    Pretty print classification metrics for notebook display.
    
    Args:
        metrics (dict): Classification metrics
    """
    print("Accuracy:", metrics['accuracy'])
    print("\nConfusion Matrix:")
    print(pd.DataFrame(metrics['confusion_matrix']))
    
    print("\nClassification Report:")
    print(pd.DataFrame(metrics['classification_report']).transpose())

# Notebook workflow example
# results_metrics = analyze_promptfoo_results('path/to/your/results.json')
# print_classification_metrics(results_metrics)


def print_analysis(result_path):
    # Load results
    results = load_promptfoo_results(result_path)

    # Extract labels
    y_true, y_pred = extract_results_from_json(results)

    # Accuracy
    print(f"acc: {accuracy_score(y_true, y_pred)}")

    print(classification_report(y_true, y_pred))

    # Confusion Matrix
    cm = confusion_matrix(y_true, y_pred)

    # Visualization
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=sorted(set(y_true + y_pred)),
                yticklabels=sorted(set(y_true + y_pred)))
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.show()