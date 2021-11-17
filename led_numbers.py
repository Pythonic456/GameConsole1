number_leds = {0:'''#####
#   #
#   #
#   #
#   #
#   #
#####''',
1:''' ##  
  #  
  #  
  #  
  #  
  #  
 ### ''',2:
'''#####
    #
    #
#####
#    
#    
#####''',3:
'''#####
    #
    #
#####
    #
    #
#####''',4:
'''    #
   ##
  # #
 #  #
#####
    #
    #
    #''',5:
'''#####
#    
#    
#####
    #
    #
#####''',6:
'''#####
#    
#    
#####
#   #
#   #
#####''',7:
'''#####
    #
   # 
  #  
 #   
#    
#    ''',8:
'''#####
#   #
#   #
#####
#   #
#   #
#####''',9:
'''#####
#   #
#   #
#####
    #
    #
#####'''}

def draw_numbers(number):
    rows = []
    number = str(number)
    if len(number) < 2: number = '0'+number
    for i in range(7):
        row = number_leds[int(number[0])].split('\n')[i]+number_leds[int(number[1])].split('\n')[i]
        rows.append(row)
    pos = []
    for i in range(7):
        for b in range(10):
            c = rows[i][b]
            pos.append({'x':b,'y':i,'state':{' ':0,'#':1}[c]})
    return pos