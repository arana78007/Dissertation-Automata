import numpy as np
import matplotlib.pyplot as plt
from numba import jit
size = 100
probability = 0.5
alphabuy = 0.005
alphasell = 0.004
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
consumption_list = []
income_y = 5
price_consume = 1000
theta_buy = 0.4
theta_sell = -0.4
delta_buy = -0.3
delta_sell = 0.5
c_hat = 4
n_inasset = np.full((size,size),50.0)
      
def quantityselection(x,y):
    tempconsume = 0
    if grid[x][y] == 1:
        consume = (income_y+((theta_buy)/(delta_buy))*c_hat)*(delta_buy/(delta_buy+theta_buy))
        quantity = (theta_buy/(delta_buy*(price_list[-1]/(price_consume))))*(consume-c_hat)
        tempconsume += consume
        n_inasset[x][y] += quantity
    elif grid[x][y] == -1:
        consume = (income_y+((theta_sell)/(delta_sell))*c_hat)*(delta_sell/(delta_sell+theta_sell))
        tempconsume += consume
        quantity = (theta_sell/(delta_sell*(price_list[-1]/(price_consume))))*(consume-c_hat)
        n_inasset[x][y] += quantity
        if n_inasset[x][y]>0:
            quantity
        else:
            quantity += -n_inasset[x][y]
    return quantity, tempconsume

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
    else:
        tempnumprice = price_list[time-1]*(1) + beta*(buyselldiff[-1]) 
        price_list.append(tempnumprice)
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
    probability_array[x][y] += alphabuy*states[1] + alphasell*states[0]  
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
                consume += temp[1]
#UPDATES CELL BY CELL
                
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
    plt.pause(0.01) 
#main function loop

plt.show()