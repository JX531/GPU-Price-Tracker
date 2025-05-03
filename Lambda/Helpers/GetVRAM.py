import re

def getVram(title):
    '''
    Extract GPU Vram from a string ( usually a title )

    Input  : a string ( usually a title )
    Output : VRAM amount as an int

    e.g
    In  : "Palit GeForce RTX 5070 Ti GameRock (16 GB GDDR7/PCI Express 5.0/ MHz/28000MHz)"
    Out : "16"
    '''
    title = title.upper() #convert all to upper

    pattern = r'(\b\d{1,2})\b\s*GB' #find up to digits followed by 'GB'
    matches = re.search(pattern, title)
    
    if not matches: #no matches
        return None
    
    return int(matches.group(1))