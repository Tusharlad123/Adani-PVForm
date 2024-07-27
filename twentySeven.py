#code t be added
 <button onclick="addRow()">Add Row</button>

 function addRow() {
        const table = document.querySelector('table');
        if (!table) return;

        const headers = Array.from(table.querySelectorAll('th')).map(th => th.textContent);
        let newRow = '<tr>';
        headers.forEach(header => {
            if (header !== 'Actions') {
                newRow += `<td contenteditable="true"></td>`;
            }
        });
        newRow += '<td><button class="delete-button" onclick="deleteRow(this)">Delete</button></td></tr>';
        table.innerHTML += newRow;
    }


    function saveData() {
        let data = [];

        let table = document.querySelector('table');
        let headers = Array.from(table.querySelectorAll('th')).map(th => th.textContent);
        let rows = table.querySelectorAll('tr');
        for (let i = 1; i < rows.length; i++) {
            let row = {};
            let cells = rows[i].querySelectorAll('td');
            headers.forEach((header, index) => {
                if (header !== 'Actions') {
                    row[header] = cells[index].textContent;
                }
            });
            data.push(row);
        }
        fetch(`/save_data?block=${currentBlock}&plant=${currentPlant}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(result => alert(result.message));
    }
