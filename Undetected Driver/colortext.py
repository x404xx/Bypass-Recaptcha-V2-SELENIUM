from colored import attr, fg


#! Colored code
yellow = fg("yellow")
white = fg("white")
blue = fg(20)
cyan = fg('cyan')
green = fg(46)
red = fg("red")
purple = fg("purple_1a")
grey = fg("grey_27")
org = fg('orange_red_1')
bold = attr("bold")
reset = attr("reset")

INFO = f'{yellow}[INFO]{reset}'
WARNING = f'{red}[WARNING]{reset}'
PROXY = f'{yellow}[PROXY]{reset}'
SUCCESS = f'{green}[SUCCESS]{reset}'