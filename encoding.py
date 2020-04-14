import numpy as np
import cv2

inputImg = cv2.imread('dog.jpg', 0)  # read the image
cv2.imshow('dog', inputImg)

row = inputImg.shape[0]
col = inputImg.shape[1]

img = np.array(inputImg).flatten()  # flatten the image into 1d array
frq = np.zeros(256, dtype=int)  # frq of all gray scale levels
blockSize = int(input('1. Enter the block size: '))
floatSize = int(input('2. Enter the float size (16-32-64): '))
total = row * col
if floatSize == 16:
    res = np.zeros(total // blockSize, dtype=np.float16)  # final codes
    # array of probability of each of 256 gray scale levles
    prob = np.zeros(256, dtype=np.float16)
elif floatSize == 32:
    res = np.zeros(total // blockSize, dtype=np.float32)  # final codes
    prob = np.zeros(256, dtype=np.float32)
elif floatSize == 64:
    res = np.zeros(total // blockSize, dtype=np.float64)  # final codes
    prob = np.zeros(256, dtype=np.float64)

# prob = np.zeros(256)  # array of probability of each of 256 gray scale levles
grayLvl = 256

for i in img:
    frq[i] += 1

for i in range(0, grayLvl):
    prob[i] = frq[i] / (total)

for i in range(1, grayLvl):
    prob[i] += prob[i - 1]

for i in range(0, total, blockSize):
    l = 0.0
    r = 1.0
    for j in range(i, i + blockSize):
        oldLeft = l
        oldRight = r
        # base  + (range) * prob[cur pixel]
        if img[j] != 0:
            l = oldLeft + (oldRight - oldLeft) * prob[img[j] - 1]
        r = oldLeft + (oldRight - oldLeft) * prob[img[j]]
    # result of the block is the average of (upper - lower)
    it = int(i / blockSize)
    res[it] = (l + r) / 2

# export encoded tags && pro
np.save('./encoded-image', res)
np.save('./probability', prob)
blockSizeFile = open('blockSizeFile.txt', "w")
blockSizeFile.write(str(blockSize))  # read block size
blockSizeFile.write('\n' + str(row))  # read row dimension
blockSizeFile.write('\n' + str(col))  # read col dimension
# terminate showing the image on pressing any key
cv2.waitKey(0)
cv2.destroyAllWindows()
