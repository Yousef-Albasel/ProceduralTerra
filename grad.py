import math
import numpy as np
import options

def getCricleGrad():
    SCREEN_WIDTH = options.width
    SCREEN_HEIGHT = options.height
    center_x, center_y = SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2
    circle_grad = np.zeros((SCREEN_WIDTH, SCREEN_HEIGHT))  # Fix the array creation

    for y in range(SCREEN_WIDTH):
        for x in range(SCREEN_HEIGHT):
            distx = abs(x - center_x)
            disty = abs(y - center_y)
            dist = math.sqrt(distx * distx + disty * disty)
            circle_grad[y, x] = dist  # Use array indexing

    # get it between -1 and 1
    max_grad = np.max(circle_grad)
    circle_grad = circle_grad / max_grad
    circle_grad -= 0.5
    circle_grad *= 2.0
    circle_grad = -circle_grad

    # shrink gradient
    for y in range(SCREEN_WIDTH):
        for x in range(SCREEN_HEIGHT):
            if circle_grad[y, x] > 0:
                circle_grad[y, x] *= 20  # Use array indexing

    # get it between 0 and 1
    max_grad = np.max(circle_grad)
    circle_grad = circle_grad / max_grad
    return circle_grad
