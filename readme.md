# ColorPro

A small tool for converting colors - mainly for transferring from the nearly ideal CIECAM02 standard to display (sRGB/Hex) and print (Lab Colors).

## Installation

You can install colorpro via "pip" like this:

```bash
$ pip3 install colorpro
```

Alternatively you can clone the repository and install via:

```bash
$ python3 setup.py install
```

## Dependencies

- [NumPy](http://www.numpy.org/)
- [SciPy](http://www.scipy.org/)
- [Colour Science](http://colour-science.org/)


## Assumptions

Making color convertions under a few assumption:

- CIECAM02 is better than CIELAB because of improved distance between color hues.
- Typical lightning should be oriented on a typical office space - makes sense when designing web pages/apps mainly.
- An observer of 2° is a good choice. It is the default for CIECAM02 and also makes sense for smaller viewing areas like Smartphones.
- The typical office space has about 500 lux with an average lighting surrounding.
- D65 white point is the default for sRGB which is our most typical output scenario (general display profile)
- D50 is used for LAB output as this is the default whitepoint handling for offset printing

