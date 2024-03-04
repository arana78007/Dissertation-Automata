#CODE LUCE MODEL DERIVED AND SIMULATE, WILL WE GET RESULT THAT BUBBLES CAN BE CORRECTED, FIRST OPTIMAL PURCHASE AMOUNT UTILITY MAX
import numpy as np
import matplotlib.pyplot as plt
from numba import jit
size = 100
probability = 0.5
alphabuy = 0.1
#alphabuy critikal point where herding counter luce model utility is 0.15 or difference = 0.125 solve for formally
alphasell = 0.005
neighborhood_size = 3
time = 0
max_time = 400
start_price = 1000
beta = 0.0005
price_list = []  
return_list = [0,0]  
profit = 1100
buyselldiff = []
starting_diff = 0
gamma = 0.1
quantity_array = np.full((size,size),0)
consumption_list = []
income_y = 5
price_consume = 1000
delta = 0.95
luceset_ = [0.05,0.5,0.95]

def luce_utility_(time):
    if time>1:
        deltafunc = (delta*(-buyselldiff[-1]))/(1+np.abs(buyselldiff[-1]))
        utility_list = list(map(lambda x: np.power(x,deltafunc) + x*return_list[-1] , luceset_))
        total_utility = sum(utility_list)
        probability_luce = list(map(lambda x: x/total_utility , utility_list))
        if sum(utility_list)!=0:
            chosen_item = np.random.choice(luceset_, p = probability_luce)
            return chosen_item
        else:
            chosen_item = np.random.choice(luceset_, p = 1/3)
            return chosen_item
    else:
        return luceset_[1]
# ADD MARTINGALE RETURNS
      
def quantityselection(x,y):
    theta_buy = np.random.uniform(0,gamma)
    tempconsume = 0
    if grid[x][y] == 1:
        quantity = income_y*((theta_buy)/(theta_buy+gamma))
        tempconsume += income_y*((gamma)/((gamma+theta_buy)*(price_consume/price_list[-1])))
    elif grid[x][y] == -1:
        quantity = -income_y*((theta_buy)/(theta_buy+gamma))
        tempconsume += 0
    return quantity, tempconsume
#gives the selection of quanity based on utility
#TODO maybe consider c being negative as well?
        
def asset_return(time):
    if time > 0:
        return_list.append((((price_list[time])-price_list[time-1])/price_list[time-1]))
        return return_list
    else:
        return 690
#GIVES PERCENT CHANGE, CORRECT FOR NEGATIVE PRICES NEEDED.

def price(time):
    if time < 1:
        price_list.append(start_price)
        return price_list
    elif 1<=time<max_time:
        beta = np.abs((buyselldiff[-1])/(10000000))
        tempnum = price_list[time-1] + beta*(buyselldiff[-1]) + np.random.normal(0,2)
        price_list.append(tempnum)
        return price_list
#GIVES A LIST OF THE PRICE OVERTIME WHERE EACH ENTRY CORRESPONDS TO THE TIME PERIOD 

@jit
def neighbourstatesellbuy(size,grid,x, y):
    tempnum1 = [0,0]
    for dx in [-1, 0, 1]:
        if 0 <= x + dx < size:
            for dy in [-1, 0, 1]:
                if 0 <= y + dy < size:
                    if dx == 0 and dy == 0:
                        continue
                    if  grid[x + dx][y + dy] == -1:
                        tempnum1[0] += grid[x + dx][y + dy]
                    elif grid[x + dx][y + dy] == 1:
                        tempnum1[1] += grid[x + dx][y + dy]         
    return tempnum1 
#SUMS NEIGHBOURS STATES, first number is sellers, second is the buyers

def intial_grid(size):
    grid = np.random.choice([-1,1],size=(size,size))
    probability_array = np.full((size,size),0.5)
    return grid, probability_array
#PICKS RANDOM STARTING POINT WITH 50:50 CHANCE

def grid_update(size,grid,x, y,probability_array):
    states = neighbourstatesellbuy(size,grid,x, y)
    probability_array[x][y] = luce_utility_(time) + alphabuy*states[1] + alphasell*states[0]    
    if probability_array[x][y] > 1:
        probability_array[x][y] = 1
        return  1
    elif probability_array[x][y] < 0:
            probability_array[x][y] = 0
            return -1
    else:
        if np.random.rand()< probability_array[x][y]:
                return 1
        else:
                return -1
#UPDATE FUNCTION FOR GIVEN RULES, edge cases defined on sets outside of [0,1]

grid, probability_array = intial_grid(size)
fig, axs = plt.subplots(4, gridspec_kw={'height_ratios': [4, 2, 1, 2]})
img = axs[0].imshow(grid,cmap='BuPu',interpolation='nearest') 
text = axs[0].text(0.5, 1.05, '', transform=axs[0].transAxes, ha='center')
price_graph = axs[1].plot(price(time))
#PLOT TYPES + GRID INITIALIZATION

def main(grid,size,probability_array):
    global starting_diff,consume
    consume = 0
    starting_diff = 0
    temp_array = grid.copy()
    for x in range(size):
            for y in range(size):
                grid[x][y] = grid_update(size, temp_array, x, y, probability_array)
                temp = quantityselection(x,y)
                starting_diff += temp[0]
                consume += quantityselection(x,y)[1]
#UPDATES CELL BY CELL, resource heavy
                
while time < max_time:
    if time>=0:
        main(grid,size,probability_array)
        buyselldiff.append(starting_diff)
        consumption_list.append(consume)
    price_graph = axs[1].plot(price(time))
    percent_graph = axs[2].plot(asset_return(time))
    consumption_graph = axs[3].plot(consumption_list)
    axs[2].set_ylim(-0.2,0.2)
    img.set_array(grid)
    time += 1
    text.set_text(f'Time: {time}')
    plt.pause(0.001) 
#MAIN FUNCTION LOOP

plt.show()

#consumption function fails when the price of the asset is negative correct this to make the price 0 when it goes below 0
#np.abs(put price here)
#UPDATE CONSUMPTION UTILITY LUCE WORKS WELL