placeholders = "noNO"
cs = """₵¢₡¤$₫€ƒ₣₲₴₭₤₺₼₦₧₱₽₹£₸₮₩¥∙⁒∕≡≢+−×÷=≠><≥≤±≈~¬^∅∞∫Ω∆∏∑√∂µ%‰∶↑→↓←●○◊@&¶§©®™°′″|¦†ℓ‡℮№␣"""
ccs = r""".,:;…!¡?¿·•*#/\(){}[]-–—‒_‚„“”‘’«»‹›‵‴"'⟨⟩"""


def print_in_placeholders(characters, placeholders="noNO"):
    strings = [[f"{p*2}{c}{p*2}" for c in characters] for p in placeholders]
    for row in strings:
        print("".join(row))
        print()
