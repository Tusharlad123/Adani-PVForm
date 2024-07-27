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


def save_data():
    block = request.args.get('block')
    plant = request.args.get('plant')
    data = request.json
    print(data)
    block_df = pd.DataFrame(data)

    filter_plant = df[df['Plantname'] == plant]
    mytable = filter_plant.Tablename.unique()
    mytable = listToString(mytable)
    mytable = remove(mytable)

    selectQuery = "SELECT * FROM agel-svc-winddata-dmz-prod.winddata." + mytable
    df11 = client.query(selectQuery).to_dataframe()

    df22 = df11[df11['Block'] != block].append(block_df, ignore_index=True)
    df33 = df22[df22['Plant'] == plant]

    print(df22)

    csv_file_path = "D:\\OneDrive - Adani\\Documents\\" + plant + ".csv"
    df33.to_csv(csv_file_path, index=False)

    table_id = "agel-svc-winddata-dmz-prod.winddata." + mytable
    table = bigquery.Table(table_id)
    job_config = bigquery.LoadJobConfig()
    job_config.write_disposition = "WRITE_TRUNCATE"  # Overwrite table truncate
    df22 = df22.astype(str)
    job = client.load_table_from_dataframe(df22, table, job_config=job_config)
    return jsonify({"message": "Data saved successfully"})
