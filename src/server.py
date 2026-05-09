import sys
import os
import grpc
from concurrent import futures

# Add the generated directory to the path so imports work correctly
sys.path.append(os.path.join(os.path.dirname(__file__), 'generated'))

import solver_pb2
import solver_pb2_grpc
from solvers import algorithmic
import threading
from consumer import start_consumer

class RubiksSolverServicer(solver_pb2_grpc.RubiksSolverServicer):
    def SolveAlgorithmic(self, request, context):
        print("Received SolveAlgorithmic request")
        moves, message = algorithmic.solve(request.state)
        
        if moves is None:
            return solver_pb2.SolveResponse(moves=[], message=message)
        
        return solver_pb2.SolveResponse(moves=moves, message=message)

    def SolveNeuralNetwork(self, request, context):
        return solver_pb2.SolveResponse(moves=[], message="Neural Network solver not implemented yet.")

    def SolveReinforcementLearning(self, request, context):
        return solver_pb2.SolveResponse(moves=[], message="Reinforcement Learning solver not implemented yet.")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    solver_pb2_grpc.add_RubiksSolverServicer_to_server(RubiksSolverServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("Rubik's Solver Server starting on port 50051...")
    
    # Start RabbitMQ consumer in a background thread
    consumer_thread = threading.Thread(target=start_consumer, daemon=True)
    consumer_thread.start()
    print("RabbitMQ consumer started in background thread.")
    
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
