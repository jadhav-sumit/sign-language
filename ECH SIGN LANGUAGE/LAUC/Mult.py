from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":

        # Step 1: Get matrix sizes
        rowsA = int(request.form["rowsA"])
        colsA = int(request.form["colsA"])
        rowsB = int(request.form["rowsB"])
        colsB = int(request.form["colsB"])

        # Validate
        if colsA != rowsB:
            return render_template("index.html",
                                   error="Matrix multiplication not possible! Columns of A must match Rows of B.")

        # Step 2: Read Matrix A
        A = []
        for i in range(rowsA):
            row = []
            for j in range(colsA):
                key = f"A_{i}_{j}"
                row.append(int(request.form[key]))
            A.append(row)

        # Step 3: Read Matrix B
        B = []
        for i in range(rowsB):
            row = []
            for j in range(colsB):
                key = f"B_{i}_{j}"
                row.append(int(request.form[key]))
            B.append(row)

        # Step 4: Matrix multiplication
        C = []
        for i in range(rowsA):
            row = []
            for j in range(colsB):
                val = sum(A[i][k] * B[k][j] for k in range(colsA))
                row.append(val)
            C.append(row)

        return render_template("index.html",
                               rowsA=rowsA, colsA=colsA,
                               rowsB=rowsB, colsB=colsB,
                               A=A, B=B, C=C)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
