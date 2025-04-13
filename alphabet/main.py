#%%
import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label, regionprops
from skimage.segmentation import clear_border
from skimage.morphology import binary_dilation
from pathlib import Path


def count_holes(region):
    shape = region.image.shape
    new_image = np.zeros((shape[0] + 2, shape[1] + 2))
    new_image[1: -1, 1: -1] = region.image
    new_image = np.logical_not(new_image)
    labeled = label(new_image)
    
    return np.max(labeled) - 1


def count_vlines(region):
    return np.all(region.image, axis=0).sum()


def count_lgr_vlines(region):
    x = region.image.mean(axis=0) == 1
    return np.sum(x[: len(x) // 2]) > np.sum(x[len(x) // 2:])


def size_of_hole(region):
    inverted = ~region.image
    cleared = clear_border(inverted)
    regions = regionprops(label(cleared))
    return sum(region.area for region in regions)


def recognize(region):
    if np.all(region.image):
        return '-'
    else: # 9 symbols
        holes = count_holes(region)
        if holes == 2: # 8 or B
            _, cx = region.centroid_local
            cx /= region.image.shape[1]
            # return f'{cx}'
            if cx < 0.44:
                return 'B'
            return '8'
        elif holes == 1: # A or 0 and P or D
            if count_vlines(region) > 1: # P, D
                if size_of_hole(region) / region.area < 0.5:
                    return 'P' 
                else:
                    return 'D'
            else: # A, 0
                cy, cx = region.centroid_local
                cx /= region.image.shape[1]
                cy /= region.image.shape[0]
                if abs(cx - cy) < 0.03:
                    return '0'
                return 'A'
        else: # 1, *, /, X, W
            if count_vlines(region) >= 3:
                return '1'
            else:
                if region.eccentricity < 0.43:
                    return '*'
                # /, X, W
                inv_image = ~region.image
                inv_image = binary_dilation(inv_image, np.ones((3, 3)))
                labeled = label(inv_image, connectivity=1)
                match np.max(labeled):
                    case 2:
                        return '/'
                    case 4:
                        return 'X'
                    case _:
                        return 'W'

    return '#'


symbols = plt.imread(Path(__file__).parent / 'symbols.png')
gray = symbols[:, :, :-1].mean(axis=2)
binary = gray > 0
labeled = label(binary)
regions = regionprops(labeled)

result = {}

for i, region in enumerate(regions):
    # if (i + 1) % 25 == 0:
    #     print(f'{i + 1}/{len(regions)}')
    symbol = recognize(region)
    if symbol not in result:
        result[symbol] = 0
    result[symbol] += 1

for symbol, value in result.items():
    print(f'"{symbol}" -> {value}')
