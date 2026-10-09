from flask import Flask, render_template, request

app = Flask(__name__)

# ------------------ DETERMINANT FUNCTION ------------------
def det3(a):
    return (
        a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
        - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
        + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0])
    )

# ------------------ ROUTE ------------------
@app.route("/", methods=["GET", "POST"])
def cramer():  # Function name is 'cramer'
    error = None
    detA = x = y = z = None

    if request.method == "POST":
        try:
            # Matrix A
            A = []
            for i in range(3):
                row = []
                for j in range(3):
                    row.append(float(request.form.get(f"A_{i}_{j}")))
                A.append(row)

            # Matrix B
            B = []
            for i in range(3):
                B.append(float(request.form.get(f"B_{i}")))

            detA = det3(A)

            if detA == 0:
                error = "No unique solution! Determinant = 0"
            else:
                Ax = [row[:] for row in A]
                Ay = [row[:] for row in A]
                Az = [row[:] for row in A]

                for i in range(3):
                    Ax[i][0] = B[i]
                    Ay[i][1] = B[i]
                    Az[i][2] = B[i]

                x = det3(Ax) / detA
                y = det3(Ay) / detA
                z = det3(Az) / detA

        except Exception as e:
            error = f"Error: {str(e)}"

    return render_template("cramers.html", detA=detA, x=x, y=y, z=z, error=error)

if __name__ == "__main__":
    app.run(debug=True)
