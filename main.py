import cv2
import numpy as np
import matplotlib.pyplot as plt

image = 'coins4.jpg'
img = cv2.imread(image, 1)
img_orig = img.copy()
img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
img = cv2.GaussianBlur(img, (21,21), cv2.BORDER_DEFAULT)

all_circs = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 0.9, 120, param1 = 70, param2 = 35, minRadius = 50, maxRadius=250)
all_circs_rounded = np.uint16(np.around(all_circs))

print(all_circs_rounded)
print(all_circs_rounded.shape)
print(f"There are {all_circs_rounded.shape[1]} coins")

def which_coin(coinz):
    coin_types = []
    coins = coinz[0]
    quarter = 0
    for coin in coins:
        if coin[2] > quarter:
            quarter = coin[2]
    for coin in coins:
        if (coin[2]/quarter <= 1).any() and (coin[2]/quarter >= 0.85).any():
            coin_types.append("Quarter")
        elif (coin[2]/quarter < 0.85).any() and (coin[2]/quarter >= 0.70).any():
            coin_types.append("Nickel")
        elif (coin[2]/quarter < 0.70).any() and (coin[2]/quarter >= 0.65).any():
            coin_types.append("Penny")
        elif (coin[2]/quarter < 0.65).any():
            coin_types.append("Dime")
    return coin_types

def calculate_total(coins):
    total = 0
    for coin in coins:
        if coin == "Quarter":
            total += 0.25
        elif coin == "Nickel":
            total += 0.05
        elif coin == "Dime":
            total += 0.10
        elif coin == "Penny":
            total += 0.01
    return total

count = 0

coin_type = which_coin(all_circs_rounded)
print(len(coin_type))
total = calculate_total(coin_type)
print(f"The total is ${total}")
for i in all_circs_rounded[0, :]:
    cv2.circle(img_orig, (i[0], i[1]),i[2],(50, 200, 200), 5)
    cv2.circle(img_orig, (i[0], i[1]), 2, (255, 0, 0), 3)
    cv2.putText(img_orig, f"{coin_type[count]}", (i[0]-70,i[1]+30), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 0, 0), 2)
    count += 1
plt.rcParams['figure.figsize'] = (16,9)
plt.imshow(img_orig, cmap='gray')
plt.show()


'''
A Nickel is 0.8743455497 of a Quarter
A Penny is 0.7853403141
A Dime is 
'''