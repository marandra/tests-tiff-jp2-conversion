#!/usr/bin/env python2.7

import skimage.io as io
import glymur
from glob import glob
import time
from libxmp import XMPFiles
import uuid
start = time.time()

files = glob('*IMAGE*/*.tif*')

nfiles = len(files)

for file in files:
    #name for jp2 image
    fjp2 = "{}.jp2".format(file.split('.tif')[0])
    #read metadata from tiff
    xf = XMPFiles()
    xf.open_file(file)
    xmp = xf.get_xmp()
    #read bitmap from tiff
    image = io.imread(file, plugin='tifffile')
    #write bitmap to jp2 image 
    jp2 = glymur.Jp2k(fjp2, 'wb')
    jp2[:] = image
    #append metadata in uuid box
    xmp_uuid = uuid.UUID('be7acfcb-97a9-42e8-9c71-999491e3afac')
    box = glymur.jp2box.UUIDBox(xmp_uuid, str(xmp))
    jp2.append(box)
    #write second resolution as thumbnail
    jt = glymur.Jp2k("thumb"+fjp2, 'wb')
    jt[:] = jp2.read(rlevel=2)

end = time.time()
print "Time:{:.0e}s Files:{} Time/Files:{:.1e}s/file".format(end-start, nfiles, (end-start)/nfiles)
