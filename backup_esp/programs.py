import uasyncio as asyncio
import helpers as h

from time import sleep


async def color_cycle():
    for hue in range(0, 360, 2):
        h.set_rgb(*h.hsv_to_rgb(hue / 360, 1, 1))
        await asyncio.sleep(0.1)


async def color_flash(**kwargs):

    pattern = [1023, 0, 1023, 0, 1023, 0]

    color = kwargs.get("flash_color", None)

    if color is None:
        for color in ["R", "G", "B"]:
            h.set_rgb(**{color: 1023})
            await asyncio.sleep(0.5)
            h.reset_pins()
            await asyncio.sleep(0.5)

    else:
        h.set_rgb(*color)
        await asyncio.sleep(0.5)
        h.reset_pins()
        await asyncio.sleep(0.5)


def ramp_up(color_from=(0, 0, 1023), duration=1, n_steps=100):

    color_from_hsv = h.rgb_to_hsv(*color_from)
    saturation_start = color_from_hsv[1]

    for step in range(0, n_steps):
        saturation = saturation_start - step * (saturation_start / n_steps)
        rgb = h.hsv_to_rgb(color_from_hsv[0], saturation, color_from_hsv[2])
        h.set_rgb(*rgb)

        sleep(duration / n_steps)


def ramp_down(color_to=(0, 0, 1023), duration=1, n_steps=100):

    color_to_hsv = h.rgb_to_hsv(*color_to)
    saturation_end = color_to_hsv[1]

    for step in range(0, n_steps):
        saturation = step * (saturation_end / n_steps)
        rgb = h.hsv_to_rgb(color_to_hsv[0], saturation, color_to_hsv[2])
        h.set_rgb(*rgb)

        sleep(duration / n_steps)


async def storm(**kwargs):
    """
    To simulate a storm each "flash_period" seconds
    """

    storm_period = kwargs.get("storm_period", 60)
    storm_color = kwargs.get("storm_color", (0, 0, 1023))

    h.set_rgb(*storm_color)

    await asyncio.sleep(5)
    ramp_up(color_from=storm_color, duration=0.25, n_steps=10)
    ramp_down(color_to=storm_color, duration=1, n_steps=40)

    await asyncio.sleep(5)
    ramp_up(color_from=storm_color, duration=0.15, n_steps=10)
    h.set_rgb(*storm_color)
    ramp_up(color_from=storm_color, duration=0.25, n_steps=10)
    ramp_down(color_to=storm_color, duration=0.5, n_steps=20)


async def program(program_name, **kwargs):
    if program_name == "color_cycle":
        await color_cycle()
    elif program_name == "color_flash":
        await color_flash(**kwargs)
    elif program_name == "storm":
        await storm(**kwargs)
