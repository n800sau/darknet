#!/usr/bin/env python

import sys, os, glob, subprocess, imghdr

# first parameter is a directory
BBOXNAME = './bboxes.txt'
DFLNAME = 'filelist.lst'
DNFLNAME = 'processed.lst'
SRCFLIST = 'filelist_src.lst'


processed = [l.strip() for l in file(DNFLNAME, 'r').readlines()] if (os.path.exists(DNFLNAME)) else []

dfl = file(DFLNAME, 'w')

if len(sys.argv) > 1:

	for root,dirnames,filenames in os.walk(os.path.expanduser(sys.argv[1]), followlinks=True):
		for fname in filenames:
			fname = os.path.join(root, fname)
			if fname not in processed:
				if imghdr.what(fname) in ('jpeg', 'png'):
					dfl.write(fname + '\n')
else:

	for fname in file(SRCFLIST):
		if fname.strip() not in processed:
			dfl.write(fname)

dfl.close()

darknet = subprocess.Popen([
		'./darknet',
		'yolo',
		'test_on_filelist',
		'cfg/yolo-tiny.cfg',
		'yolo-tiny.weights',
		'-c_filelist', '-',
		'-c_classes', 'data/classnames_VOC.txt',
		'-write', '1',
		'-dest', BBOXNAME
		],
		stdin=subprocess.PIPE,
		stdout=subprocess.PIPE
	)

dnfl = file(DNFLNAME, 'a')
for line in file(DFLNAME, 'r'):
	print 'Feed %s' % line
	darknet.stdin.write(line)
	dnfl.write(line)
	dnfl.flush()
	while not darknet.poll():
		reply = darknet.stdout.readline()
		print reply,
		if reply.strip() == 'Processed!':
			break
	if darknet.poll():
		raise Exception('premature exit, status:%d' % darknet.returncode)
dnfl.close()
darknet.stdin.close()
darknet.wait()
print'Finished'
