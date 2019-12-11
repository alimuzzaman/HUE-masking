from PIL import Image
import numpy as np
import codecs, json

# im = Image.open('SFdE0.png')
im = Image.open('alim.jpg')
HSV = im.convert('HSV')
RGB = im.convert('RGBA')

data = np.array(HSV)   # "data" is a height x width x 4 numpy array
hue, saturation, value = data.T # Temporarily unpack the bands for readability

im_RGB = np.array(RGB)   # "data" is a height x width x 4 numpy array
red, green, blue, alpha = im_RGB.T # Temporarily unpack the bands for readability

hue_sample = [1, 350, 354, 10, 6, 358, 344, 6, 347, 16, 346, 6]
hue_avg = np.average(hue_sample)
print(hue_sample)
print(hue_avg)
print(int(hue_avg) - 30, int(hue_avg) + 30)
# Mask = (np.zeros([len(hue),len(hue[0])])).astype(np.uint8)
Mask = np.empty([len(hue[0]),len(hue)])

for i in range(0, len(hue)):
    for j in range(0, len(hue[i])):
        if hue[i][j] in range(int(hue_avg) - 30, int(hue_avg) + 30) :
            Mask[j][i] = 255
        else:
            Mask[j][i] = 0


for i in range(0, len(im_RGB)):
    for j in range(0, len(im_RGB[i])):
        if Mask[i][j] == 255:
            im_RGB[i][j] = [255, 255, 255, 1]


json.dump(im_RGB[0:2].tolist(), codecs.open('tst.json', 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4) ### this saves the array in .json format

# Replace white with hue... (leaves alpha values alone...)
# white_areas = (red == 255) & (blue == 255) & (green == 255)
# im_RGB[..., :-1][white_areas.T] = (255, 0, 0) # Transpose back needed

im2 = Image.fromarray(Mask)
im2 = im2.convert('RGB')
im2.save('alim.mask.jpg')
im2.show()

im2 = Image.fromarray(im_RGB)
im2 = im2.convert('RGB')
im2.save('alim.masked.jpg')

im2.show()