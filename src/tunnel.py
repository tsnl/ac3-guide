"""Static wall geometry for the CSS-only oval tunnel (no runtime drawing)."""
from math import atan2, cos, degrees, hypot, pi, sin


def markup():
    walls = []
    for side in range(24):
        angle = side * 2 * pi / 24
        following = (side + 1) * 2 * pi / 24
        x, y = 42.78 * cos(angle), 27.9 * sin(angle)
        dx, dy = 42.78 * cos(following) - x, 27.9 * sin(following) - y
        style = (f'--x:{x:.6f};--y:{y:.6f};--width:{hypot(dx, dy):.6f};'
                 f'--angle:{degrees(atan2(dy, dx)):.6f}deg;'
                 f'--light:{85 + cos(angle - .6) * 3:.4f}%')
        walls.append(f'<div class="tunnel-wall" style="{style}"></div>')
    return ('<div id="electrosphere" aria-hidden="true">'
            '<div class="tunnel-camera"><div class="tunnel-flight">'
            + ''.join(walls) + '</div></div><div class="tunnel-haze"></div></div>')
