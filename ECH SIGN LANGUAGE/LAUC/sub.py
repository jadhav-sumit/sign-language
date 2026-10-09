from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("sub.html")

@app.route("/subtract", methods=["POST"])
def subtract():
    rows = int(request.form["rows"])
    cols = int(request.form["cols"])

    # Read Matrix A
    A = []
    for i in range(rows):
        row = []
        for j in range(cols):
            key = f"A{i}{j}"
            row.append(int(request.form[key]))
        A.append(row)

    # Read Matrix B
    B = []
    for i in range(rows):
        row = []
        for j in range(cols):
            key = f"B{i}{j}"
            row.append(int(request.form[key]))
        B.append(row)

    # Matrix Subtraction: C = A - B
    C = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(A[i][j] - B[i][j])
        C.append(row)

    return render_template("sub.html", rows=rows, cols=cols, C=C)

if __name__ == "__main__":
    app.run(debug=True)
