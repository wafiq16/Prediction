import random
import csv

consentration = [5, 10, 15, 20, 25, 30]
header = ['class', 'consentration', 'red', 'green', 'blue']

# =======================
# ==> class encoder   <==
# ==> 1 = green       <==
# ==> 2 = blue        <==
# ==> 3 = red         <==
# =======================

f_reg = open('/home/wafiq/Prediction/data/dummy_data_reg.csv', 'w')
# writer = csv.writer(f)
writer_reg = csv.writer(f_reg)

f_class = open('/home/wafiq/Prediction/data/dummy_data_cla.csv', 'w')
# writer = csv.writer(f)
writer_class = csv.writer(f_class)

# writer.writerow(header)

i = 0

while(i<250) :
     
    # class dominant green
    classes = "green"
    g = random.uniform(0.4, 0.7)
    b = random.uniform(0, 1-g-0.3)
    r = 1 - b - g
    amount = consentration[random.randint(0,5)]
    print("green class : ")
    print("g = %f, b = %f, r = %f" %(g, b, r))
    row = [r, g, b, classes]
    writer_class.writerow(row)
    row = [r, g, b, amount]
    writer_reg.writerow(row)
    i = i + 1

i = 0

while(i<250) :
    # class dominant blue
    classes = "blue"
    b = random.uniform(0.4, 0.7)
    g = random.uniform(0, 1-b-0.3)
    r = 1 - b - g
    amount = consentration[random.randint(0,5)]
    print("blue class : ")
    print("g = %f, b = %f, r = %f" %(g, b, r))
    row = [r, g, b, classes]
    writer_class.writerow(row)
    row = [r, g, b, amount]
    writer_reg.writerow(row)
    i = i + 1

i = 0

while(i<250) :
    # class dominant red
    classes = "red"
    r = random.uniform(0.4, 0.7)
    b = random.uniform(0, 1-r-0.3)
    g = 1 - b - g
    amount = consentration[random.randint(0,5)]
    print("red class : ")
    print("g = %f, b = %f, r = %f" %(g, b, r))
    row = [r, g, b, classes]
    writer_class.writerow(row)
    row = [r, g, b, amount]
    writer_reg.writerow(row)
    
    i = i + 1

i = 0