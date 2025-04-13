#%%
import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label, regionprops
from skimage.segmentation import clear_border


def norm_l1(v1, v2):
    return ((v1 - v2) ** 2).sum() ** 0.5


"""
Символ - сколько я распознал - сколько должно быть
/ 21 21
B 27 25
- 20 20
8 21 23
A 23 21
1 31 31
W 12 12
* 22 22
0 8  10
X 15 15
Неправильно распознано 8 символов. Ошибка < 5%
"""


def extractor(region):
    area = region.area / region.image.size
    cy, cx = region.centroid_local
    cy /= region.image.shape[0]
    cx /= region.image.shape[1]
    perimeter = region.perimeter
    perimeter /= region.image.size
    eccintricity = region.eccentricity
    # vlines = (np.sum(region.image, 0) == region.image.shape[0])
    # vlines = np.sum(vlines) # / region.image.shape
    vlines = count_lgr_vlines(region)
    hole_size = size_of_hole(region) / region.image.size
    euler_number = region.euler_number
    solidity = region.solidity
    wth = region.image.shape[1] / region.image.shape[0]

    return np.array([area, cy, cx*10, perimeter*2, eccintricity*5, vlines*0.3,
                     hole_size*1.2, euler_number*1.2, solidity*1.2, wth])


def classificator(v, templates):
    result = '_'
    min_dist = 10 ** 16

    for key in templates:
        d = norm_l1(v, templates[key])
        if d < min_dist:
            result = key
            min_dist = d

    return result


def size_of_hole(region):
    inverted = ~region.image
    cleared = clear_border(inverted)
    regions = regionprops(label(cleared))
    return sum(region.area for region in regions)


def count_vlines(region):
    return np.all(region.image, axis=0).sum()


def count_lgr_vlines(region):
    x = region.image.mean(axis=0) == 1
    return np.sum(x[: len(x) // 2]) > np.sum(x[len(x) // 2:])



image = plt.imread('./alphabet-small.png')
gray = image.mean(axis=2)
binary = gray < 1

labeled = label(binary)
regions = regionprops(labeled)

# print(len(regions))
# print(image.shape)

templates = {
    'A': [extractor(regions[2])],
    'B': [extractor(regions[3])],
    '8': [extractor(regions[0])],
    '0': [extractor(regions[1])],
    '1': [extractor(regions[4])],
    'W': [extractor(regions[5])],
    'X': [extractor(regions[6])],
    '*': [extractor(regions[7])],
    '-': [extractor(regions[9])],
    '/': [extractor(regions[8])]
}

# print(templates)

# cnt = 1
# for symbol, region in zip(templates, regions):
#     plt.subplot(2, 5, cnt)
#     plt.title(symbol)
#     plt.imshow(region.image)
#     cnt += 1


symbols = plt.imread('./alphabet.png')[:, :, :-1]
gray = symbols.mean(axis=2)
binary = gray > 0
labeled = label(binary)
regions = regionprops(labeled)

res = {}
# -----------------------------------------
for i, region in enumerate(regions):
    v = extractor(region)
    symbol = str(classificator(v, templates))
    # plt.subplot(2, 5, i+1)
    # plt.title(classificator(v, templates))
    
    # print(f'{classificator(v, templates)}')
    # print(i, symbol)
    # print(type(symbol))s
    if symbol in res.keys():
        res[symbol] +=1
    else:
        res[symbol] = 1
    
    # plt.imshow(region.image)
# -----------------------------------------
for symbol, value in res.items():
    print(f'"{symbol}" - {value}')

print(sum(res.values()))

# plt.figure()
# v = extractor(regions[3])
# plt.title(classificator(v, templates))
# plt.imshow(regions[3].image)


# plt.imshow(labeled)
# plt.show()
