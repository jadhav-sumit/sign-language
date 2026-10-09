from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("Gauss.html")   # optional


def gauss_elimination(matrix):
    """
    Performs Gauss Elimination and returns:
    - Upper triangular matrix (Row Echelon Form)
    - Steps (optional)
    """
    steps = []
    m = [row[:] for row in matrix]  # deep copy
    n = len(m)

    for i in range(n):
        # Find pivot
        pivot = m[i][i]
        if pivot == 0:
            # swap with a row below that has non-zero pivot
            for k in range(i + 1, n):
                if m[k][i] != 0:
                    m[i], m[k] = m[k], m[i]
                    steps.append({"action": f"Swap row {i+1} with row {k+1}", "matrix": [r[:] for r in m]})
                    pivot = m[i][i]
                    break

        if pivot == 0:
            steps.append({"action": f"No pivot found in column {i+1}", "matrix": [r[:] for r in m]})
            continue

        # Eliminate below
        for j in range(i + 1, n):
            if m[j][i] == 0:
                continue

            factor = m[j][i] / pivot
            for k in range(i, n):
                m[j][k] -= factor * m[i][k]

            steps.append({
                "action": f"R{j+1} = R{j+1} - ({factor:.2f}) * R{i+1}",
                "matrix": [r[:] for r in m]
            })

    return m, steps


@app.route("/gauss", methods=["POST"])
def gauss():
    try:
        # From HTML <form>
        matrix = request.form.getlist("matrix")

        # From JSON
        if not matrix:
            data = request.json
            matrix = data.get("matrix")

        # Convert matrix rows to lists of floats
        processed = []
        for r in matrix:
            processed.append([float(x) for x in r.split()] if isinstance(r, str) else r)

        # Must be square or rectangular allowed
        if len(processed) < 2 or len(processed[0]) < 2:
            return jsonify({"error": "Matrix must have at least 2 rows and 2 columns"}), 400

        # Perform Gauss Elimination
        result, steps = gauss_elimination(processed)

        return jsonify({
            "input_matrix": processed,
            "row_echelon_form": result,
            "steps": steps
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)