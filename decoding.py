# Lib to convert np array to image cuz I can't convert numpy array to an image using opencv
from PIL import Image
import numpy as np

res = np.load('./encoded-image.npy')
prob = np.load('./probability.npy')
grayLvl = 256
blockSizeFile = open('blockSizeFile.txt', "r")
blockSize = int(blockSizeFile.readline())
row = int(blockSizeFile.readline())
col = int(blockSizeFile.readline())
total = row * col
out = np.zeros(total)

for i in range(0, total, blockSize):
    l = 0.0
    r = 1.0
    for j in range(i, i + blockSize):  # loop over block size  = 16
        for k in range(0, grayLvl):
            tag = res[int(i / blockSize)]
            if tag < l + (r - l) * prob[k]:  # if This interval cover me
                oldLeft = l
                oldRight = r
                if k != 0:
                    l = oldLeft + (oldRight - oldLeft) * prob[k - 1]
                r = oldLeft + (oldRight - oldLeft) * prob[k]
                out[j] = k
                break

print(out)
out = np.array(out).reshape((row, col))

outImage = Image.fromarray(out)
outImage.show()
