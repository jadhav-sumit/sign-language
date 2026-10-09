from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('scalar.html')


@app.route('/scalar_mul', methods=['POST'])
def scalar_mul():
    try:
        data = request.get_json()

        scalar = float(data.get('scalar'))
        matrix_rows = data.get('matrix')

        # Convert each row (string) into list of floats
        processed_matrix = []
        for row in matrix_rows:
            numbers = [float(x) for x in row.split()]
            processed_matrix.append(numbers)

        # Perform multiplication
        result = [[scalar * x for x in row] for row in processed_matrix]

        return jsonify({
            "result": result
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
