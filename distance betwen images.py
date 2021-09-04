import os
import numpy as np
import PIL as pl
import matplotlib.pyplot as plt
import imagehash as ms


PATH = './runs/run_1'

images = []
imagenames = []
for root, dirs, filies in os.walk(PATH):
    for file in filies[::100]:
        images.append(pl.Image.open(os.path.join(PATH, file)))
        imagenames.append(file.replace('.png',''))
        print('image: '+file+' added')

print('done collecting images')
def distance(image1, image2): #not in use
    return np.sum((2*(((image1-image1.min())/image1.max())-0.5))*(2*(((image2-image2.min())/image2.max())-0.5)))/(image1.shape[0]*image1.shape[1])



print('started calculating distances')
hashes = []
for i in range(len(images)):
    image=np.copy(np.asarray(images[i]))
    b=ms.dhash(images[i]).hash.flatten()
    hashes.append(int(''.join(list(b.astype(int).astype(str))),2)) #calculating "number" of edges in the -> direction

print('done calculating distances')
plt.imshow(images[5])
plt.show()
Z = [x for _,x in sorted(zip(hashes,imagenames))]
print(Z)
plt.figure()
plt.plot(hashes, [1]*len(hashes), '.')
plt.show()
