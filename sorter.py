#!/usr/bin/env python

import os

BOXFNAME = 'bboxes.txt'
CLSFNAME = 'data/classnames_VOC.txt'
DESTDIR = 'sorted'

cls_only = ['cat', 'bird']

clslst = [l.strip() for l in file(CLSFNAME).readlines()]

clsf = {}
for line in file(BOXFNAME):
	fname,x1,y1,x2,y2,prob,dummy,cls = line.split()
	if cls not in clsf:
		clsf[cls] = []
	clsf[cls].append(fname)

for cls,fnames in clsf.items():
	clsname = clslst[int(cls)]
	if clsname in cls_only or not cls_only:
		ddname = os.path.join(DESTDIR, clsname)
		if not os.path.exists(ddname):
			os.makedirs(ddname)
		for fname in fnames:
			slname = os.path.join(ddname, os.path.basename(fname))
			if not os.path.exists(slname):
				os.symlink(fname, slname)
