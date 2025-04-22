import re

def standardiseModel(modelStr):
    '''
    Extract a standardised GPU model from a string

    Input  : a string that is a non standardised model name
    Output : a string that is standardised

    e.g
    In  : "Palit GeForce RTX 5070 Ti GameRock (16 GB GDDR7/PCI Express 5.0/ MHz/28000MHz)"
    Out : "RTX 5070 TI"
    '''
    modelStr = modelStr.upper() #convert all to upper
    modelStr = re.sub(r'[^a-zA-Z0-9\s]', '', modelStr.strip()) #remove non alpha numerics

    prefixes = ["RTX", "RX", "ARC"] #prefixes to find
    suffixes = ['TI', 'SUPER', 'XT', 'XTX'] #possible suffixes

    prefixPattern = '|'.join(prefix for prefix in prefixes) #assemble into a string joined by '|' for regex searching
    suffixPattern = '|'.join(suffix for suffix in suffixes)

    pattern = rf'(?:.*?\b({prefixPattern})\b).*?\s*([A-Za-z])?(\d{{3,4}})\s*((?:\b(?:{suffixPattern})\b\s*)*)' #skip until prefix, optional alphabet ( for cases like A770 ), 3-4 digits, optional suffixes

    matches = re.search(pattern, modelStr) #find groups using regex search
    if not matches: #no matches
        return None

    prefix = matches.group(1) #prefix = prefix
    model = matches.group(2) + matches.group(3) if matches.group(2) else matches.group(3) #model = alphabet + digits if alphabet exists, otherwise just digits
    suffix = matches.group(4) or "" #suffix = any suffixes found or empty otherwise

    return " ".join([prefix,model,suffix]).strip()
    
# model = "Palit GeForce RTX 5070 Ti GameRock (16GB GDDR7/PCI Express 5.0/ MHz/28000MHz)"

# print(standardiseModel(model))