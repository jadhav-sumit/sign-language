from flask import Flask, request, jsonify, render_template
import numpy as np

app = Flask(__name__)

# -------------------- ROUTES -------------------- #

@app.route("/")
def home():
    return render_template("front.html")

@app.route("/rankpage")
def rank_page():
    return render_template("rank.html")

@app.route("/operations")
def operations_page():
    return render_template("matrix_operation.html")

@app.route("/linear")
def linear_page():
    return render_template("linear.html")

@app.route("/add")
def add_page():
    return render_template("add.html")

@app.route("/subtract")
def subtract_page():
    return render_template("sub.html")

@app.route("/multiply")
def multiply_page():
    return render_template("index.html")

@app.route("/solver")
def solver_page():
    return render_template("frontpage.html")

@app.route("/scalar")
def scalar_page():
    return render_template("scalar.html")

@app.route("/minor")
def minor_page():
    return render_template("minor.html")

@app.route("/cofactor")
def cofactor_page():
    return render_template("cofactor.html")

# -------------------- API: MATRIX RANK -------------------- #
@app.route("/rank", methods=["POST"])
def rank_matrix():
    data = request.get_json()
    matrix = data.get("matrix")

    if matrix is None:
        return jsonify({"error": "Matrix not provided"}), 400

    try:
        arr = np.array(matrix, dtype=float)
        rank_value = int(np.linalg.matrix_rank(arr))
        return jsonify({"rank": rank_value})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# -------------------- MAIN -------------------- #
if __name__ == "__main__":
    app.run(debug=True)
