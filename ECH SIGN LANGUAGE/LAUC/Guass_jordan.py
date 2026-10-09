from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


def gauss_jordan(matrix):
    mat = [row[:] for row in matrix]
    rows = len(mat)
    cols = len(mat[0])
    
    r = 0  # Current row

    for c in range(cols):

        # Find pivot row
        pivot = None
        for i in range(r, rows):
            if mat[i][c] != 0:
                pivot = i
                break

        # If no pivot in this column → skip
        if pivot is None:
            continue

        # Swap pivot row with current row
        if pivot != r:
            mat[r], mat[pivot] = mat[pivot], mat[r]

        # Normalize pivot row
        pivot_val = mat[r][c]
        mat[r] = [x / pivot_val for x in mat[r]]

        # Eliminate other rows
        for i in range(rows):
            if i != r:
                factor = mat[i][c]
                mat[i] = [mat[i][j] - factor * mat[r][j] for j in range(cols)]

        r += 1
        if r == rows:
            break

    return mat


@app.route("/")
def home():
    return render_template("jordan.html")


@app.route("/solve", methods=["POST"])
def solve():
    try:
        matrix = request.form.getlist("matrix")

        # convert input rows
        processed = []
        for r in matrix:
            processed.append([float(x) for x in r.split()])

        result = gauss_jordan(processed)

        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
