# this section is for calcuating the mask

def calc(num : int):
    if num < 8:
        ret = 0
        for x in range(num):
            ret += 2**(7-x)
        return ret
    else:
        return 255
    
mask = 0

while True:
    try:
        user_input = input('Input mask (e.g., 24) or press Enter to quit > ').strip()
        
        if user_input == '':
            print("Exiting...")
            False
            break
            
        mask = int(user_input)
        
        if 0 <= mask <= 32:
            print(f"Valid mask received > /{mask}")
            break
        else:
            print("Please enter a mask between 0 and 32.")

    except ValueError:
        print('Invalid input! Please enter an integer.')
    except KeyboardInterrupt:
        print('\nProgram stopped by user.')
        False
        break

if mask <= 8:
    print(f'Mask is in decimal > {calc(mask)}.0.0.0')
elif mask <= 16:
    print(f'Mask is in decimal > 255.{calc(mask-8)}.0.0')
elif mask <= 24:
    print(f'Mask is in decimal > 255.255.{calc(mask-16)}.0')
else:
    print(f'Mask is in decimal > 255.255.255.{calc(mask-24)}')