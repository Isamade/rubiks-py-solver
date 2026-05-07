import numpy as np

# indices in the piece.colors array correspond to:
# 0: front (z=1)
# 1: back (z=-1)
# 2: top (y=1)
# 3: bottom (y=-1)
# 4: right (x=1)
# 5: left (x=-1)
FACE_COLOR_INDEX = {
    "F": 0,
    "B": 1,
    "U": 2,
    "D": 3,
    "R": 4,
    "L": 5
}

def get_facelet_string(cube_state):
    """
    Converts the CubeState (list of pieces) into a 54-char string for Kociemba.
    Order: U1-U9, R1-R9, F1-F9, D1-D9, L1-L9, B1-B9
    """
    pieces = cube_state.pieces
    
    # Create a 3D grid of pieces for easy lookup based on their index in the pieces array
    grid = {}
    for i, piece in enumerate(pieces):
        # The frontend loops x, then y, then z in [-1, 0, 1]
        x = (i // 9) - 1
        y = ((i % 9) // 3) - 1
        z = (i % 3) - 1
        grid[(x, y, z)] = piece.colors

    # Identify face characters based on center piece colors
    # Centers are at: U(0,1,0), D(0,-1,0), F(0,0,1), B(0,0,-1), R(1,0,0), L(-1,0,0)
    COLOR_TO_FACE = {
        grid[(0, 1, 0)][FACE_COLOR_INDEX["U"]]: "U",
        grid[(0, -1, 0)][FACE_COLOR_INDEX["D"]]: "D",
        grid[(0, 0, 1)][FACE_COLOR_INDEX["F"]]: "F",
        grid[(0, 0, -1)][FACE_COLOR_INDEX["B"]]: "B",
        grid[(1, 0, 0)][FACE_COLOR_INDEX["R"]]: "R",
        grid[(-1, 0, 0)][FACE_COLOR_INDEX["L"]]: "L",
    }

    def get_char(pos, face_char):
        piece_colors = grid.get(pos)
        if not piece_colors:
            return "?"
        color_hex = piece_colors[FACE_COLOR_INDEX[face_char]]
        return COLOR_TO_FACE.get(color_hex, "?")

    # U1-U9 (Up): y=1, z from -1 to 1, x from -1 to 1
    u_face = ""
    for z in [-1, 0, 1]:
        for x in [-1, 0, 1]:
            u_face += get_char((x, 1, z), "U")

    # R1-R9 (Right): x=1, y from 1 to -1, z from 1 to -1
    r_face = ""
    for y in [1, 0, -1]:
        for z in [1, 0, -1]:
            r_face += get_char((1, y, z), "R")

    # F1-F9 (Front): z=1, y from 1 to -1, x from -1 to 1
    f_face = ""
    for y in [1, 0, -1]:
        for x in [-1, 0, 1]:
            f_face += get_char((x, y, 1), "F")

    # D1-D9 (Down): y=-1, z from 1 to -1, x from -1 to 1
    d_face = ""
    for z in [1, 0, -1]:
        for x in [-1, 0, 1]:
            d_face += get_char((x, -1, z), "D")

    # L1-L9 (Left): x=-1, y from 1 to -1, z from -1 to 1
    l_face = ""
    for y in [1, 0, -1]:
        for z in [-1, 0, 1]:
            l_face += get_char((-1, y, z), "L")

    # B1-B9 (Back): z=-1, y from 1 to -1, x from 1 to -1
    b_face = ""
    for y in [1, 0, -1]:
        for x in [1, 0, -1]:
            b_face += get_char((x, y, -1), "B")

    return u_face + r_face + f_face + d_face + l_face + b_face
