import modes
from comm import uart1

transfer = 'X000000X000000' #Xf0Xf0  0Xf0Xf
income = {
            "aceleration_x": 0,
            "aceleration_y": 0,
            "button": "0",
            "mode": 0
}


while True:
    try:
        transfer = uart1.read(len(transfer)).decode('utf-8') #přijem řetězce z microbitu --> dva signály za sebou
        x_pos = transfer.index('X') # pozice znaku 'X' v signálu --> 'X' je oddělovač, tzn. značí začátek signálu --> ošetření signalizace
        income["aceleration_x"] = int(transfer[x_pos+1]+transfer[x_pos+2])
        income["aceleration_y"] = int(transfer[x_pos+3]+transfer[x_pos+4])
        income["button"] = transfer[x_pos+5]
        income["mode"] = int(transfer[x_pos+6])
        
    except UnicodeError: # ošetření vyjímek, signal je zpočátku zmatený
        pass
    except ValueError: # ošetření vyjímek, signal je zpočátku zmatený
        pass
    except IndexError: # ošetření vyjímek, signal je zpočátku zmatený
        pass

    if income["mode"] == 0:
        modes.mode0() 

    elif income["mode"] == 1:
        modes.mode1(income)
        
    elif income["mode"] == 2:
        modes.mode2(income)
    
    elif income["mode"] == 3:
        modes.mode3()