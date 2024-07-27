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


