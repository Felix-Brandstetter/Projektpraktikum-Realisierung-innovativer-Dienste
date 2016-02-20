#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# © 2013-15: jbarlow83 from Github (https://github.com/jbarlow83)
#
#
# Use Leptonica to detect find and remove page skew.  Leptonica uses the method
# of differential square sums, which its author claim is faster and more robust
# than the Hough transform used by ImageMagick.

from __future__ import print_function, absolute_import, division
import argparse
import sys
import os
import logging
from tempfile import TemporaryFile
from ctypes.util import find_library
from .lib._leptonica import ffi
from functools import lru_cache

lept = ffi.dlopen(find_library('lept'))

logger = logging.getLogger(__name__)


def stderr(*objs):
    """Python 2/3 compatible print to stderr.
    """
    print("leptonica.py:", *objs, file=sys.stderr)


class LeptonicaErrorTrap(object):
    """Context manager to trap errors reported by Leptonica.

    Leptonica's error return codes are unreliable to the point of being
    almost useless.  It does, however, write errors to stderr provided that is
    not disabled at its compile time.  Fortunately this is done using error
    macros so it is very self-consistent.

    This context manager redirects stderr to a temporary file which is then
    read and parsed for error messages.  As a side benefit, debug messages
    from Leptonica are also suppressed.

    """
    def __enter__(self):
        self.tmpfile = TemporaryFile()

        # Save the old stderr, and redirect stderr to temporary file
        self.old_stderr_fileno = os.dup(sys.stderr.fileno())
        os.dup2(self.tmpfile.fileno(), sys.stderr.fileno())
        return

    def __exit__(self, exc_type, exc_value, traceback):
        # Restore old stderr
        os.dup2(self.old_stderr_fileno, sys.stderr.fileno())

        # Get data from tmpfile (in with block to ensure it is closed)
        with self.tmpfile as tmpfile:
            tmpfile.seek(0)  # Cursor will be at end, so move back to beginning
            leptonica_output = tmpfile.read().decode(errors='replace')

        # If there are Python errors, let them bubble up
        if exc_type:
            logger.warning(leptonica_output)
            return False

        # If there are Leptonica errors, wrap them in Python excpetions
        if 'Error' in leptonica_output:
            if 'image file not found' in leptonica_output:
                raise FileNotFoundError()
            if 'pixWrite: stream not opened' in leptonica_output:
                raise LeptonicaIOError()
            raise LeptonicaError(leptonica_output)

        return False


class LeptonicaError(Exception):
    pass


class LeptonicaIOError(LeptonicaError):
    pass


class Pix:
    """Wrapper around leptonica's PIX object.

    Leptonica uses referencing counting on PIX objects. Also, many Leptonica
    functions return the original object with an increased reference count
    if the operation had no effect (for example, image skew was found to be 0).
    This has complications for memory management in Python. Whenever Leptonica
    returns a PIX object (new or old), we wrap it in this class, which
    registers it with the FFI garbage collector. pixDestroy() decrements the
    reference count and only destroys when the last reference is removed.

    Leptonica's reference counting is not threadsafe. This class can be used
    in a threadsafe manner if a Python threading.Lock protects the data.
    """

    def __init__(self, cpix):
        self.cpix = ffi.gc(cpix, Pix._pix_destroy)

    def __repr__(self):
        if self.cpix:
            s = "<leptonica.Pix image size={0}x{1} depth={2} at 0x{3:x}>"
            return s.format(self.cpix.w, self.cpix.h, self.cpix.d,
                            int(ffi.cast("intptr_t", self.cpix)))
        else:
            return "<leptonica.Pix image NULL>"

    def __getstate__(self):
        state = {}
        if self.cpix.colormap:
            raise NotImplementedError('colormap')
        else:
            state['colormap'] = None
        if self.cpix.text:
            state['text'] = ffi.string(self.cpix.text)[:]
        else:
            state['text'] = None
        if self.cpix.data:
            data_bytes = self.cpix.wpl * self.cpix.h * 4
            state['data'] = ffi.buffer(self.cpix.data, data_bytes)[:]
        else:
            state['data'] = None

        cpix_copy = ffi.new('PIX *')
        ffi.buffer(cpix_copy)[:] = self.cpix
        cpix_copy.text = ffi.NULL
        cpix_copy.colormap = ffi.NULL
        cpix_copy.data = ffi.NULL

        state['cpix'] = ffi.buffer(self.cpix)[:]
        return state

    def __setstate__(self, state):
        import array
        self.cpix = ffi.new('PIX *')
        ffi.buffer(self.cpix)[:] = state['cpix']

        data_array = array.array('I', state['data'])
        self.cpix.data = ffi.from_buffer(data_array)
        self.cpix.text = ffi.new('char[]', state['text'])
        self.cpix.colormap = ffi.NULL

    @property
    def width(self):
        return self.cpix.w

    @property
    def height(self):
        return self.cpix.h

    @classmethod
    def read(cls, filename):
        """Load an image file into a PIX object.

        Leptonica can load TIFF, PNM (PBM, PGM, PPM), PNG, and JPEG.  If
        loading fails then the object will wrap a C null pointer.
        """
        with LeptonicaErrorTrap():
            return cls(lept.pixRead(
                filename.encode(sys.getfilesystemencoding())))

    def write_implied_format(
            self, filename, jpeg_quality=0, jpeg_progressive=0):
        """Write pix to the filename, with the extension indicating format.

        jpeg_quality -- quality (iff JPEG; 1 - 100, 0 for default)
        jpeg_progressive -- (iff JPEG; 0 for baseline seq., 1 for progressive)
        """
        with LeptonicaErrorTrap():
            lept.pixWriteImpliedFormat(
                filename.encode(sys.getfilesystemencoding()),
                self.cpix, jpeg_quality, jpeg_progressive)

    def deskew(self, reduction_factor=0):
        """Returns the deskewed pix object.

        A clone of the original is returned when the algorithm cannot find a
        skew angle with sufficient confidence.

        reduction_factor -- amount to downsample (0 for default) when searching
            for skew angle
        """
        with LeptonicaErrorTrap():
            return Pix(lept.pixDeskew(self.cpix, reduction_factor))

    def scale(self, scalex, scaley):
        "Returns the pix object rescaled according to the proportions given."
        with LeptonicaErrorTrap():
            return Pix(lept.pixScale(self.cpix, scalex, scaley))

    def rotate180(self):
        with LeptonicaErrorTrap():
            return Pix(lept.pixRotate180(ffi.NULL, self.cpix))

    def find_skew(self):
        """Returns a tuple (deskew angle in degrees, confidence value).

        Returns (None, None) if no angle is available.
        """
        with LeptonicaErrorTrap():
            angle = ffi.new('float *', 0.0)
            confidence = ffi.new('float *', 0.0)
            result = lept.pixFindSkew(self.cpix, angle, confidence)
            if result == 0:
                return (angle[0], confidence[0])
            else:
                return (None, None)

    @staticmethod
    def correlation_binary(pix1, pix2):
        if get_leptonica_version() < 'leptonica-1.72':
            # Older versions of Leptonica (pre-1.72) have a buggy
            # implementation of pixCorrelationBinary that overflows on larger
            # images.
            pix1_count = ffi.new('l_int32 *', 0)
            pix2_count = ffi.new('l_int32 *', 0)
            pixn_count = ffi.new('l_int32 *', 0)
            tab8 = lept.makePixelSumTab8()  # Small memory leak on each call

            lept.pixCountPixels(pix1.cpix, pix1_count, tab8)
            lept.pixCountPixels(pix2.cpix, pix2_count, tab8)
            pixn = Pix(lept.pixAnd(ffi.NULL, pix1.cpix, pix2.cpix))
            lept.pixCountPixels(pixn.cpix, pixn_count, tab8)

            # Python converts these int32s to larger units as needed
            # to avoid overflow. Overflow happens easily here.
            correlation = (
                    (pixn_count[0] * pixn_count[0]) /
                    (pix1_count[0] * pix2_count[0])
                    )
            return correlation
        else:
            correlation = ffi.new('float *', 0.0)
            result = lept.pixCorrelationBinary(pix1.cpix, pix2.cpix,
                                               correlation)
            if result != 0:
                raise LeptonicaError("Correlation failed")
            return correlation[0]

    @staticmethod
    def _pix_destroy(pix):
        ptr_to_pix = ffi.new('PIX **', pix)
        lept.pixDestroy(ptr_to_pix)
        # print('pix destroy ' + repr(pix))


