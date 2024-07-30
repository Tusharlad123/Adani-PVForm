@app.route('/load_data')
def load_data():
    plant = request.args.get('plant')
    block = request.args.get('block')
    filter_plant = df[df['Plantname'] == plant]
    mytable = filter_plant.Tablename.unique()
    mytable = listToString(mytable)
    mytable = remove(mytable)
    selectQuery = f"SELECT * FROM agel-svc-winddata-dmz-prod.winddata.{mytable} WHERE Plant = '{plant}'"
    df1 = client.query(selectQuery).to_dataframe()
    df2 = df1[df1['Plant'] == plant]

    if block:
        block_data = df2[df2['Block'] == block]
        return jsonify(block_data.to_dict(orient='records'))

    blocks = df2.Block.unique()

    # Calculate summary statistics
    rt = df2.astype(str)
    totalblocks = len(rt.Block.unique())
    rt['DCCapacityKWp'] = pd.to_numeric(rt['DCCapacityKWp'], errors='coerce')
    rt1 = rt[rt.DCCapacityKWp.notnull()]
    totaldcMWp = round(sum(rt1['DCCapacityKWp']) / 1000, 2)

    summary = {
        'total_blocks': totalblocks,
        'total_dc_mwp': totaldcMWp
    }

    return jsonify({
        'blocks': blocks.tolist(),
        'summary': summary
    })


#js
function selectPlant() {
    const dropdown = document.getElementById('plantDropdown');
    currentPlant = dropdown.value;
    fetch(`/load_data?plant=${currentPlant}`)
        .then(response => response.json())
        .then(data => {
            createBlockDropdown(data.blocks, data.summary);
            console.log(data.summary); // Debugging line to check summary data
        })
        .catch(error => console.error('Error fetching plant data:', error));
}

function createBlockDropdown(blocks, summary) {
    const blockDropdown = document.getElementById('blockDropdown');
    blockDropdown.innerHTML = '';
    blocks.forEach(block => {
        const option = document.createElement('option');
        option.value = block;
        option.text = block;
        blockDropdown.appendChild(option);
    });
    blockDropdown.style.display = 'block';
    
    // Display summary
    const summaryContainer = document.getElementById('summaryContainer');
    const totalBlocks = document.getElementById('totalBlocks');
    const totalDcMWp = document.getElementById('totalDcMWp');
    
    totalBlocks.textContent = `Total Blocks: ${summary.total_blocks}`;
    totalDcMWp.textContent = `Total DC MWp: ${summary.total_dc_mwp}`;
    
    summaryContainer.style.display = 'block';
}

# html css
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PV Form</title>
    <style>
        /* Your CSS styles */
    </style>
