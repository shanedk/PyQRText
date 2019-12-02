# PyQRText

A Python script to display a QR code in a text screen using the Unicode block characters so that two rows are displayed on a single line.

## So, what do I do?

Run the `PyQRText.py` file passing through the text you want to encode as an argument.

Example:

```
PyQRText.py "This is the QR data."
```

## Anything else I need to know?

Yes: most QR code readers require that the QR code be a dark color on a lighter background. Terminals generally tend to be dark with light text, so the default will work fine. ***However***, if you're using a terminal that displays dark text on a light background, this will cause many QR readers to fail. So pass in the word "light" (not case-sensitive) as a second argument and the script will adjust for this.

Example:

```
PyQRText.py "This is the QR data." "light"
```

## Built With

* [PyQRNative](https://code.google.com/archive/p/pyqrnative/) - Used to generate the QR data. This is a customized version with fixes for Python 3.x and the image generation commented out, as it's not needed. 

## Authors

* **Shane D. Killian** - *Initial work* - [ShaneDK](https://github.com/shanedk)

## License

**CC0:** Creative Commons 0. This work is in the public domain. See [COPYING.txt](COPYING.tct)

**Note:** The included PyQRNative.py is licensed under the MIT License. See the notice inside the file.