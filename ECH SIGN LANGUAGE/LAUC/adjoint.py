from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template("adjoint.html")


def get_minor(matrix, row, col):
    """Get the minor matrix by removing row and column"""
    return [
        [matrix[i][j] for j in range(len(matrix)) if j != col]
        for i in range(len(matrix)) if i != row
    ]


def determinant(matrix):
    """Calculate determinant of a matrix"""
    n = len(matrix)

    # Base cases
    if n == 1:
        return matrix[0][0]

    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    # Recursive case for larger matrices
    det = 0
    for c in range(n):
        minor = get_minor(matrix, 0, c)
        det += ((-1) ** c) * matrix[0][c] * determinant(minor)
    return det


def cofactor_matrix(matrix):
    """Calculate cofactor matrix"""
    n = len(matrix)
    cofactor = []

    for i in range(n):
        row = []
        for j in range(n):
            minor_mat = get_minor(matrix, i, j)
            cof = ((-1) ** (i + j)) * determinant(minor_mat)
            row.append(cof)
        cofactor.append(row)
    return cofactor


def transpose(matrix):
    """Transpose a matrix"""
    return [list(row) for row in zip(*matrix)]


@app.route('/adjoint', methods=['POST'])
def calculate_adjoint():
    try:
        data = request.get_json()
        
        if not data or 'matrix' not in data:
            return jsonify({"error": "No matrix provided"}), 400
        
        matrix = data['matrix']
        
        # Validate matrix
        if not isinstance(matrix, list) or len(matrix) == 0:
            return jsonify({"error": "Invalid matrix format"}), 400
        
        n = len(matrix)
        
        # Check if matrix is square
        for row in matrix:
            if len(row) != n:
                return jsonify({"error": "Matrix must be square"}), 400
            
            # Check if all elements are numbers
            for element in row:
                try:
                    float(element)
                except ValueError:
                    return jsonify({"error": "Matrix elements must be numbers"}), 400
        
        # Convert all elements to float
        processed = [[float(element) for element in row] for row in matrix]
        
        # Check if determinant is zero (for singular matrix)
        det = determinant(processed)
        if det == 0:
            return jsonify({"error": "Matrix is singular (determinant is zero)"}), 400
        
        # Calculate cofactor matrix
        cof_matrix = cofactor_matrix(processed)
        
        # Calculate adjoint (transpose of cofactor matrix)
        adj = transpose(cof_matrix)
        
        # Calculate inverse (adjoint / determinant) if needed
        inverse = [[adj[i][j] / det for j in range(n)] for i in range(n)]
        
        return jsonify({
            "success": True,
            "matrix": processed,
            "determinant": det,
            "cofactor_matrix": cof_matrix,
            "adjoint": adj,
            "inverse": inverse,
            "size": n
        })
        
    except Exception as e:
        app.logger.error(f"Error calculating adjoint: {str(e)}")
        return jsonify({"error": str(e)}), 400


@app.route('/determinant', methods=['POST'])
def calculate_determinant():
    try:
        data = request.get_json()
        
        if not data or 'matrix' not in data:
            return jsonify({"error": "No matrix provided"}), 400
        
        matrix = data['matrix']
        n = len(matrix)
        
        # Check if matrix is square
        for row in matrix:
            if len(row) != n:
                return jsonify({"error": "Matrix must be square"}), 400
        
        processed = [[float(element) for element in row] for row in matrix]
        det = determinant(processed)
        
        return jsonify({
            "success": True,
            "determinant": det,
            "matrix": processed,
            "size": n
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True, port=5000)