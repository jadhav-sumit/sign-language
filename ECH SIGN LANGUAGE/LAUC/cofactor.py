from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("cofactor.html")   # optional


def get_minor(matrix, row, col):
    """
    Returns the minor matrix after removing the given row and column.
    """
    return [
        [matrix[i][j] for j in range(len(matrix)) if j != col]
        for i in range(len(matrix)) if i != row
    ]


def determinant(matrix):
    """
    Recursively calculates determinant (needed for cofactor).
    """
    n = len(matrix)

    if n == 1:
        return matrix[0][0]

    if n == 2:
        return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]

    det = 0
    for c in range(n):
        det += ((-1)**c) * matrix[0][c] * determinant(get_minor(matrix, 0, c))

    return det


@app.route("/cofactor", methods=["POST"])
def cofactor():
    try:
        # Receive form data
        row = request.form.get("row")
        col = request.form.get("col")
        matrix = request.form.getlist("matrix")

        # Receive JSON data
        if not row:
            data = request.json
            row = data.get("row")
            col = data.get("col")
            matrix = data.get("matrix")

        row = int(row)
        col = int(col)

        # Convert matrix
        processed_matrix = []
        for r in matrix:
            processed_matrix.append(
                [float(x) for x in r.split()] if isinstance(r, str) else r
            )

        n = len(processed_matrix)
        if row < 0 or row >= n or col < 0 or col >= n:
            return jsonify({"error": "Invalid row/column index"}), 400

        # Minor
        minor_matrix = get_minor(processed_matrix, row, col)

        # Cofactor: (-1)^(i+j) * det(minor)
        sign = (-1) ** (row + col)
        cofactor_value = sign * determinant(minor_matrix)

        return jsonify({
            "matrix": processed_matrix,
            "row": row,
            "col": col,
            "minor": minor_matrix,
            "cofactor": cofactor_value
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)