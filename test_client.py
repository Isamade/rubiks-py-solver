import sys
import os
import grpc

# Add the generated directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'generated'))

import solver_pb2
import solver_pb2_grpc

def create_solved_cube():
    pieces = []
    positions = [-1, 0, 1]
    
    # Classic Rubik's cube colors (matching RubiksCube.tsx)
    face_colors = {
        "top": "#ffff00",    # yellow
        "bottom": "#ffffff", # white
        "front": "#2196f3",  # blue
        "back": "#4caf50",   # green
        "right": "#ff0000",  # red
        "left": "#ff8c00",   # orange
    }

    for x in positions:
        for y in positions:
            for z in positions:
                colors = [
                    face_colors["front"] if z == 1 else "#1a1a1a",
                    face_colors["back"] if z == -1 else "#1a1a1a",
                    face_colors["top"] if y == 1 else "#1a1a1a",
                    face_colors["bottom"] if y == -1 else "#1a1a1a",
                    face_colors["right"] if x == 1 else "#1a1a1a",
                    face_colors["left"] if x == -1 else "#1a1a1a",
                ]
                pieces.append(solver_pb2.Piece(position=[float(x), float(y), float(z)], colors=colors))
    
    return solver_pb2.CubeState(pieces=pieces)

def test():
    channel = grpc.insecure_channel('localhost:50051')
    stub = solver_pb2_grpc.RubiksSolverStub(channel)
    
    print("Testing with solved cube...")
    state = create_solved_cube()
    request = solver_pb2.SolveRequest(state=state)
    
    try:
        response = stub.SolveAlgorithmic(request)
        print(f"Response: {response.message}")
        print(f"Moves: {response.moves}")
    except grpc.RpcError as e:
        print(f"RPC failed: {e}")

if __name__ == '__main__':
    test()
