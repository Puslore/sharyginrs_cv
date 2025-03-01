#%%
import numpy as np
import matplotlib.pyplot as plt


external = np.diag([1, 1, 1, 1]).reshape(4, 2, 2)

internal = np.logical_not(external)

cross = np.array([[[1, 0], [0, 1]],
                           [[0, 1], [1, 0]]])


def match(a, masks):
    for mask in masks:
        a = (a != 0).astype(int)
        if np.all(a == mask):
            return True
    return False


def count_objects(image):
    E = 0
    for y in range(0, image.shape[0] - 1):
        for x in range(0, image.shape[1] - 1):
            sub = image[y : y + 2, x : x + 2]
            if match(sub, external):
                E += 1
            elif match(sub, internal):
                E -= 1
            elif match(sub, cross):
                E += 2
    return E / 4


# --------------------------------------------
# тут решение для первого файла
# image = np.load('example1.npy')

# image.shape

# print(count_objects(image))

# plt.imshow(image)
# plt.show()
# --------------------------------------------


# тут решение для второго файла
image = np.load('example2.npy')

cnt = 0
for i in range(image.shape[2]):
    cnt += count_objects(image[:, :, i])
    # print(count_objects(image[:, :, i]))

cnt
