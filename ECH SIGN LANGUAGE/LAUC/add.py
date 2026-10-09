from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/add")
def home():
    return render_template("add.html")

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
                value = request.form.get(f"A{i}{j}", "0")
                row.append(int(value))
            A.append(row)

        # Read Matrix B
        B = []
        for i in range(rows):
            row = []
            for j in range(cols):
                value = request.form.get(f"B{i}{j}", "0")
                row.append(int(value))
            B.append(row)

        # Addition
        C = []
        for i in range(rows):
            row = []
            for j in range(cols):
                row.append(A[i][j] + B[i][j])
            C.append(row)

        return render_template("add.html", 
                              result=C, 
                              rows=rows, 
                              cols=cols, 
                              matrix_a=A, 
                              matrix_b=B)
    
    except ValueError as e:
        return render_template("add.html", error=f"Invalid input: {str(e)}")
    except Exception as e:
        return render_template("add.html", error=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True)