</head>
<body>
    <div class="header">
        <img src="https://logowik.com/content/uploads/images/adani-renewables-green-energy1681.logowik.com.webp" alt="Company Logo" class="logo">
        <h1>PV Form</h1>
    </div>
    <div class="underline"></div>
    <div class="dropdown-container">
        <select class="dropdown" id="plantDropdown" onchange="selectPlant()">
            {% for plant in plants %}
            <option value="{{ plant }}">{{ plant }}</option>
            {% endfor %}
        </select>
        <select class="dropdown" id="blockDropdown" onchange="selectBlock()" style="display:none;">
            <!-- Options will be dynamically added here -->
        </select>
    </div>
    <div class="summary-container" id="summaryContainer" style="display: none;">
        <h3>Summary</h3>
        <p id="totalBlocks"></p>
        <p id="totalDcMWp"></p>
    </div>
    <div class="main-content">
        <input type="text" placeholder="Search.." class="search-bar" oninput="searchTable()">
        <div id="data"></div>
        <button onclick="addRow()">Add Row</button>
        <button onclick="saveData()">Save Data</button>
    </div>

    <script>
        let currentBlock = '';
        let currentPlant = '';

        // JavaScript functions defined here

        function selectPlant() {
            const dropdown = document.getElementById('plantDropdown');
            currentPlant = dropdown.value;
            fetch(`/load_data?plant=${currentPlant}`)
                .then(response => response.json())
                .then(data => {
                    createBlockDropdown(data.blocks, data.summary);
                    console.log(data.summary); // Debugging line to check summary data
                })
                .catch(error => console.error('Error fetching plant data:', error));
        }

        function createBlockDropdown(blocks, summary) {
            const blockDropdown = document.getElementById('blockDropdown');
            blockDropdown.innerHTML = '';
            blocks.forEach(block => {
                const option = document.createElement('option');
                option.value = block;
                option.text = block;
                blockDropdown.appendChild(option);
            });
            blockDropdown.style.display = 'block';

            // Display summary
            const summaryContainer = document.getElementById('summaryContainer');
            const totalBlocks = document.getElementById('totalBlocks');
            const totalDcMWp = document.getElementById('totalDcMWp');

            totalBlocks.textContent = `Total Blocks: ${summary.total_blocks}`;
            totalDcMWp.textContent = `Total DC MWp: ${summary.total_dc_mwp}`;

            summaryContainer.style.display = 'block';
        }

        function selectBlock() {
            const dropdown = document.getElementById('blockDropdown');
            currentBlock = dropdown.value;
            loadData(currentBlock);
        }

        function loadData(block) {
            fetch(`/load_data?plant=${currentPlant}&block=${block}`)
                .then(response => response.json())
                .then(data => {
                    let table = '<table><tr>';
                    for (let key in data[0]) {
                        table += `<th>${key}</th>`;
                    }
                    table += `<th>Actions</th></tr>`;
                    data.forEach(row => {
                        table += '<tr>';
                        for (let key in row) {
                            table += `<td contenteditable="true">${row[key]}</td>`;
                        }
                        table += '<td><button class="delete-button" onclick="deleteRow(this)">Delete</button></td></tr>';
                    });
                    table += '</table>';
                    document.getElementById('data').innerHTML = table;
                    const tableElement = document.querySelector('table');
                    if (tableElement) {
                        tableElement.style.opacity = 1;
                        tableElement.style.transform = 'translateY(0)';
                    }
                });
        }

        function searchTable() {
            const input = document.querySelector('.search-bar');
            const filter = input.value.toLowerCase();
            const table = document.querySelector('table');
            const tr = table.getElementsByTagName('tr');

            for (let i = 1; i < tr.length; i++) {
                let display = false;
                const td = tr[i].getElementsByTagName('td');
                for (let j = 0; j < td.length; j++) {
                    if (td[j]) {
                        if (td[j].innerText.toLowerCase().indexOf(filter) > -1) {
                            display = true;
                        }
                    }
                }
                tr[i].style.display = display ? '' : 'none';
            }
        }

        function addRow() {
            const table = document.querySelector('table');
            const newRow = table.insertRow();
            const cells = table.rows[0].cells.length;
            for (let i = 0; i < cells - 1; i++) {
                const newCell = newRow.insertCell(i);
                newCell.contentEditable = 'true';
                newCell.textContent = '';
            }
            const actionCell = newRow.insertCell(cells - 1);
            actionCell.innerHTML = '<button class="delete-button" onclick="deleteRow(this)">Delete</button>';
        }

        function deleteRow(button) {
            const row = button.closest('tr');
            row.parentNode.removeChild(row);
        }

        function saveData() {
            const table = document.querySelector('table');
            const rows = table.getElementsByTagName('tr');
            const data = [];
            for (let i = 1; i < rows.length; i++) {
                const row = rows[i];
                const cells = row.getElementsByTagName('td');
                const rowData = {};
                for (let j = 0; j < cells.length - 1; j++) {
                    const key = table.rows[0].cells[j].innerText;
                    rowData[key] = cells[j].innerText;
                }
                data.push(rowData);
            }
            fetch('/save_data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(result => {
                console.log(result);
            })
            .catch(error => {
                console.error('Error saving data:', error);
            });
        }
    </script>
</body>
</html>
