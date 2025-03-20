# %%
import numpy as np
import matplotlib.pyplot as plt
from skimage.morphology import binary_opening
from skimage.measure import label


stars = np.load('./stars.npy')
rectangle_mask = np.array(
    [
        [1, 1, 1],
        [1, 1, 1]
    ]
)

labeled_stars = label(stars)
labeled_rectangles = label(binary_opening(stars, rectangle_mask))

res = np.max(labeled_stars) - np.max(labeled_rectangles)

print(f'Stars value: {res}')


plt.imshow(stars)
plt.show()
