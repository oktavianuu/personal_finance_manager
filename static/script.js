document.getElementById('transaction-form').addEventListener('submit', function (e) {
    e.preventDefault();
    const data = {
        user_id: document.getElementById('user_id').value,
        amount: document.getElementById('amount').value,
        date: document.getElementById('date').value,
        category: document.getElementById('category').value
    };
    fetch('/transactions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(response => response.json()).then(data => {
        alert(data.message);
    });
});

function predict() {
    const user_id = document.getElementById('user_id').value;
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({user_id})
    }).then(response => response.json()).then(data => {
        document.getElementById('prediction').innerText = `Predicted next month's expense: ${data.predicted_expense}`;
    });
}
