import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
from skimage.color import rgb2hsv

def print_statistics(hues, split_points):
    print('Number of shades: ' + str(len(split_points[0]) + 1))
    print(f'Number of shapes of shade 1: {split_points[0][0]}')
    for i in range(1, len(split_points[0])):
        print(f'Number of shapes of shade {i + 1}: {split_points[0][i] - split_points[0][i - 1]}')
    print(f'Number of shapes of shade {len(split_points[0]) + 1}: {len(hues) - split_points[0][-1]}')

def main():
    img = plt.imread('./balls_and_rects.png')
    gray = img.mean(axis=2)
    binary_mask = gray > 0
    labeled = label(binary_mask)
    regions = regionprops(labeled)

    circle_num = 0
    circle_hues = []
    rect_num = 0
    rect_hues = []

    for region in regions:
        fill = region.area / (region.image.shape[0] * region.image.shape[1])
        y, x = region.centroid
        hue = rgb2hsv(img[int(y), int(x)])[0]
        if fill < 1.0:
            circle_num += 1
            circle_hues.append(hue)
        else:
            rect_num += 1
            rect_hues.append(hue)

    total_shapes = len(regions)
    all_hues = [rgb2hsv(img[int(region.centroid[0]), int(region.centroid[1])])[0] for region in regions]

    print(f'Number of circles: {circle_num}')
    print(f'Number of rectangles: {rect_num}')
    print(f'Total number of shapes: {total_shapes}')

    hue_diff_all = np.diff(sorted(all_hues))
    split_all = np.where(hue_diff_all > np.std(hue_diff_all))
    print('Total:')
    print_statistics(all_hues, split_all)
    print('\n')

    hue_diff_circles = np.diff(sorted(circle_hues))
    split_circles = np.where(hue_diff_circles > np.std(hue_diff_circles) * 2)
    print('Circles:')
    print_statistics(circle_hues, split_circles)
    print('\n')

    hue_diff_rects = np.diff(sorted(rect_hues))
    split_rects = np.where(hue_diff_rects > np.std(hue_diff_rects) * 2)
    print('Rectangles:')
    print_statistics(rect_hues, split_rects)

if __name__ == "__main__":
    main()
