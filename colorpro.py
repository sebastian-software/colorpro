# ColorPro - Color Compution Helper
# Copyright 2015 Sebastian Software GmbH, Germany

__version__ = "0.2"

import sys
import re
import colour
import numpy

# Observers
# - Classic default was 2° (from 1931)
# - Newer addition of 10° (from 1964)
#
# Das 2°-Gesichtsfeld entspricht der Größe der Netzhautregion mit der dichtesten Packung von
# Zapfen (Farbrezeptoren) im menschlichen Auge. Das normale Sichtfeld der menschlichen Wahrnehmung
# ist allerdings größer als dieser 2°-Bereich.
#
# 1964 wurde deshalb das System für einen Normalbeobachter mit 10°-Sichtfeld eingeführt.
# Als CIE-System wird auch heute noch das 2°-Sichtfeld-System unterstellt, sofern nichts
# anderes angegeben ist.
#
# Da die heutigen Dimensionen für farbige Kleinbildschirme, zum Beispiel für Smartphones,
# sehr gering ausfallen, gewinnt der 2°-Normalbeobachter von 1931 für kleine Betrachtungswinkel
# wieder an Bedeutung. Für Print-Produkte mit einem normalerweise größeren Betrachungswinkel,
# z.B. einem A4-Format, ist 10° daher interessanter.
#
# Constants for typical illuminants
#
# D50:
# - bevorzugt in der Druckindustrie.
# - Weißpunkt für Wide-Gamut-RGB und Color-Match-RGB
#
# D65:
# - entspricht etwa einem grau verhangenen Himmel
# - genutzt wird dieses Normlicht als Weißpunkt für sRGB, Adobe-RGB und die PAL/SECAM-TV-Norm

OBSERVER_2 = colour.ILLUMINANTS.get('CIE 1931 2 Degree Standard Observer')
# OBSERVER_10 = colour.ILLUMINANTS.get('CIE 1964 10 Degree Standard Observer')

ILLUMINANT_D50_2 = OBSERVER_2.get('D50')
# ILLUMINANT_D50_10 = OBSERVER_10.get('D50')
ILLUMINANT_D65_2 = OBSERVER_2.get('D65')
# ILLUMINANT_D65_10 = OBSERVER_10.get('D65')

WHITEPOINT_D50_2 = colour.xyY_to_XYZ([ILLUMINANT_D50_2[0], ILLUMINANT_D50_2[1], 1]) * 100
# WHITEPOINT_D50_10 = colour.xyY_to_XYZ([ILLUMINANT_D50_10[0], ILLUMINANT_D50_10[1], 1]) * 100
WHITEPOINT_D65_2 = colour.xyY_to_XYZ([ILLUMINANT_D65_2[0], ILLUMINANT_D65_2[1], 1]) * 100
# WHITEPOINT_D65_10 = colour.xyY_to_XYZ([ILLUMINANT_D65_10[0], ILLUMINANT_D65_10[1], 1]) * 100

# Typische Beleuchtungsstärken:
# - Heller Sonnentag       100.000 lx
# - Bedeckter Sommertag     20.000 lx
# - Im Schatten im Sommer   10.000 lx
# - Bedeckter Wintertag      3.500 lx
# - Elite-Fußballstadion     1.400 lx
# - Beleuchtung TV-Studio    1.000 lx
# - Büro-/Zimmerbeleuchtung    500 lx
# - Flurbeleuchtung            100 lx
# - Wohnzimmer[6]               50 lx
# - Straßenbeleuchtung          10 lx
# - Kerze ca. 1 Meter entfernt   1 lx

# 1000 lux: Surface colour evaluation in a light booth
# 500 Lux = Viewing self-luminous display under office illumination
# 38 Lux = Viewing self-luminous display at home
# 0 Lux = Viewing slides in dark room

# Via: http://sutlib2.sut.ac.th/sut_contents/H95009/DATA/5637_61.PDF
# - Average / Booth: 1000 Lux => white luminance=318.30 cd/m2 => La=63.66 => Yb=18
# - Average / Office: 500 Lux => white luminance=80 cd/m2 => La=16 => Yb=18
# - Dim: 100 Lux => white luminance=80 cd/m2 => La=16 => Yb=18
# - Dark: 0 Lux => white luminance=150 cd/m2 => La=47.74 => Yb=18

# Via: Buch "Color Appearance Models" von Mark D. Fairchild
# - Average: 1000 Lux => white luminance=318.30 => La=60 => Sr=1
# - Average: 500 Lux => white luminance=80 => La=15 => Sr=2
# - Dim: 38 Lux => white luminance=80 => La=20 => Sr=0.15

# Via: http://scanline.ca/ciecam02/ciecam02-0.3.h und http://scanline.ca/ciecam02/
# - Average = 64 Lux => La=4 => yb=20 (for sRGB)

# Background Relative Luminance (y_b)
# - Typical grey - 20% of the chosen whitepoint (100 is the luminance of the whitepoints (both D50 and D65) => 20)
# - 20 (pcolor, chromatist)
# - 19 und 22 ('Illumination, Color and Imaging' by P. Bodrogi, T. Q. Khan)
# - 18 (http://newsgroups.derkeiler.com/Archive/Sci/sci.engr.color/2009-01/msg00009.html)
# - 20 ('Color Appearance Models' by Fairchild)
# - 20 (https://groups.google.com/forum/#!topic/sci.engr.color/3P9DXaCAWAI)
background_luminance = 18

