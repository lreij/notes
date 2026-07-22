#!/usr/bin/env python3
"""
Usage:
    python3 grid.py <quota> <init_price>
    python3 grid.py 10000 1.486
"""
import sys
import math
from decimal import Decimal, ROUND_HALF_UP


def java_round(x: float) -> int:
    """Replicate Java's Math.round(double): floor(x + 0.5) as a long."""
    return math.floor(x + 0.5)


def fmt2(x: float) -> str:
    """Replicate Java's String.format("%.2f", x) which uses HALF_UP rounding."""
    return str(Decimal(repr(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def get_volume(quota: float, price: float, volume: int) -> int:
    while price * volume < quota:
        volume += 100
    return volume


def grid(quota: float, init_price: float) -> None:
    levels = []
    for i in range(1, 20):
        percent = 1 - i * 0.05
        raw_price = init_price * percent
        raw_volume = quota / raw_price
        price = java_round(raw_price * 100) / 100.0
        volume = java_round(raw_volume / 100) * 100
        volume = get_volume(quota, price, volume)
        levels.append((percent, price, volume))

    # toString: "%.2f %.2f %d %d" -> percent, price, volume, round(price*volume)
    for percent, price, volume in levels:
        print(f"{fmt2(percent)} {fmt2(price)} {volume} {java_round(price * volume)}")

    # Additionally, output the first three columns separately,
    # each column printed in order, one value per line.
    print()
    for percent, _, _ in levels:
        print(fmt2(percent))
    print()
    for _, price, _ in levels:
        print(fmt2(price))
    print()
    for _, _, volume in levels:
        print(volume)


def main() -> None:
    quota = 10000.0
    init_price = 1.486
    if len(sys.argv) >= 3:
        quota = float(sys.argv[1])
        init_price = float(sys.argv[2])
    grid(quota, init_price)


if __name__ == "__main__":
    main()
