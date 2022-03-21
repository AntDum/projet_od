from pygame.math import Vector2

def rotate_pivot(pos, size, pivotPos, angle):
    """calculate the upper left origin of the rotated image

        use 
        rotated_image = pygame.transform.rotate(image, angle)

        and 
        blit(rotated_image, origin)
    """

    w, h       = size
    box        = [Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
    box_rotate = [p.rotate(angle) for p in box]
    extreme_box    = (min(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

    pivot        = Vector2(pivotPos[0], -pivotPos[1])
    pivot_rotate = pivot.rotate(angle)
    pivot_move   = pivot_rotate - pivot

    origin = (pos[0] - pivotPos[0] + extreme_box[0] - pivot_move[0],
              pos[1] - pivotPos[1] - extreme_box[1] + pivot_move[1])

    return origin
