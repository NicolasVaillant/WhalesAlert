const query = decodeURIComponent(window.location.search.split("?q=")[1])
const name_c = document.querySelector('.name-crypto');
name_c.innerHTML = `${query.charAt(0).toUpperCase() + query.slice(1)}`

const fLoad_crypto = async() => {
    try {
        const response = await fetch(`resources/data/${query}.json`);
        return await response.json()
    } catch (error) {
        return error.message
    }
}

fLoad_crypto()
    .then(r => {
        const data = (typeof r === 'object') ? r : "No currency found"
        fLoad_table(r)
    })


const fLoad_table = async(r) => {
    let leaderboard_table = $('#table_crypto_unique').DataTable({
        data: r,
        lengthMenu: [
            [10, 25, 50],
            [10, 25, 50],
        ],
        columns: [
            { data: 'amount'},
            { data: 'value' },
            { data: 'porcentage_supply' },
            { data: 'url' }
        ],
        columnDefs: [{
            "defaultContent": "-",
            "targets": "_all"
        }],
        order: [[0, 'asc']],
        scrollX: "300px",
        "searching": false,
        "ordering": true,
        "autoWidth": false,
        "responsive": false,
    });
}