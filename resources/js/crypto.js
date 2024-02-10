const table_coin = document.querySelector('.array-content')
const query = decodeURIComponent(window.location.search.split("?q=")[1])
const name_c = document.querySelector('.name-crypto');
const logo_crypto = document.querySelector('.logo_crypto');
name_c.innerHTML = `${query.charAt(0).toUpperCase() + query.slice(1)}`

const fLoad_crypto = async() => {
    try {
        const response = await fetch(
            LINK_TO_DATA__coin.replace('__COIN__', query)
        );
        return await response.json()
    } catch (error) {
        return error.message
    }
}
const fLoad_cryptoIMG = async() => {
    try {
        const response = await fetch(`resources/logos/${query}.png`);
        return await response.blob()
    } catch (error) {
        return error.message
    }
}

fLoad_crypto()
    .then(r => {
        fLoad_table(r)
    })

fLoad_cryptoIMG()
    .then(r => {
        const data = (r.type === 'image/png') ? r : "null"
        if(r.type == 'image/png'){
            logo_crypto.src = `resources/logos/${query}.png`
        }else{
            console.log("no");
        }
    })


const fLoad_table = async(r) => {
    console.log(r, typeof r);

    if(typeof r !== 'object'){
        const cont = document.querySelector('.container-error')
        cont.classList.remove('hidden')
        table_coin.classList.add('hidden')
    }

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