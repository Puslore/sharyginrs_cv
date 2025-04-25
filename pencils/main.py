import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import regionprops,label
from skimage.filters import sobel, threshold_otsu
from scipy.ndimage import binary_fill_holes


def pencil_recognition(region, size):
    cy,cx = region.centroid_local
    cx /= region.image.shape[1]
    cy /= region.image.shape[0]
    not_rounded = region.area / (region.perimeter ** 2) < 0.025
    length = ((region.image.shape[0] ** 2) + (region.image.shape[1] ** 2)) ** 0.5
    perimeter = 0.25 * region.perimeter / length
    
    if (perimeter < 1.3) and (perimeter > 0.5) and \
    (abs(cx - 0.5) < 0.1) and (length < size) and \
    (length > (size / 2)) and (not_rounded) and \
    (abs(cy - 0.5) < 0.1):
        return True

    return False


def main():
    absolute_sum = 0

    for i in range(1,13):
        image = plt.imread(f'./images/img ({i}).jpg').mean(axis=2)
        s = sobel(image)

        thresh = threshold_otsu(s) / 2
        s[s < thresh] = 0
        s[s >= thresh] = 1
        s = binary_fill_holes(s, np.ones((3, 3)))
        labeled = (label(s))
        regions = regionprops(labeled)
        regions = sorted(regions, key=lambda x: x.perimeter)
        cnt = 0
        size=np.min(labeled.shape)

        for reg in regions[-10:]:
            cnt += pencil_recognition(reg, size)
            
        print(f'{i}) {cnt} pencils')
        absolute_sum+= cnt

    print(f'Penclis sum: {absolute_sum}')


if __name__ == "__main__":
    main()