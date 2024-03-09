const table_coin = document.querySelector('.array-content')
const query = decodeURIComponent(window.location.search.split("?q=")[1])
const name_c = document.querySelector('.name-crypto');
const logo_crypto = document.querySelector('.logo_crypto');
name_c.innerHTML = `${query.charAt(0).toUpperCase() + query.slice(1)}`

const fLoad_crypto_tx = async() => {
    try {
        const response = await fetch(
            LINK_TO_DATA__tx.replace('__COIN__', query)
        );
        return await response.json()
    } catch (error) {
        return error.message
    }
}

const fLoad_crypto_coin = async() => {
    try {
        const response = await fetch(
            LINK_TO_DATA__coin.replace('__COIN__', query.toLowerCase())
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

fLoad_crypto_tx()
    .then(r => {
        fLoad_table(r)
    })

fLoad_crypto_coin()
    .then(r => {
        const data = (r.length === 1) ? r[0] : "null"
        setAsideInfo(data)
    })

fLoad_cryptoIMG()
    .then(r => {
        const data = (r.type === 'image/png') ? r : "null"
        if(r.type == 'image/png'){
            logo_crypto.src = `resources/logos/${query}.png`
        }else{}
    })


const setAsideInfo = (data) => {
    console.log(data);
    const duplicated_info = document.querySelector('.duplicated-info')
    const container = document.querySelector('.crypto-info')
    const symbol = document.querySelector('.crypto-info-symbol')
    if(data == "null"){
        container.closest('.container-split').classList.add('no-more-info')
        container.closest('.col-more-info').classList.add('hidden')
        duplicated_info.classList.add('hidden')
    } else{
        symbol.innerText = data.symbol
    }
    const price = document.querySelector('.quote-USD-price')
    const price_dup = document.querySelector('.dup-quote-USD-price')
    const percent_change_24h = document.querySelector('.percent-24h')
    const market_cap = document.querySelector('.market-cap')
    const dup_market_cap = document.querySelector('.dup-market-cap')
    const market_cap_change = document.querySelector('.market-cap-change')
    const volume_24h = document.querySelector('.volume-24h')
    const dup_volume_24h = document.querySelector('.dup-volume-24h')
    const volume_24h_change = document.querySelector('.volume-24h-change')
    const max_supply = document.querySelector('.max-supply')
    const circulating_supply = document.querySelector('.circulating-supply')
    const refresh_date = document.querySelector('.refresh-date')
    percent_change_24h.innerText = `${data.quotes.USD.percent_change_24h}%`

    price.innerText = data.quotes.USD.price.toLocaleString("us-US", {style: "currency", currency: "USD"})
    price_dup.innerText = data.quotes.USD.price.toLocaleString("us-US", {style: "currency", currency: "USD"})
    market_cap.innerText = data.quotes.USD.market_cap.toLocaleString("us-US", {style: "currency", currency: "USD"})
    dup_market_cap.innerText = data.quotes.USD.market_cap.toLocaleString("us-US", {style: "currency", currency: "USD"})
    market_cap_change.innerText = `${data.quotes.USD.market_cap_change_24h}%`
    volume_24h.innerText = data.quotes.USD.volume_24h.toLocaleString("us-US", {style: "currency", currency: "USD"})
    dup_volume_24h.innerText = data.quotes.USD.volume_24h.toLocaleString("us-US", {style: "currency", currency: "USD"})
    volume_24h_change.innerText = `${data.quotes.USD.volume_24h_change_24h}%`
    max_supply.innerText = data.max_supply.toLocaleString("us-US", {style: "currency", currency: "BTC"})
    circulating_supply.innerText = data.circulating_supply.toLocaleString("us-US", {style: "currency", currency: "BTC"})
    refresh_date.innerText = new Date(data.last_updated).toLocaleString()
}

const fLoad_table = async(r) => {
    
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
        scrollX: "300px",
        "searching": false,
        "ordering": false,
        "autoWidth": false,
        "responsive": false,
    });

    $('#table_crypto_unique tbody').on('click', 'tr', function (e) {
        const url = $(this)[0].querySelectorAll('td')[3].innerText
        if ($(this).hasClass('selected')) {
            $(this).removeClass('selected');
            modal.style.display = 'none';
        } else {
            leaderboard_table.$('tr.selected').removeClass('selected');
            contextMenuCreation(url, e.clientX, e.clientY, true)
        }
    })
}