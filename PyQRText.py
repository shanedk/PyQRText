#!/usr/bin/python
#
# PyQRText.py
# Written in 2019 by Shane D. Killian
#
# To the extent possible under law, the author(s) have dedicated all copyright
# and related and neighboring rights to this software to the public domain
# worldwide. This software is distributed without any warranty. You should have
# received a copy of the CC0 Public Domain Dedication along with this software.
# If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#
# The word "QR Code" is registered trademark of
# DENSO WAVE INCORPORATED
# https://www.qrcode.com/en/patent.html
#
# The purpose of this script is to create a QR code suitable for displaying
# on text-only screens using Unicode block codes so that no graphic libraries
# need to be loaded.
#
# The main feature of this script as opposed to other text-based QR generators
# is that each line of text represents two rows of the QR code, meaning more
# complex QR codes can fit on a single screen.
#
# The script takes two arguments. The first is simply the data to be encoded.
# The second is optional. If it doesn't exist or is anything other than the
# word "light", then dark mode is assumed, in other words, the current terminal
# is dark with light text. If the terminal is light with dark text, pass the
# word "light" as an argument. This is important for proper scanning because
# most QR readers only work with a dark QR code on a light background.
#
# The maximum length of the input is 520 binary characters. Most terminal
# screens cannot display QR codes larger than this.
#
import sys
from PyQRNative import QRCode, QRErrorCorrectLevel

try:
    text = sys.argv[1]
except:
    print('USAGE: python', sys.argv[0], 'content light/[dark]')
    sys.exit(1)

if len(sys.argv) > 2:
    if str(sys.argv[2]).lower() == 'light':
        darkmode = False
    else:
        darkmode = True
else:
    darkmode = True


# These are the QR code levels at the lowest level error correction, "Level L."
# See the QR code documentation for more information. Again, we max out at 520
# binary characters.
#
levels = [17, 32, 53, 78, 106, 134, 154, 192, 230, 271, 321, 367, 425, 458, 520]
level = None

for i in zip(range(1, 16), levels):
    if len(text) <= i[1]:
        level = i[0]
        break

if level is None:
    print('ERROR: Content is too long (520 characters maximum).')
    sys.exit(1)


# Next, we get the data for the QR code.
qr = QRCode(level, QRErrorCorrectLevel.L)
qr.addData(text)
qr.make()

# We use different block elements depending on whether or not we're in block
# mode. Note that all of these are Unicode except for the space.
if not darkmode:
    char00 = u'\u2588'
    char01 = u'\u2580'
    char10 = u'\u2584'
    char11 = ' '
else:
    char00 = ' '
    char01 = u'\u2584'
    char10 = u'\u2580'
    char11 = u'\u2588'

# This is actually both the width and the height, since QR codes are square.
width = qr.moduleCount

# We start off with a blank line to have a sufficient margin at the top.
print(char11 * (width + 4))

# Now we display the actual QR data two rows at a time.
for y in range(0, width, 2):

    # We'll start off with a two-character left margin.
    row = char11 * 2

    # Now we go through the width of the QR data.
    for x in range(width):

        # We need to check to see if we've ended on an odd row, otherwise
        # we'll go out of bounds.
        if y == width-1:
            if qr.isDark(y, x):
                row += char01
            else:
                row += char11

        # Otherwise, we get the data for the next two rows and use the block
        # characters we defined above to display them.
        else:
            if qr.isDark(y, x) and qr.isDark(y+1, x):
                row += char00
            elif qr.isDark(y, x) and not qr.isDark(y+1, x):
                row += char01
            elif not qr.isDark(y, x) and qr.isDark(y+1, x):
                row += char10
            else:
                row += char11

    # Then we display the two-character right margin.
    row += char11 * 2

    # We're done with this row, so let's print it.
    print(row)

# And we finish with the margin on the bottom.
print(char11 * (width + 4))
