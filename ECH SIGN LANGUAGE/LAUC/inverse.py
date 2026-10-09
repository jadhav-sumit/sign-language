from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("inverse.html")   # optional


def get_minor(matrix, row, col):
    return [
        [matrix[i][j] for j in range(len(matrix)) if j != col]
        for i in range(len(matrix)) if i != row
    ]


def determinant(matrix):
    n = len(matrix)

    # 1×1
    if n == 1:
        return matrix[0][0]

    # 2×2
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    # n > 2
    det = 0
    for c in range(n):
        det += ((-1) ** c) * matrix[0][c] * determinant(get_minor(matrix, 0, c))
    return det


def cofactor_matrix(matrix):
    n = len(matrix)
    cof = []

    for i in range(n):
        row = []
        for j in range(n):
            minor_mat = get_minor(matrix, i, j)
            cof_val = ((-1) ** (i + j)) * determinant(minor_mat)
            row.append(cof_val)
        cof.append(row)

    return cof


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


@app.route('/inverse', methods=['POST'])
def inverse():
    try:
        # Form input
        matrix = request.form.getlist("matrix")

        # JSON input
        if not matrix:
            data = request.json
            matrix = data.get("matrix")

        # Convert to numeric rows
        processed = []
        for r in matrix:
            processed.append(
                [float(x) for x in r.split()] if isinstance(r, str) else r
            )

        # Must be square matrix
        n = len(processed)
        for row in processed:
            if len(row) != n:
                return jsonify({"error": "Matrix must be square"}), 400

        # Determinant
        det = determinant(processed)

        if det == 0:
            return jsonify({"error": "Matrix is singular (determinant = 0). Inverse does not exist."}), 400

        # Adjoint = transpose of cofactor matrix
        cof = cofactor_matrix(processed)
        adj = transpose(cof)

        # Inverse = adj / det
        inv = [[adj[i][j] / det for j in range(n)] for i in range(n)]

        return jsonify({
            "matrix": processed,
            "determinant": det,
            "adjoint": adj,
            "inverse": inv
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)