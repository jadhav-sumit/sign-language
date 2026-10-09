from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("first.html")

@app.route("/add", methods=["POST"])
def add():
    try:
        rows = int(request.form["rows"])
        cols = int(request.form["cols"])

        # Read Matrix A
        A = []
        for i in range(rows):
            row = []
            for j in range(cols):
                row.append(int(request.form.get(f"A{i}{j}", 0)))
            A.append(row)

        # Read Matrix B
        B = []
        for i in range(rows):
            row = []
            for j in range(cols):
                row.append(int(request.form.get(f"B{i}{j}", 0)))
            B.append(row)

        # Addition
        C = []
        for i in range(rows):
            row = []
            for j in range(cols):
                row.append(A[i][j] + B[i][j])
            C.append(row)

        return render_template("first.html", result=C, rows=rows, cols=cols, matrix_a=A, matrix_b=B)
    
    except Exception as e:
        return render_template("first.html", error=str(e))

if __name__ == "__main__":
    app.run(debug=True)