@lru_cache(maxsize=1)
def get_leptonica_version():
    """Get Leptonica version string.

    Caveat: Leptonica expects the caller to free this memory.  We don't,
    since that would involve binding to libc to access libc.free(),
    a pointless effort to reclaim 100 bytes of memory.
    """
    return ffi.string(lept.getLeptonicaVersion()).decode()


def deskew(infile, outfile, dpi):
    try:
        pix_source = Pix.read(infile)
    except LeptonicaIOError:
        raise LeptonicaIOError("Failed to open file: %s" % infile)

    if dpi < 150:
        reduction_factor = 1  # Don't downsample too much if DPI is already low
    else:
        reduction_factor = 0  # Use default
    pix_deskewed = pix_source.deskew(reduction_factor)

    try:
        pix_deskewed.write_implied_format(outfile)
    except LeptonicaIOError:
        raise LeptonicaIOError("Failed to open destination file: %s" % outfile)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Python wrapper to access Leptonica")

    subparsers = parser.add_subparsers(title='commands',
                                       description='supported operations')

    parser_deskew = subparsers.add_parser('deskew')
    parser_deskew.add_argument('-r', '--dpi', dest='dpi', action='store',
                               type=int, default=300, help='input resolution')
    parser_deskew.add_argument('infile', help='image to deskew')
    parser_deskew.add_argument('outfile', help='deskewed output image')
    parser_deskew.set_defaults(func=deskew)

    args = parser.parse_args()

    if get_leptonica_version() != u'leptonica-1.69':
        print("Unexpected leptonica version: %s" % getLeptonicaVersion())

    args.func(args)


def test_skew_angle():
    from PIL import Image, ImageDraw
    from tempfile import NamedTemporaryFile

    im = Image.new(mode='1', size=(1000, 1000), color=1)

    draw = ImageDraw.Draw(im)
    for n in range(20):
        draw.line([(50, 25 + 50*n), (950, 25 + 50*n)], width=1)
    del draw

    test_angles = [0.1 * ang for ang in range(1, 10)] + \
                  [float(ang) for ang in range(1, 7)]
    test_angles += [-ang for ang in test_angles]
    test_angles = sorted(test_angles)

    for rotate_angle in test_angles:
        rotated_im = im.rotate(rotate_angle)
        with NamedTemporaryFile(prefix='lept-skew', suffix='.png', delete=True) as tmpfile:
            rotated_im.save(tmpfile)
            pix = pixRead(tmpfile.name)
            angle, confidence = pixFindSkew(pix)
            print('{0} {1}  {2}'.format(rotate_angle, angle, confidence), file=sys.stderr)


