from configuration import COLORS


def reset_pins():
    [pwm.duty(0) for pwm in COLORS.values()]


def set_rgb(R=0, G=0, B=0):
    COLORS["R"].duty(R)
    COLORS["G"].duty(G)
    COLORS["B"].duty(B)


def hsv_to_normalized_rgb(h, s, v):
    if s == 0.0:
        return (v, v, v)
    i = int(h * 6.0)
    f = (h * 6.0) - i
    p, q, t = v * (1.0 - s), v * (1.0 - s * f), v * (1.0 - s * (1.0 - f))
    i %= 6
    if i == 0:
        return (v, t, p)
    if i == 1:
        return (q, v, p)
    if i == 2:
        return (p, v, t)
    if i == 3:
        return (p, q, v)
    if i == 4:
        return (t, p, v)
    if i == 5:
        return (v, p, q)


def normalized_rgb_to_hsv(r, g, b):
    maxc = max(r, g, b)
    minc = min(r, g, b)
    v = maxc
    if minc == maxc:
        return 0.0, 0.0, v
    s = (maxc - minc) / maxc
    rc = (maxc - r) / (maxc - minc)
    gc = (maxc - g) / (maxc - minc)
    bc = (maxc - b) / (maxc - minc)
    if r == maxc:
        h = bc - gc
    elif g == maxc:
        h = 2.0 + rc - bc
    else:
        h = 4.0 + gc - rc
    h = (h / 6.0) % 1.0
    return h, s, v


def rgb_to_hsv(R, G, B):
    r, g, b = R / 1023, G / 1023, B / 1023
    return normalized_rgb_to_hsv(r, g, b)


def hsv_to_rgb(h, s, v):
    (r, g, b) = hsv_to_normalized_rgb(h, s, v)
    return (
        int(1023 * r),
        int(1023 * g),
        int(1023 * b),
    )