# Adapting field *luminance* (L_A) in `cd/m^2`.
# - 318.30 (Fairchild)
# - 328.31 (Python Colormath - might be a typo)
# - 40 (ColoristJS; )
# - 64 (pcolor)
# - 4 (http://scanline.ca/ciecam02/ciecam02-0.3.h und http://scanline.ca/ciecam02/)
# - 230 ('Illumination, Color and Imaging' by P. Bodrogi, T. Q. Khan)
# - 2000/200/20/2 (http://newsgroups.derkeiler.com/Archive/Sci/sci.engr.color/2009-01/msg00009.html)
adapting_luminance = 16

# Whether light should follow human logic
# Default = False
discount_illuminant = False

# Viewing Conditions
# Default = Average
surround = colour.CIECAM02_VIEWING_CONDITIONS['Average']


def rgb_to_hex(RGB):
  """
  Improved rounding for hex values compared to triplet method in colour-science.
  """

  RGB = numpy.asarray(RGB)

  to_HEX = numpy.vectorize('{0:02x}'.format)

  RGB = numpy.array([ round(x * 255) for x in RGB ])

  HEX = to_HEX((RGB).astype(numpy.uint8)).astype(object)
  HEX = numpy.asarray('#') + HEX[..., 0] + HEX[..., 1] + HEX[..., 2]

  return HEX


def floatlist(value):
  """
  Generic color value number formatting with 000.00 pattern.
  """

  return "{0:6.2f}, {1:6.2f}, {2:6.2f}".format(*[round(x, 2) for x in value])


def intlist(value):
  """
  Generic color value number formatting with 000 pattern.
  """

  return "{0}, {1}, {2}".format(*[int(round(x)) for x in value])


def compute(name, hue, lightness, saturation, output="scss"):
  """
  Outputs different conversations of the given CIECAM02 input.
  Uses CIECAM with the same "signature" as HLC
  """

  xyz = colour.CIECAM02_to_XYZ(
    lightness, saturation, hue,
    WHITEPOINT_D65_2, adapting_luminance, background_luminance,
    surround = surround,
    discount_illuminant = discount_illuminant
  )
  xyz_trans = [ value / 100 for value in xyz ]

  #lab_65_10 = colour.XYZ_to_Lab(xyz_trans, illuminant=ILLUMINANT_D65_10)
  #lch_65_10 = colour.Lab_to_LCHab(lab_65_10)
  #hlc_65_10 = [lch_65_10[2], lch_65_10[0], lch_65_10[1]]

  lab_65_2 = colour.XYZ_to_Lab(xyz_trans, illuminant=ILLUMINANT_D65_2)
  lch_65_2 = colour.Lab_to_LCHab(lab_65_2)
  hlc_65_2 = [lch_65_2[2], lch_65_2[0], lch_65_2[1]]

  #lab_50_10 = colour.XYZ_to_Lab(xyz_trans, illuminant=ILLUMINANT_D50_10)
  #lch_50_10 = colour.Lab_to_LCHab(lab_50_10)
  #hlc_50_10 = [lch_50_10[2], lch_50_10[0], lch_50_10[1]]

  lab_50_2 = colour.XYZ_to_Lab(xyz_trans, illuminant=ILLUMINANT_D50_2)
  lch_50_2 = colour.Lab_to_LCHab(lab_50_2)
  hlc_50_2 = [lch_50_2[2], lch_50_2[0], lch_50_2[1]]

  srgb = colour.XYZ_to_sRGB(xyz_trans)
  srgb_trans = [ value * 255 for value in srgb ]

  hex_trans = rgb_to_hex(srgb)

  if output == "text":
    print("NAME      :", name)
    print("CAM-65    :", floatlist([hue, lightness, saturation]))
    print("XYZ       :", floatlist(xyz))
    print("LAB-50/2° :", floatlist(lab_50_2))
    print("HLC-50/2° :", floatlist(hlc_50_2))
    print("LAB-65/2° :", floatlist(lab_65_2))
    print("HLC-65/2° :", floatlist(hlc_65_2))
    print("sRGB      :", floatlist(srgb_trans))
    print("HEX       :", hex_trans)
    print("")

  elif output == "scss":
    print("$%s: %s;" % (name, hex_trans))

  elif output == "print":
    print("%s = %s" % (name, intlist(lab_50_2)))

  elif output == "affinity":
    print("%s = %s" % (name, intlist(lab_65_2)))


LINE_FORMAT = re.compile(r'([a-zA-Z0-9-]+)\s*:\s*([0-9]+),\s*([0-9]+),\s*([0-9]+)')


def read(filename, output):
  for line in open(filename).readlines():
    line = line.strip()

    if line == "" or line.startswith("#"):
      continue

    match = LINE_FORMAT.match(line)
    if not match:
      print("Invalid: %s" % line)
      continue

    colorargs = match.groups()
    compute(colorargs[0], int(colorargs[1]), int(colorargs[2]), int(colorargs[3]), output=output)
