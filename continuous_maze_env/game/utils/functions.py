from pyglet.shapes import Rectangle, Circle


def _ccw(a, b, c):
    # Counter-clockwise test. Keeping this at module scope avoids re-defining it per call.
    return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])


def line_segments_intersect(p1, p2, q1, q2):
    """
    Check if line segments p1-p2 and q1-q2 intersect.
    """
    return (_ccw(p1, q1, q2) != _ccw(p2, q1, q2)) and (
        _ccw(p1, p2, q1) != _ccw(p1, p2, q2)
    )


def rectangle_circle_overlap(rect: Rectangle, circle: Circle) -> bool:
    """
    Check if a rectangle and a circle overlap.
    rect: dict with 'left', 'right', 'top', 'bottom'
    circle: Circle object with x, y, radius
    """
    # Find the closest point to the circle within the rectangle
    closest_x = min(max(circle.x, rect["left"]), rect["right"])
    closest_y = min(max(circle.y, rect["bottom"]), rect["top"])

    # Calculate the distance between the circle's center and this closest point
    distance_x = circle.x - closest_x
    distance_y = circle.y - closest_y

    # If the distance is less than the circle's radius, there's a collision
    distance_squared = distance_x**2 + distance_y**2
    return distance_squared < circle.radius**2


def rectangle_inside(rect1, rect2):
    """
    Check if rect1 is completely inside rect2.
    """
    return (
        rect1.x + 4 >= rect2.x
        and rect1.x + rect1.width <= rect2.x + 4 + rect2.width
        and rect1.y + 4 >= rect2.y
        and rect1.y + rect1.height <= rect2.y + rect2.height + 4
    )
