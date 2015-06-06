# ColorPro

A small tool for converting colors - mainly for transferring from the nearly ideal CIECAM02 standard to display (sRGB/Hex) and print (Lab Colors).


## Dependencies

- [NumPy](http://www.numpy.org/)
- [SciPy](http://www.scipy.org/)
- [Colour Science](http://colour-science.org/)


## Installation

You can install colorpro via "pip" like this:

```bash
$ pip3 install colorpro
```

Alternatively you can clone the repository and install via:

```bash
$ python3 setup.py install
```

## Usage

Just pass a file with colors to `colorpro`

```bash
$ colorpro file-with-colors.txt
```

### Input

Example for input file:

```
dark-teal: 218, 15, 20
darker-teal: 218, 25, 30
vibrant-teal: 218, 35, 40
light-teal: 218, 85, 15
white-teal: 218, 90, 10
```

The formatting is:

- Hue (h)
- Lightness (J)
- Chroma (C)

which is a little re-ordered when compared to the "original" signature of `LCh`.


### Output

By default `colorpro` puts out a series of [Scss](http://sass-lang.com/) variables e.g.

```
$dark-teal: #19363e;
$darker-teal: #1f5866;
$vibrant-teal: #15788d;
$light-teal: #cfe4eb;
$white-teal: #e1edf1;
```

One great trick on Mac OS to copy the result to the clipboard:

```
colorpro file-with-colors.txt | pbcopy
```

Now just paste the result into your editor e.g. the file with the Sass variables.

There is also an output of D50 LAB colors via the `--output print` flag:

```
dark-teal = 21, -9, -15
darker-teal = 34, -15, -23
vibrant-teal = 46, -20, -31
light-teal = 89, -8, -24
white-teal = 93, -5, -22
```

For usage in "Affinity Designer" which in version 1.2 seems to use LAB colors in D65 you can use the `--output affinity` flag:

```
dark-teal = 21, -8, -8
darker-teal = 34, -14, -13
vibrant-teal = 46, -19, -19
light-teal = 89, -6, -6
white-teal = 93, -3, -3
```

Maybe adding exporting color palettes would be a nice addon for the future.

You can also output all values at once via the `--output text` flag:

```
NAME      : dark-teal
CAM-65    : 218.00,  15.00,  20.00
XYZ       :   2.60,   3.22,   5.06
LAB-50/2° :  20.89,  -9.13, -15.26
HLC-50/2° : 239.10,  20.89,  17.78
LAB-65/2° :  20.89,  -8.41,  -8.29
HLC-65/2° : 224.60,  20.89,  11.81
sRGB      :  24.63,  54.29,  62.13
HEX       : #19363e

NAME      : darker-teal
CAM-65    : 218.00,  25.00,  30.00
XYZ       :   6.47,   8.25,  13.81
LAB-50/2° :  34.50, -14.52, -23.15
HLC-50/2° : 237.91,  34.50,  27.33
LAB-65/2° :  34.50, -13.54, -13.42
HLC-65/2° : 224.75,  34.50,  19.07
sRGB      :  31.25,  88.11, 101.97
HEX       : #1f5866

NAME      : vibrant-teal
CAM-65    : 218.00,  35.00,  40.00
XYZ       :  11.75,  15.42,  27.37
LAB-50/2° :  46.20, -20.22, -31.21
HLC-50/2° : 237.06,  46.20,  37.19
LAB-65/2° :  46.20, -19.03, -18.98
HLC-65/2° : 224.93,  46.20,  26.88
sRGB      :  20.55, 119.66, 140.53
HEX       : #15788d

NAME      : light-teal
CAM-65    : 218.00,  85.00,  15.00
XYZ       :  68.40,  74.76,  89.44
LAB-50/2° :  89.28,  -7.86, -23.93
HLC-50/2° : 251.81,  89.28,  25.19
LAB-65/2° :  89.28,  -5.72,  -5.79
HLC-65/2° : 225.36,  89.28,   8.13
sRGB      : 206.65, 228.10, 235.04
HEX       : #cfe4eb

NAME      : white-teal
CAM-65    : 218.00,  90.00,  10.00
XYZ       :  77.01,  82.71,  95.02
LAB-50/2° :  92.89,  -5.43, -21.89
HLC-50/2° : 256.06,  92.89,  22.55
LAB-65/2° :  92.89,  -3.20,  -3.38
HLC-65/2° : 226.57,  92.89,   4.65
sRGB      : 224.70, 236.72, 240.87
HEX       : #e1edf1
```


## Assumptions

We implemented this with a few assumption (color stuff is hard and we tried hard to simplify things):

- CIECAM02 is better than CIELAB because of improved distance between color hues.
- Typical lightning should be oriented on a typical office space - makes sense when designing web pages/apps mainly.
- An observer of 2° is a good choice. It is the default for CIECAM02 and also makes sense for smaller viewing areas like Smartphones.
- The typical office space has about 500 lux with an average lighting surrounding.
- D65 white point is the default for sRGB which is our most typical output scenario (general display profile)
- D50 is used for LAB output as this is the default whitepoint handling for offset printing
- In the LAB colorspace there is an alternative declaration called `Lch`, but as the signature is pretty inconvenient we prefer the `HCL` variant.
- Input for CIECAM was improved in the same way: `JCh` => `hJC`. The original was identical to the signature of the `Lch` color scheme and follow the same transformation as the `HLC` color scheme.
