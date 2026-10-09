
document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const matrixA = document.getElementById('matrixA');
    const matrixB = document.getElementById('matrixB');
    const rowsA = document.getElementById('rowsA');
    const colsA = document.getElementById('colsA');
    const rowsB = document.getElementById('rowsB');
    const colsB = document.getElementById('colsB');
    const sizeLabelA = document.getElementById('sizeLabelA');
    const sizeLabelB = document.getElementById('sizeLabelB');
    const resultBox = document.getElementById('result');
    const stepsBox = document.getElementById('steps');
    const stepsContent = document.getElementById('stepsContent');
    const operationButtons = document.querySelectorAll('.btn');
    
    // Current state
    let currentRowsA = 3, currentColsA = 3;
    let currentRowsB = 3, currentColsB = 3;
    let currentOperation = null;
    
    // Initialize matrices
    createMatrix('A', currentRowsA, currentColsA);
    createMatrix('B', currentRowsB, currentColsB);
    
    // Update matrix sizes
    rowsA.addEventListener('change', updateMatrixSize);
    colsA.addEventListener('change', updateMatrixSize);
    rowsB.addEventListener('change', updateMatrixSize);
    colsB.addEventListener('change', updateMatrixSize);
    
    // Operation buttons
    operationButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons
            operationButtons.forEach(btn => btn.classList.remove('active'));
            // Add active class to clicked button
            this.classList.add('active');
            currentOperation = this.getAttribute('data-op');
            
            // Update B matrix for equations
            if (['cramer', 'gauss', 'gauss_jordan'].includes(currentOperation)) {
                rowsB.value = currentRowsA;
                colsB.value = 1;
                updateMatrixSize();
            }
            
            // Perform calculation
            calculate();
        });
    });
    
    // Matrix input change listener
    document.addEventListener('input', function(e) {
        if (e.target.classList.contains('matrix-cell')) {
            if (currentOperation) {
                setTimeout(calculate, 500);
            }
        }
    });
    
    // Functions
    function createMatrix(type, rows, cols) {
        const container = type === 'A' ? matrixA : matrixB;
        container.innerHTML = '';
        
        for (let i = 0; i < rows; i++) {
            const rowDiv = document.createElement('div');
            rowDiv.className = 'matrix-row';
            
            for (let j = 0; j < cols; j++) {
                const input = document.createElement('input');
                input.type = 'number';
                input.className = 'matrix-cell';
                input.dataset.row = i;
                input.dataset.col = j;
                input.dataset.matrix = type;
                input.value = (i === j) ? '1' : '0';
                
                rowDiv.appendChild(input);
            }
            
            container.appendChild(rowDiv);
        }
        
        // Update size label
        if (type === 'A') {
            sizeLabelA.textContent = `${rows}×${cols}`;
        } else {
            sizeLabelB.textContent = `${rows}×${cols}`;
        }
    }
    
    function updateMatrixSize() {
        currentRowsA = parseInt(rowsA.value) || 1;
        currentColsA = parseInt(colsA.value) || 1;
        currentRowsB = parseInt(rowsB.value) || 1;
        currentColsB = parseInt(colsB.value) || 1;
        
        createMatrix('A', currentRowsA, currentColsA);
        createMatrix('B', currentRowsB, currentColsB);
        
        if (currentOperation) {
            calculate();
        }
    }
    
    function getMatrixValues(type) {
        const rows = type === 'A' ? currentRowsA : currentRowsB;
        const cols = type === 'A' ? currentColsA : currentColsB;
        const values = [];
        
        for (let i = 0; i < rows; i++) {
            const row = [];
            for (let j = 0; j < cols; j++) {
                const input = document.querySelector(`.matrix-cell[data-matrix="${type}"][data-row="${i}"][data-col="${j}"]`);
                const val = input.value.trim();
                row.push(val === '' ? '0' : val);
            }
            values.push(row.join(','));
        }
        
        return values.join(';');
    }
    
    function calculate() {
        if (!currentOperation) return;
        
        const matrixAStr = getMatrixValues('A');
        const matrixBStr = getMatrixValues('B');
        
        // Show loading
        resultBox.innerHTML = '<div class="placeholder"><div class="icon">⏳</div><p>Calculating...</p></div>';
        stepsBox.style.display = 'none';
        
        // Prepare data
        const data = {
            operation: currentOperation,
            matrixA: matrixAStr,
            matrixB: matrixBStr
        };
        
        // For minor and cofactor operations, ask for position
        if (currentOperation === 'minor' || currentOperation === 'cofactor') {
            const row = prompt(`Enter row number (1 to ${currentRowsA}):`, "1");
            const col = prompt(`Enter column number (1 to ${currentColsA}):`, "1");
            
            if (row && col) {
                data.row = parseInt(row) - 1;
                data.col = parseInt(col) - 1;
            } else {
                return;
            }
        }
        
        // Send request to server
        fetch('/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            displayResult(data);
        })
        .catch(error => {
            showError('Network error: ' + error.message);
        });
    }
    
    function displayResult(data) {
        if (data.error) {
            showError(data.error);
            return;
        }
        
        let resultHTML = '';
        
        if (data.success) {
            resultHTML += `<div class="success">${data.result}</div>`;
            
            if (data.matrix) {
                resultHTML += `<div class="matrix-result">`;
                const rows = data.matrix.split(';');
                rows.forEach(row => {
                    const cells = row.split(',');
                    resultHTML += `<div class="matrix-row" style="justify-content: center;">`;
                    cells.forEach(cell => {
                        resultHTML += `<span style="padding: 5px 10px; margin: 2px; background: white; border: 1px solid #ddd; min-width: 60px; text-align: center;">${cell}</span>`;
                    });
                    resultHTML += `</div>`;
                });
                resultHTML += `</div>`;
            }
            
            if (data.details) {
                stepsContent.textContent = data.details;
                stepsBox.style.display = 'block';
            }
        }
        
        resultBox.innerHTML = resultHTML;
    }
    
    function showError(message) {
        resultBox.innerHTML = `<div class="error">Error: ${message}</div>`;
        stepsBox.style.display = 'none';
    }
    
    // Initialize with default values
    createMatrix('A', 3, 3);
    createMatrix('B', 3, 3);
});