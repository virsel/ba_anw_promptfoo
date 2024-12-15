from typing import Dict, Any, Union



def get_assert(output: str, options: Dict[str, Any]) -> Union[bool, float, Dict[str, Any]]:


    # Extract required data from options
    rc = options.get('vars', {}).get('root_cause', "default context")
    try:
        res = output.lower() == rc.lower()  
    except Exception as e:
        print("Error:", e)
        return False
    return res
