def convert_kelvin_to_rgb(cct_in_kelvin: float) -> list:
    """Converts color temperature (CCT) to RGB values, for CCT between 1000 and 40000.

    Accepts CCT in degrees Kelvin as an int or float; otherwise will return a TypeError.
    Returns RGB as a list of three floats, each in the range 0.0-255.0.
    Assumes a white balance of 6600K.

    Math is Neil Bartlett's algorithm, a more accurate re-mapping of Tanner Helland's data.
    Bartlett: https://www.zombieprototypes.com/?p=210
    Helland: https://tannerhelland.com/2012/09/18/convert-temperature-rgb-algorithm-code.html
    """

    from math import log

    kelvin = (lambda k: max(min(40000.0, k), 1000.0))(cct_in_kelvin)  # limits CCT range to 1000-40000
    kel = round(kelvin / 100, 3)

    def a_bx_clnx(a, b, c, x):
        """computes a+bx+cln(x); floats a, b, c, and x are given by the algorithm for each color"""
        return a + (b * x) + (c * log(x))

    if kel <= 66:
        red = 255.0
        green = a_bx_clnx(a=-155.25485562709179, b=-0.44596950469579133, c=104.49216199393888, x=kel-2)
        if kel >= 19:
            blue = a_bx_clnx(a=-254.76935184120902, b=0.8274096064007395, c=115.67994401066147, x=kel-10)
        else:
            blue = 0.0
    else:
        red = a_bx_clnx(a=351.97690566805693, b=0.114206453784165, c=-40.25366309332127, x=kel-55)
        green = a_bx_clnx(a=325.4494125711974, b=0.07943456536662342, c=-28.0852963507957, x=kel-50)
        blue = 255.0

    rgb = [red, green, blue]

    for color in rgb:
        rgb[rgb.index(color)] = (lambda n: max(min(255.0, n), 0.0))(color)  # limits output to 0.0-255.0

    return rgb
