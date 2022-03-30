# pnger
### Convert data into, and back out of, functioning PNG format images
![preview](https://i.ibb.co/MRp7GVw/test.png)

No dependencies outside of stdlib! Doesn't even require PIL/Pillow.

pnger converts arbitrary binary data in and out of png format.  Call it from command line or
import it and use `png_to_file(input, output)` and `file_to_png(input, output)`
since data is first converted to base64, it works with just about anything ive tried (ttf fonts, mp3s, binary executables...), even into
the hundreds of megabytes, without corruption.  Shoutout to 'bin2png' and 'pypng'!
I learned (most) everything from these two projects: https://github.com/ESultanik/bin2png and https://github.com/drj11/pypng


To use:

`python3 pnger.py <input file> outputfilename.png` 

To convert a PNG back to data:

`python3 pnger.py pngfile.png <output file>`


...what's super cool is that the output image ends up smaller! than the input file, due to zlib compression:
```
user@x230:~/pngerstudy$ du  test.png tmp.mp3 
5732	test.png
5780	tmp.mp3
```
