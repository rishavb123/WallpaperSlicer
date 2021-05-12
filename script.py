import os

import argparse
import cv2

parser = argparse.ArgumentParser(description='')

def align_type(s):
    if s in ['top', '0', 'up']: return 0
    elif s in ['bot', 'bottom', '2', 'down']: return 2
    else: return 1

def aspect_ratio(s):
    return [int(n) for n in s.split(':')]

parser.add_argument('-a', '--align', type=align_type, default=1, help='Where to align the two images (along the y-axis)')
parser.add_argument('-i', '--input-image', type=str, default='./sunset-over-water.jpg', help='The input image used to crop into seperate images')
parser.add_argument('-o', '--output-folder', type=str, default='./output/{}', help='The folder where to output the cropped images')
parser.add_argument('-ar1', '--aspect-ratio-1', type=aspect_ratio, default=(16, 9), help='The aspect ratio of the first screen')
parser.add_argument('-ar2', '--aspect-ratio-2', type=aspect_ratio, default=(16, 9), help='The aspect ratio of the second screen')
parser.add_argument('-s1', '--screen-size-1', type=float, default=15.6, help='The size of the first screen\'s diagonal in inches')
parser.add_argument('-s2', '--screen-size-2', type=float, default=15.6, help='The size of the second screen\'s diagonal in inches')

args = vars(parser.parse_args())

args['output_folder'] = args['output_folder'].replace('{}', args['input_image'].split('/')[-1].split('.')[0])

if not args['output_folder'][-1] == '/':
    args['output_folder'] += '/'

img = cv2.imread(args['input_image'])

ar1 = args['aspect_ratio_1']
ar2 = args['aspect_ratio_2']

img1, img2 = None, None

if args['screen_size_1'] > args['screen_size_2']:

    img1 = img[:, :int(img.shape[0] * ar1[0] / ar1[1])]

    sy = 0
    ey = img.shape[0]

    r = args['screen_size_2'] / args['screen_size_1']

    if args['align'] == 0:
        ey *= r
    elif args['align'] == 1:
        sy = (1 - r) * ey / 2
        ey *= (1 + r) / 2
    else:
        sy = (1 - r) * ey

    img2 = img[int(sy):int(ey), int(img.shape[0] * ar1[0] / ar1[1]):int(img.shape[0] * ar2[0] * (1 + r) / ar2[1])]

else:

    r = args['screen_size_1'] / args['screen_size_2']

    sy = 0
    ey = img.shape[0]

    if args['align'] == 0:
        ey *= r
    elif args['align'] == 1:
        sy = (1 - r) * ey / 2
        ey *= (1 + r) / 2
    else:
        sy = (1 - r) * ey

    img1 = img[int(sy):int(ey), 0:int(img.shape[0] * ar1[0] * r / ar1[1])]
    img2 = img[:, int(img.shape[0] * ar1[0] * r / ar1[1]):int(img.shape[0] * ar1[0] * r / ar1[1] + img.shape[0] * ar2[0] / ar2[1])]

s = ''
for f in args['output_folder'].split('/'):
    s += f + '/'
    if not os.path.exists(s):
        os.mkdir(s)

cv2.imwrite(args['output_folder'] + 'img1.jpg', img1)
cv2.imwrite(args['output_folder'] + 'img2.jpg', img2)
