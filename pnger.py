#!/usr/bin/python3


# pnger converts arbitrary binary data in and out of png format.  Call it from command line or
# import it and use png_to_file(input, output) and file_to_png(input, output)
# since data is first converted to base64, it works with just about anything ive tried, even into
# the hundreds of megabytes, without corruption.  Shoutout to 'bin2png' and 'pypng'!
# Much mooched from https://github.com/ESultanik/bin2png and https://github.com/drj11/pypng/
import math
import sys
import io, zlib
import struct
import base64
from hashlib import md5
import os
############################### w00t #########################################################


def png_to_file(infile,outfile):
    infile = open(infile, 'rb')
    alldata = []
    # sig
    sig = infile.read(8)
    #print(f'sig: {sig}')
    if not sig:
        return None
    count = 0
    while True:
        count += 1
        x = infile.read(8)
        if not x:
            print("png broken, we should have hit IEND")
            break
        length, type = struct.unpack('!I4s', x)
        if type == b'IHDR':
            data = infile.read(length)
            checksum = infile.read(4)
            width, height, null, null, null, null, null = struct.unpack("!2I5B", data)
            #print(f'{type} length: {length} width: {width} height: {height}')
        if type == b'IEND':
            #print('breaking at IEND')
            break
        if type != b'IDAT':
            continue
        alldata.append(infile.read(length))
        checksum = infile.read(4)
    infile.close()
    d = zlib.decompressobj()
    raw = []
    for data in alldata:
        raw.append(bytearray(d.decompress(data)))
    raw.append(bytearray(d.flush()))
    pix_buffer = 0
    nums = []
    for line in raw:
        for segment in line:
            if segment != 255:
                nums.append(segment)
    bs = [chr(i) for i in nums]
    z=''
    for i in bs:
        z+=i
    final = base64.b64decode(z)
    f = open(outfile,'wb')
    f.write(final)
    f.close()


def _write_chunk(out, chunk_type, data):
    assert 4 == len(chunk_type)
    out.write(struct.pack(">L", len(data)))
    out.write(chunk_type)
    out.write(data)
    checksum = zlib.crc32(chunk_type)
    checksum = zlib.crc32(data, checksum)
    out.write(struct.pack(">L", checksum))


def _rows_to_png(out, rows, size):
    out.write(bytearray([137, 80, 78, 71, 13, 10, 26, 10]))
    header = struct.pack(">2LBBBBB", size[0], size[1], 8, 2, 0, 0, 0)
    _write_chunk(out, b"IHDR", header)
    bs = bytearray()
    for row in rows:
        bs.append(0)
        bs.extend(row)
    _write_chunk(out, b"IDAT", zlib.compress(bs))
    _write_chunk(out, b"IEND", bytearray())


def file_to_png(infile, outfile=None):
    with open(infile, 'rb') as f:
        infile = base64.b64encode(f.read())
    num_bytes = len(infile)
    num_pixels = int(math.ceil(float(num_bytes) / 3.0))
    sqrt = math.sqrt(num_pixels)
    sqrt_max = int(math.ceil(sqrt))
    dimensions = (sqrt_max, sqrt_max)
    pixels = []
    for row in range(dimensions[1]):
        pixels.append([])
    row = 0
    column = -1
    i = 0
    reader = io.BytesIO(infile)
    while True:
        b = reader.read(3)
        if not b:
            break
        column += 1
        if column >= dimensions[0]:
            column = 0
            row += 1
        color = [b[0], 255, 255]
        if len(b) > 1:
            color[1] = b[1]
        if len(b) > 2:
            color[2] = b[2]
        if not row >= dimensions[1]:
            for i in color:
                pixels[row].append(i)
    reader.close()
    if len(pixels[-1]) == 0:
        pixels.pop(-1)
    while len(pixels[-1]) < len(pixels[-2]):
        pixels[-1].append("0")
    pixels = list([(int(c) for c in row) for row in pixels])
    total_rows = len(pixels)
    with open(outfile, 'wb') as f:
        _rows_to_png(f, pixels, (dimensions[0], dimensions[1]))


def _md5sum(filename):
    m = md5()
    with open(filename, 'rb') as f:
        data = f.read(8192)
        while data:
            m.update(data)
            data = f.read(8192)
    return m.hexdigest()


def _test_output(outfile, original):
    if outfile.endswith(".png"):
        png_to_file(outfile, 'pnger_tempfile')
        og = _md5sum(original)
        temp = _md5sum('pnger_tempfile')
        print(f'{og} :: {original}\n{temp} :: output after re conversion')
        if og != temp:
            print('FAIL: Conversion back does not match original file!')
        else:
            print('Success')
        os.remove('pnger_tempfile')


if __name__ == "__main__":
    # if argv[1] is a png, convert it to a file
    if sys.argv[1].endswith(".png"):
        png_to_file(sys.argv[1], sys.argv[2])
    # if argv[1] is a file, convert it to a png
    else:
        file_to_png(sys.argv[1], sys.argv[2])
    # verify successful output by converting back and comparing
    _test_output(sys.argv[2], sys.argv[1])


