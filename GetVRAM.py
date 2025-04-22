import re

def getVram(title):
    '''
    Extract GPU Vram from a string ( usually a title )

    Input  : a string ( usually a title )
    Output : VRAM amount as a string

    e.g
    In  : "Palit GeForce RTX 5070 Ti GameRock (16 GB GDDR7/PCI Express 5.0/ MHz/28000MHz)"
    Out : "16GB"
    '''
    title = title.upper() #convert all to upper

    pattern = r'(\b\d{1,2})\b\s*(GB)' #find up to digits followed by 'GB'
    matches = re.search(pattern, title)
    
    if not matches: #no matches
        return None
    
    #captures both the digits and 'GB' into two groups, so return together
    return matches.group(1) + matches.group(2)

# title = "Powercolor Radeon RX 7800XT | Fighter 16 GB GPU"

# print(getVram(title))