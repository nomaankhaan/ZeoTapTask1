document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('eligibilityForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = {
            rule: {
                type: "operator",
                operator: "AND",
                left: {
                    type: "comparison",
                    field: "age",
                    operator: ">=",  // Changed from GTE to >=
                    value: 18
                },
                right: {
                    type: "operator",
                    operator: "OR",
                    left: {
                        type: "comparison",
                        field: "income",
                        operator: ">",  // Changed from GT to >
                        value: 50000
                    },
                    right: {
                        type: "comparison",
                        field: "spend",
                        operator: ">",  // Changed from GT to >
                        value: 10000
                    }
                }
            },
            user_data: {
                age: parseInt(document.getElementById('age').value),
                department: document.getElementById('department').value,
                income: parseFloat(document.getElementById('income').value),
                spend: parseFloat(document.getElementById('spend').value)
            }
        };

        try {
            const response = await fetch('/api/evaluate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();
            const resultDiv = document.getElementById('result');
            
            if (response.ok) {
                resultDiv.className = 'result ' + (data.eligible ? 'success' : 'error');
                resultDiv.textContent = data.eligible 
                    ? 'Congratulations! You are eligible.' 
                    : 'Sorry, you are not eligible.';
            } else {
                resultDiv.className = 'result error';
                resultDiv.textContent = 'Error: ' + data.detail;
            }
        } catch (error) {
            const resultDiv = document.getElementById('result');
            resultDiv.className = 'result error';
            resultDiv.textContent = 'Error: Could not connect to the server.';
        }
    });
});