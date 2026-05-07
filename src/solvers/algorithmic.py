import kociemba
from utils.state_mapper import get_facelet_string

SOLVED_STRING = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"

def solve(cube_state):
    """
    Solves the cube using Kociemba's two-phase algorithm.
    Returns a list of moves or an error message.
    """
    try:
        facelet_string = get_facelet_string(cube_state)
        print(f"Generated facelet string: {facelet_string}")
        
        # Check if already solved
        if facelet_string == SOLVED_STRING:
            print("Cube is already solved.")
            return [], "Success"
            
        # Validate that we have 54 facelets and no '?'
        if len(facelet_string) != 54 or '?' in facelet_string:
            return None, "Invalid cube state: missing pieces or unknown colors."
            
        solution = kociemba.solve(facelet_string)
        if not solution:
            return [], "Success"
            
        moves = solution.split(' ')
        return moves, "Success"
    except Exception as e:
        print(f"Solver error: {str(e)}")
        return None, str(e)
