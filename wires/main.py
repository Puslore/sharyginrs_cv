# %%
import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label
from skimage.morphology import (binary_closing,
                                                    binary_opening,
                                                    binary_dilation,
                                                    binary_erosion)



# plt.imshow(np.load('./files/wires6npy.txt'))
# plt.show()

for _ in range(1, 7):
    print(f'{_} файл:')
    data = np.load(f'./files/wires{_}npy.txt')

    labeled = np.max(label(data)) #marking image
    # print(labeled)
    # print(np.max(labeled)) #count object value
    
    for cnt in range(1, labeled + 1):
        print(f'{cnt} провод:')
        result = binary_erosion(label(data) == cnt, #slicing
                                        np.ones(3).reshape(3, 1))
        new_labeled = np.max(label(result))

        # new_labeled == cnt
        # answer = new_labeled - labeled
        # print(new_labeled, labeled, answer)

        if new_labeled > 1:
            print(f'провод порван на {new_labeled} частей')
        
        else:
            print('провод целый')
        # print(answer)


        plt.imshow(label(data) == cnt)
        plt.show()
