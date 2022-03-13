import random
import csv

consentration = [20, 40, 50, 60, 80, 100]
header = ['class', 'consentration', 'camera max red', 'camera max green', 'camera max blue', 'camera mean red', 'camera mean green',
          'camera mean blue', 'mic max red', 'mic max green', 'mic max blue', 'mic mean red', 'mic mean green', 'mic mean blue', 'sensor red', 'sensor green', 'sensor blue']

# =======================
# ==> class encoder   <==
# ==> 1 = red         <==
# ==> 2 = green       <==
# ==> 3 = blue        <==
# =======================

f_reg = open('data/dummy_data_reg.csv', 'w')
# writer = csv.writer(f)
writer_reg = csv.writer(f_reg)

f_class = open('data/dummy_data_cla.csv', 'w')
# writer = csv.writer(f)
writer_class = csv.writer(f_class)

# writer.writerow(header)

i = 0

while(i < 250):
    # class dominant red
    classes = "red"
    cam_mean_r = random.uniform(0.4, 0.7)
    cam_mean_g = random.uniform(0, 1-cam_mean_r-0.3)
    cam_mean_b = 1 - cam_mean_r - cam_mean_g

    cam_max_r = random.uniform(cam_mean_r, 0.7)
    cam_max_g = random.uniform(0, 1-cam_max_r-0.3)
    cam_max_b = 1 - cam_max_r - cam_max_g

    mic_mean_r = random.uniform(0.4, 0.7)
    mic_mean_g = random.uniform(0, 1-mic_mean_r-0.3)
    mic_mean_b = 1 - mic_mean_r - mic_mean_g

    mic_max_r = random.uniform(mic_mean_r, 0.7)
    mic_max_g = random.uniform(0, 1-mic_max_r-0.3)
    mic_max_b = 1 - mic_max_r - mic_max_g

    sens_r = random.uniform(0.4, 0.7)
    sens_g = random.uniform(0, 1-sens_r-0.3)
    sens_b = 1 - sens_r - sens_g

    if(cam_mean_r <= 0.45):
        amount = consentration[random.randint(0, 1)]
    elif(cam_mean_r <= 0.6 and cam_mean_r >= 0.45):
        amount = consentration[random.randint(2, 3)]
    elif(cam_mean_r >= 0.6):
        amount = consentration[random.randint(4, 5)]

    print("red class : ")
    print("cam mean r = %f, cam mean g = %f, cam mean b = %f, cam max r = %f, cam max g = %f, cam max b = %f \n mic mean r = %f, mic mean g = %f, mic mean b = %f, mic max r = %f, mic max g = %f, mic max b = %f \n, sensor r = %f , sensor g = %f, sensor b = %f  || amount = %f \n" % (
        cam_mean_r, cam_mean_g, cam_mean_b, cam_max_r, cam_max_g, cam_max_b, mic_mean_r, mic_mean_g, mic_mean_b, mic_max_r, mic_max_g, mic_max_b, sens_r, sens_g, sens_b, amount))
    row = [cam_mean_r, cam_mean_g, cam_mean_b, cam_max_r, cam_max_g, cam_max_b, mic_mean_r,
           mic_mean_g, mic_mean_b, mic_max_r, mic_max_g, mic_max_b, sens_r, sens_g, sens_b, classes]
    writer_class.writerow(row)
    row = [cam_mean_r, cam_mean_g, cam_mean_b, cam_max_r, cam_max_g, cam_max_b, mic_mean_r,
           mic_mean_g, mic_mean_b, mic_max_r, mic_max_g, mic_max_b, sens_r, sens_g, sens_b, amount]
    writer_reg.writerow(row)
    i = i + 1

i = 0

