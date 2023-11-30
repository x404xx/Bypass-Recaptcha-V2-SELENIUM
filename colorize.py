from colored import attr, fg


class Colors:
    yellow = fg('yellow')
    white = fg('white')
    blue = fg('blue_3b')
    dblue = fg('dodger_blue_2')
    cyan = fg('cyan')
    green = fg('green_1')
    sgreen = fg('medium_spring_green')
    red = fg('red')
    purple = fg('purple_1a')
    magenta = fg('magenta')
    grey = fg('grey_27')
    orange = fg('orange_red_1')
    bold = attr('bold')
    reset = attr('reset')

    INFO = f'{yellow}[INFO]{reset}'
    WARNING = f'{orange}[WARNING]{reset}'
    PROXY = f'{cyan}[PROXY]{reset}'
    SUCCESS = f'{green}[SUCCESS]{reset}'
    FAILED = f'{red}[FAILED]{reset}'

