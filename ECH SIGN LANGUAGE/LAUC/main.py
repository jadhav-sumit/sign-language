from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("main.html")  # Load frontend


def minor_2x2(a, b, c, d):
    """Return determinant of 2x2 matrix."""
    return a*d - b*c


def determinant_3x3(matrix):
    """
    Compute determinant of a 3x3 matrix using cofactor expansion.
    | a b c |
    | d e f |
    | g h i |
    """
    a, b, c = matrix[0]
    d, e, f = matrix[1]
    g, h, i = matrix[2]

    det = (
        a * minor_2x2(e, f, h, i)
        - b * minor_2x2(d, f, g, i)
        + c * minor_2x2(d, e, g, h)
    )
    return det


@app.route("/determinant3", methods=["POST"])
def det3():
    try:
        # HTML Form
        matrix = request.form.getlist("matrix")

        # JSON API
        if not matrix:
            matrix = request.json.get("matrix")

        # Convert rows to float list
        processed = []
        for r in matrix:
            processed.append(
                [float(x) for x in r.split()] if isinstance(r, str) else r
            )

        # Validate 3x3 matrix
        if len(processed) != 3 or any(len(row) != 3 for row in processed):
            return jsonify({"error": "Matrix must be 3x3"}), 400

        # Compute determinant
        det = determinant_3x3(processed)

        return jsonify({
            "matrix": processed,
            "determinant": det
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
