# pnger
### Convert data into, and back out of, functioning PNG format images

No dependencies outside of stdlib! Doesn't even require PIL/Pillow.

pnger converts arbitrary binary data in and out of png format.  Call it from command line or
import it and use `png_to_file(input, output)` and `file_to_png(input, output)`
since data is first converted to base64, it works with just about anything ive tried, even into
the hundreds of megabytes, without corruption.  Shoutout to 'bin2png' and 'pypng'!
I learned (most) everything from these two projects: https://github.com/ESultanik/bin2png and https://github.com/drj11/pypng


To use:

`python3 pnger.py <input file> outputfilename.png` 

To convert a PNG back to data:

`python3 pnger.py pngfile.png <output file>`

