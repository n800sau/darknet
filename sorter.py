#!/usr/bin/env python

import os
from PIL import Image, ImageDraw

BOXFNAME = 'bboxes.txt'
CLSFNAME = 'data/classnames_VOC.txt'
DESTDIR = 'sorted'

#cls_only = ['cat', 'bird']
cls_only = []

clslst = [l.strip() for l in file(CLSFNAME).readlines()]

clsf = {}
for line in file(BOXFNAME):
	fname,x1,y1,x2,y2,prob,dummy,cls = line.split()
	if cls not in clsf:
		clsf[cls] = []
	clsf[cls].append([fname, (x1,y1,x2,y2)])

for cls,vals in clsf.items():
	clsname = clslst[int(cls)]
	if clsname in cls_only or not cls_only:
		ddname = os.path.join(DESTDIR, clsname)
		if not os.path.exists(ddname):
			os.makedirs(ddname)
		for fname,rect in vals:
			slname = os.path.join(ddname, os.path.basename(fname))
			im = Image.open(fname)
			sz = im.size
			coef = sz[0] / float(sz[1])
			nsz = (180, int(180 / coef))
			scale = nsz[0] / float(sz[0])
			nrect = [int(v) * scale for v in rect]
			nrect[2] += nrect[0]
			nrect[3] += nrect[1]
			if not os.path.exists(slname):
				im = im.resize(nsz)
			else:
				im = Image.open(slname)
			draw = ImageDraw.Draw(im)
			draw.rectangle(nrect, outline=(255,0,0))
			del draw
			im.save(slname)
#				os.symlink(fname, slname)
