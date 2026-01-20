function refreshData() {
    fetch("/refresh")
        .then(res => res.json())
        .then(data => {
            let rows = `
                <tr>
                    <th>Crypto</th>
                    <th>Price</th>
                    <th>24h Change</th>
                    <th>Volume</th>
                </tr>
            `;

            data.forEach(c => {
                let cls = c.change > 0 ? "green" : "red";
                rows += `
                    <tr>
                        <td>${c.name}</td>
                        <td>${c.price}</td>
                        <td class="${cls}">${c.change}%</td>
                        <td>${c.volume}</td>
                    </tr>
                `;
            });

            document.getElementById("cryptoTable").innerHTML = rows;
        });
}
