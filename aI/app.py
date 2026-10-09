from flask import Flask, render_template, request, jsonify
import numpy as np

app = Flask(__name__)

def parse_matrix(matrix_str):
    """Convert string to numpy matrix"""
    try:
        rows = matrix_str.strip().split(';')
        matrix = []
        for row in rows:
            if row.strip():
                vals = [float(x.strip()) for x in row.split(',')]
                matrix.append(vals)
        return np.array(matrix)
    except:
        return None

def matrix_to_str(matrix):
    """Convert numpy matrix to string"""
    if matrix is None:
        return ""
    rows = []
    for row in matrix:
        rows.append(','.join([f"{x:.4f}" for x in row]))
    return ';'.join(rows)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json
        operation = data['operation']
        matrix_a = parse_matrix(data['matrixA'])
        
        if matrix_a is None:
            return jsonify({'error': 'Invalid Matrix A'})
        
        result = {}
        
        # 1. RANK
        if operation == 'rank':
            rank = np.linalg.matrix_rank(matrix_a)
            return jsonify({
                'success': True,
                'result': f'Rank = {rank}',
                'details': f'The rank of matrix A is {rank}'
            })
        
        # 2. DETERMINANT
        elif operation == 'determinant':
            if matrix_a.shape[0] != matrix_a.shape[1]:
                return jsonify({'error': 'Matrix must be square for determinant'})
            
            det = np.linalg.det(matrix_a)
            return jsonify({
                'success': True,
                'result': f'det(A) = {det:.4f}',
                'details': f'Determinant = {det:.4f}'
            })
        
        # 3. MINOR (for specific element)
        elif operation == 'minor':
            row = int(data.get('row', 0))
            col = int(data.get('col', 0))
            
            if row >= matrix_a.shape[0] or col >= matrix_a.shape[1]:
                return jsonify({'error': 'Invalid row/column index'})
            
            # Remove row and column
            minor_matrix = np.delete(np.delete(matrix_a, row, axis=0), col, axis=1)
            
            # Calculate minor determinant
            if minor_matrix.size == 0:
                minor_det = 1
            else:
                minor_det = np.linalg.det(minor_matrix)
            
            return jsonify({
                'success': True,
                'result': f'Minor({row+1},{col+1}) = {minor_det:.4f}',
                'matrix': matrix_to_str(minor_matrix),
                'details': f'Minor of element at position ({row+1},{col+1}) = {minor_det:.4f}'
            })
        
        # 4. COFACTOR (for specific element)
        elif operation == 'cofactor':
            row = int(data.get('row', 0))
            col = int(data.get('col', 0))
            
            if row >= matrix_a.shape[0] or col >= matrix_a.shape[1]:
                return jsonify({'error': 'Invalid row/column index'})
            
            # Calculate minor
            minor_matrix = np.delete(np.delete(matrix_a, row, axis=0), col, axis=1)
            if minor_matrix.size == 0:
                minor_det = 1
            else:
                minor_det = np.linalg.det(minor_matrix)
            
            # Cofactor = (-1)^(i+j) * minor
            cofactor = ((-1) ** (row + col)) * minor_det
            
            return jsonify({
                'success': True,
                'result': f'C({row+1},{col+1}) = {cofactor:.4f}',
                'details': f'Cofactor of element at position ({row+1},{col+1}) = {cofactor:.4f}'
            })
        
        # 5. ADDITION
        elif operation == 'addition':
            matrix_b = parse_matrix(data['matrixB'])
            if matrix_b is None:
                return jsonify({'error': 'Invalid Matrix B'})
            
            if matrix_a.shape != matrix_b.shape:
                return jsonify({'error': 'Matrices must have same dimensions for addition'})
            
            result_matrix = matrix_a + matrix_b
            
            return jsonify({
                'success': True,
                'result': 'A + B =',
                'matrix': matrix_to_str(result_matrix),
                'details': f'Result matrix size: {result_matrix.shape[0]}×{result_matrix.shape[1]}'
            })
        
        # 6. SUBTRACTION
        elif operation == 'subtraction':
            matrix_b = parse_matrix(data['matrixB'])
            if matrix_b is None:
                return jsonify({'error': 'Invalid Matrix B'})
            
            if matrix_a.shape != matrix_b.shape:
                return jsonify({'error': 'Matrices must have same dimensions for subtraction'})
            
            result_matrix = matrix_a - matrix_b
            
            return jsonify({
                'success': True,
                'result': 'A - B =',
                'matrix': matrix_to_str(result_matrix),
                'details': f'Result matrix size: {result_matrix.shape[0]}×{result_matrix.shape[1]}'
            })
        
        # 7. CRAMER'S RULE
        elif operation == 'cramer':
            vector_b = parse_matrix(data['matrixB'])
            if vector_b is None:
                return jsonify({'error': 'Invalid Vector B'})
            
            if matrix_a.shape[0] != matrix_a.shape[1]:
                return jsonify({'error': 'Matrix A must be square for Cramer\'s Rule'})
            
            if matrix_a.shape[0] != vector_b.shape[0]:
                return jsonify({'error': 'Matrix A and Vector B must have same number of rows'})
            
            n = matrix_a.shape[0]
            det_a = np.linalg.det(matrix_a)
            
            if abs(det_a) < 1e-10:
                return jsonify({'error': 'Determinant is zero, Cramer\'s Rule cannot be applied'})
            
            solutions = []
            for i in range(n):
                a_i = matrix_a.copy()
                a_i[:, i] = vector_b.flatten()
                det_a_i = np.linalg.det(a_i)
                x_i = det_a_i / det_a
                solutions.append(x_i)
            
            solution_str = ', '.join([f'x{i+1} = {solutions[i]:.4f}' for i in range(n)])
            
            return jsonify({
                'success': True,
                'result': f'Solution: {solution_str}',
                'details': f'Using Cramer\'s Rule\ndet(A) = {det_a:.4f}'
            })
        
        # 8. GAUSS ELIMINATION
        elif operation == 'gauss':
            vector_b = parse_matrix(data['matrixB'])
            if vector_b is None:
                return jsonify({'error': 'Invalid Vector B'})
            
            if matrix_a.shape[0] != vector_b.shape[0]:
                return jsonify({'error': 'Matrix A and Vector B must have same number of rows'})
            
            n = matrix_a.shape[0]
            aug = np.hstack((matrix_a, vector_b.reshape(-1, 1)))
            
            steps = ["GAUSSIAN ELIMINATION STEPS:", "="*40]
            steps.append(f"Initial augmented matrix:\n{aug}")
            
            # Forward elimination
            for i in range(n):
                # Find pivot
                max_row = i
                for k in range(i+1, n):
                    if abs(aug[k, i]) > abs(aug[max_row, i]):
                        max_row = k
                
                if max_row != i:
                    aug[[i, max_row]] = aug[[max_row, i]]
                    steps.append(f"Swap R{i+1} with R{max_row+1}")
                
                if abs(aug[i, i]) > 1e-10:
                    aug[i] = aug[i] / aug[i, i]
                    steps.append(f"Normalize R{i+1}")
                
                for k in range(i+1, n):
                    if abs(aug[k, i]) > 1e-10:
                        factor = aug[k, i]
                        aug[k] = aug[k] - factor * aug[i]
                        steps.append(f"R{k+1} = R{k+1} - ({factor:.4f})*R{i+1}")
            
            # Back substitution
            x = np.zeros(n)
            for i in range(n-1, -1, -1):
                x[i] = aug[i, n]
                for j in range(i+1, n):
                    x[i] -= aug[i, j] * x[j]
            
            solution_str = ', '.join([f'x{i+1} = {x[i]:.4f}' for i in range(n)])
            
            return jsonify({
                'success': True,
                'result': f'Solution: {solution_str}',
                'details': '\n'.join(steps)
            })
        
        # 9. GAUSS-JORDAN
        elif operation == 'gauss_jordan':
            vector_b = parse_matrix(data['matrixB'])
            if vector_b is None:
                return jsonify({'error': 'Invalid Vector B'})
            
            if matrix_a.shape[0] != vector_b.shape[0]:
                return jsonify({'error': 'Matrix A and Vector B must have same number of rows'})
            
            n = matrix_a.shape[0]
            aug = np.hstack((matrix_a, vector_b.reshape(-1, 1)))
            
            steps = ["GAUSS-JORDAN ELIMINATION STEPS:", "="*40]
            steps.append(f"Initial augmented matrix:\n{aug}")
            
            for i in range(n):
                # Find pivot
                max_row = i
                for k in range(i+1, n):
                    if abs(aug[k, i]) > abs(aug[max_row, i]):
                        max_row = k
                
                if max_row != i:
                    aug[[i, max_row]] = aug[[max_row, i]]
                    steps.append(f"Swap R{i+1} with R{max_row+1}")
                
                if abs(aug[i, i]) > 1e-10:
                    aug[i] = aug[i] / aug[i, i]
                    steps.append(f"Normalize R{i+1}")
                
                for k in range(n):
                    if k != i and abs(aug[k, i]) > 1e-10:
                        factor = aug[k, i]
                        aug[k] = aug[k] - factor * aug[i]
                        steps.append(f"R{k+1} = R{k+1} - ({factor:.4f})*R{i+1}")
            
            solution = aug[:, n]
            solution_str = ', '.join([f'x{i+1} = {solution[i]:.4f}' for i in range(n)])
            
            return jsonify({
                'success': True,
                'result': f'Solution: {solution_str}',
                'details': '\n'.join(steps)
            })
        
        else:
            return jsonify({'error': 'Unknown operation'})
            
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)