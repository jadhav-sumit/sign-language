from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('minor.html')


def get_minor(matrix, row, col):
    """
    Return the minor matrix after removing 'row' and 'col'
    """
    return [
        [matrix[i][j] for j in range(len(matrix)) if j != col]
        for i in range(len(matrix)) if i != row
    ]


@app.route('/minor', methods=['POST'])
def minor():
    try:
        row = request.form.get('row')
        col = request.form.get('col')
        matrix = request.form.get('matrix')

        if not row or not col or not matrix:
            return jsonify({"error": "All fields are required!"}), 400

        row = int(row)
        col = int(col)

        # Convert textarea into matrix
        processed_matrix = []
        for line in matrix.strip().split("\n"):
            processed_matrix.append([float(x) for x in line.split()])

        n = len(processed_matrix)

        if row < 0 or row >= n or col < 0 or col >= n:
            return jsonify({"error": "Row/column index out of range"}), 400

        result = get_minor(processed_matrix, row, col)

        return jsonify({
            "matrix": processed_matrix,
            "row": row,
            "col": col,
            "minor": result
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
