import sys
import math
from logger_decorator import logger, LogResult


class CriticalError(RuntimeError):
    """Ситуация, которую считаем критической."""


@logger(handle=sys.stdout)
def solve_quadratic(a, b, c):
    try:
        a = float(a)
        b = float(b)
        c = float(c)
    except (TypeError, ValueError) as e:
        raise ValueError(f"Invalid coefficients: {e}") from e

    if a == 0 and b == 0:
        raise CriticalError("Both a and b are 0: equation is impossible/degenerate")
    if a == 0:
        if b == 0:
            raise CriticalError("Both a and b are 0 (after conversion)")
        return (-c / b,)

    d = b * b - 4 * a * c
    if d < 0:
        return LogResult("WARNING", None, f"Discriminant < 0 (d={d}); no real roots")

    sqrt_d = math.sqrt(d)
    x1 = (-b + sqrt_d) / (2 * a)
    x2 = (-b - sqrt_d) / (2 * a)
    return (x1, x2)


if __name__ == "__main__":
    print("Two roots:", solve_quadratic(1, -3, 2))
    print("Warning case:", solve_quadratic(1, 0, 1))
    try:
        solve_quadratic("abc", 1, 1)
    except Exception:
        pass
    try:
        solve_quadratic(0, 0, 1)
    except Exception:
        pass
