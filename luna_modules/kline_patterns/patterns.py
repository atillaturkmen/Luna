from luna_modules.kline_patterns import kline_helpers


def is_hammer(klines):
    head_bottom = kline_helpers.kline_head_bottom(klines[-1])
    midpoint = kline_helpers.kline_midpoint(klines[-1])
    return kline_helpers.is_red(klines[-2]) and head_bottom > midpoint


def is_hanging_man(klines):
    head_top = kline_helpers.kline_head_top(klines[-1])
    midpoint = kline_helpers.kline_midpoint(klines[-1])
    return (not kline_helpers.is_red(klines[-1])) and head_top < midpoint


def is_morning_star(klines):
    if len(klines) < 3:
        return False
    first_length = kline_helpers.kline_head_length(klines[-3])
    middle_length = kline_helpers.kline_head_length(klines[-2])
    final_length = kline_helpers.kline_head_length(klines[-1])
    first_red = kline_helpers.is_red(klines[-3])
    third_green = not kline_helpers.is_red(klines[-1])
    return first_red and third_green and middle_length < first_length and middle_length < final_length


def is_evening_star(klines):
    if len(klines) < 3:
        return False
    first_length = kline_helpers.kline_head_length(klines[-3])
    middle_length = kline_helpers.kline_head_length(klines[-2])
    final_length = kline_helpers.kline_head_length(klines[-1])
    first_green = not kline_helpers.is_red(klines[-3])
    third_red = kline_helpers.is_red(klines[-1])
    return first_green and third_red and middle_length < first_length and middle_length < final_length


def is_bullish_engulf(klines):
    prev_length = kline_helpers.kline_head_length(klines[-2])
    final_length = kline_helpers.kline_head_length(klines[-1])
    return kline_helpers.is_red(klines[-2]) and prev_length < final_length


def is_bearish_engulf(klines):
    prev_length = kline_helpers.kline_head_length(klines[-2])
    final_length = kline_helpers.kline_head_length(klines[-1])
    return (not kline_helpers.is_red(klines[-2])) and prev_length < final_length


def pattern_matches(klines):
    matches = []
    if is_hammer(klines):
        matches.append("hammer")
    if is_hanging_man(klines):
        matches.append("hanging man")
    if is_bearish_engulf(klines):
        matches.append("bearish engulf")
    if is_bullish_engulf(klines):
        matches.append("bullish engulf")
    if is_evening_star(klines):
        matches.append("evening star")
    if is_morning_star(klines):
        matches.append("morning star")