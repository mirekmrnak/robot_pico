import modes
from comm import uart1

#Set up mode 0 when car is started
mode = 0

transfer = 'X000X000' #Xf0Xf0  0Xf0Xf
income = '000' #Xf0Xf0  0Xf0Xf

while True:
    try:
        transfer = uart1.read(len(transfer)).decode('utf-8') #přijem řetězce z microbitu --> dva signály za sebou
        x_pos = transfer.index('X') # pozice znaku 'X' v signálu --> 'X' je oddělovač, tzn. značí začátek signálu --> ošetření signalizace
        income = transfer[x_pos+1]+transfer[x_pos+2]+transfer[x_pos+3] # poskládán signál už ve správném pořadí
        mode = int(income[2])
        
    except UnicodeError: # ošetření vyjímek, signal je zpočátku zmatený
        pass
    except ValueError: # ošetření vyjímek, signal je zpočátku zmatený
        pass
    except IndexError: # ošetření vyjímek, signal je zpočátku zmatený
        pass

    if mode == 0:
        modes.mode0() 

    elif mode == 1:
        modes.mode1(income)
        
    elif mode == 2:
        modes.mode2()
    
    elif mode == 3:
        modes.mode3()