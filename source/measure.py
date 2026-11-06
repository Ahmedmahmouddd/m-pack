import sys, glob
import cv2
import numpy as np

# Prints how far the text ink sits from the vertical (and horizontal) middle of each captured control.
for path in sorted(sum((glob.glob(p) for p in sys.argv[1:]), [])):
    im = cv2.imread(path).astype(int)
    h, w = im.shape[:2]
    inset_y = max(3, h // 12)
    inset_x = w // 6 if 'select' in path else max(6, w // 30)
    core = im[inset_y:h - inset_y, inset_x:w - inset_x]
    bg = np.median(core.reshape(-1, 3), axis=0)
    ink = np.abs(core - bg).sum(axis=2) > 120
    ys = ink.any(axis=1).nonzero()[0]
    xs = ink.any(axis=0).nonzero()[0]
    if not len(ys):
        print(path, 'no ink'); continue
    top = ys[0] + inset_y
    bottom = h - 1 - (ys[-1] + inset_y)
    cy = (ink.nonzero()[0].mean() + inset_y) / h
    left = xs[0] + inset_x
    right = w - 1 - (xs[-1] + inset_x)
    print(f'{path.split("/")[-1]:22s} h={h:4d} top={top:3d} bottom={bottom:3d} diff={bottom - top:+4d}  centroid={cy:.3f}  L={left} R={right}')