while(i < 250):

    # class dominant green
    classes = "green"
    cam_mean_g = random.uniform(0.4, 0.7)
    cam_mean_b = random.uniform(0, 1-cam_mean_g-0.3)
    cam_mean_r = 1 - cam_mean_b - cam_mean_g

    cam_max_g = random.uniform(cam_mean_g, 0.7)
    cam_max_b = random.uniform(0, 1-cam_max_g-0.3)
    cam_max_r = 1 - cam_max_b - cam_max_g

    mic_mean_g = random.uniform(0.4, 0.7)
    mic_mean_b = random.uniform(0, 1-mic_mean_g-0.3)
    mic_mean_r = 1 - mic_mean_b - mic_mean_g

    mic_max_g = random.uniform(mic_mean_g, 0.7)
    mic_max_b = random.uniform(0, 1-mic_max_g-0.3)
    mic_max_r = 1 - mic_max_b - mic_max_g

    sens_g = random.uniform(0.4, 0.7)
    sens_b = random.uniform(0, 1-sens_g-0.3)
    sens_r = 1 - sens_b - sens_g

    if(cam_mean_g <= 0.5):
        amount = consentration[random.randint(0, 1)]
    elif(cam_mean_g <= 0.6 and cam_mean_g >= 0.5):
        amount = consentration[random.randint(2, 3)]
    elif(cam_mean_g >= 0.6):
        amount = consentration[random.randint(4, 5)]

    print("blue class : ")
    print("cam mean r = %f, cam mean g = %f, cam mean b = %f, cam max r = %f, cam max g = %f, cam max b = %f \n mic mean r = %f, mic mean g = %f, mic mean b = %f, mic max r = %f, mic max g = %f, mic max b = %f \n, sensor r = %f , sensor g = %f, sensor b = %f  || amount = %f \n" % (
        cam_mean_r, cam_mean_g, cam_mean_b, cam_max_r, cam_max_g, cam_max_b, mic_mean_r, mic_mean_g, mic_mean_b, mic_max_r, mic_max_g, mic_max_b, sens_r, sens_g, sens_b, amount))
    row = [cam_mean_r, cam_mean_g, cam_mean_b, cam_max_r, cam_max_g, cam_max_b, mic_mean_r,
           mic_mean_g, mic_mean_b, mic_max_r, mic_max_g, mic_max_b, sens_r, sens_g, sens_b, classes]
    writer_class.writerow(row)
    row = [cam_mean_r, cam_mean_g, cam_mean_b, cam_max_r, cam_max_g, cam_max_b, mic_mean_r,
           mic_mean_g, mic_mean_b, mic_max_r, mic_max_g, mic_max_b, sens_r, sens_g, sens_b, amount]
    writer_reg.writerow(row)
    i = i + 1

i = 0

while(i < 250):
    # class dominant blue
    classes = "blue"

    cam_mean_b = random.uniform(0.4, 0.7)
    cam_mean_g = random.uniform(0, 1-cam_mean_b-0.3)
    cam_mean_r = 1 - cam_mean_b - cam_mean_g

    cam_max_b = random.uniform(cam_mean_b, 0.7)
    cam_max_g = random.uniform(0, 1-cam_max_b-0.3)
    cam_max_r = 1 - cam_max_b - cam_max_g

    mic_mean_b = random.uniform(0.4, 0.7)
    mic_mean_g = random.uniform(0, 1-mic_mean_b-0.3)
    mic_mean_r = 1 - mic_mean_b - mic_mean_g

    mic_max_b = random.uniform(mic_mean_b, 0.7)
    mic_max_g = random.uniform(0, 1-mic_max_b-0.3)
    mic_max_r = 1 - mic_max_b - mic_max_g

    sens_b = random.uniform(0.4, 0.7)
    sens_g = random.uniform(0, 1-sens_b-0.3)
    sens_r = 1 - sens_b - sens_g

    if(cam_mean_b <= 0.5):
        amount = consentration[random.randint(0, 1)]
    elif(cam_mean_b <= 0.6 and cam_mean_b >= 0.5):
        amount = consentration[random.randint(2, 3)]
    elif(cam_mean_b >= 0.6):
        amount = consentration[random.randint(4, 5)]

    print("blue class : ")
    print("cam mean r = %f, cam mean g = %f, cam mean b = %f, cam max r = %f, cam max g = %f, cam max b = %f \n mic mean r = %f, mic mean g = %f, mic mean b = %f, mic max r = %f, mic max g = %f, mic max b = %f \n, sensor r = %f , sensor g = %f, sensor b = %f  || amount = %f \n" % (
        cam_mean_r, cam_mean_g, cam_mean_b, cam_max_r, cam_max_g, cam_max_b, mic_mean_r, mic_mean_g, mic_mean_b, mic_max_r, mic_max_g, mic_max_b, sens_r, sens_g, sens_b, amount))
    row = [cam_mean_r, cam_mean_g, cam_mean_b, cam_max_r, cam_max_g, cam_max_b, mic_mean_r,
           mic_mean_g, mic_mean_b, mic_max_r, mic_max_g, mic_max_b, sens_r, sens_g, sens_b, classes]
    writer_class.writerow(row)
    row = [cam_mean_r, cam_mean_g, cam_mean_b, cam_max_r, cam_max_g, cam_max_b, mic_mean_r,
           mic_mean_g, mic_mean_b, mic_max_r, mic_max_g, mic_max_b, sens_r, sens_g, sens_b, amount]
    writer_reg.writerow(row)
    i = i + 1

i = 0
