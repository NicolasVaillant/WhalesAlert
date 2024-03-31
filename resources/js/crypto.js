const table_coin = document.querySelector('.array-content')
const query = decodeURIComponent(window.location.search.split("?q=")[1])
const name_c = document.querySelector('.name-crypto');
const logo_crypto = document.querySelector('.logo_crypto');
name_c.innerHTML = `${query.charAt(0).toUpperCase() + query.slice(1)}`

if(variables.version === "2.0.0"){
    const checkbox_fav_crypto = document.querySelector('#fav-crypto');
    const toggle_fav = document.querySelector('.toggle_fav')

    const stored_fav = JSON.parse(localStorage.getItem(label__favorite_elements))
    if(stored_fav !== null){
        if(typeof stored_fav.data === 'string'){
            if(stored_fav.data == query){
                checkbox_fav_crypto.setAttribute("checked", true)
                toggle_fav.classList.replace('fa-regular', 'fa-solid')
            }
        }else{
            stored_fav.data.forEach(e => {
                if(e == query){
                    checkbox_fav_crypto.setAttribute("checked", true)
                    toggle_fav.classList.replace('fa-regular', 'fa-solid')
                }
            })
        }
    }
    const label = document.querySelector('.label-crypto-fav');
    label.classList.remove('hidden')
    checkbox_fav_crypto.addEventListener('change', (e) => {
        checkFav(e)
    });

    const checkFav = (e) => {
        if (e.target.checked) {
            toggle_fav.classList.replace('fa-regular', 'fa-solid');
            const stored_fav = JSON.parse(localStorage.getItem(label__favorite_elements));
            let newData;
            if (stored_fav !== null) {
                newData = [query, ...stored_fav.data];
            } else {
                newData = [query];
            }
            localStorage.setItem(label__favorite_elements, JSON.stringify({
                status: 'success',
                data: newData
            }));
        } else {
            toggle_fav.classList.replace('fa-solid', 'fa-regular');
            const stored_fav = JSON.parse(localStorage.getItem(label__favorite_elements));
            if (stored_fav !== null) {
                const filteredData = stored_fav.data.filter(item => item !== query);
                localStorage.setItem(label__favorite_elements, JSON.stringify({
                    status: 'success',
                    data: filteredData
                }));
            }
        }
    }
}

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

const fLoad_cryptoIMG = async(input) => {
    try {
        const response = await fetch(`resources/logos/${input}.png`);
        return await response.blob()
    } catch (error) {
        return error.message
    }
}

fLoad_crypto_tx()
    .then(r => {
        createLabelArray()
        fLoad_table(r)
    })

fLoad_crypto_coin()
    .then(r => {
        const data = (typeof r === "object") ? r : "null"
        setAsideInfo(data)
    })

fLoad_cryptoIMG(query)
    .then(r => {
        const data = (r.type === 'image/png') ? r : "null"
        if(r.type == 'image/png'){
            logo_crypto.src = `resources/logos/${query}.png`
        }
    })

let counter_rm = 0
function readMoreInfo() {
    const moreText = document.querySelectorAll(".more");
    const btnText = document.querySelector(".read-more");
    counter_rm++
    if (counter_rm%2 === 0) {
        btnText.innerHTML = "Read more";
        moreText.forEach(e => {
            e.style.display = "none";
        })
    } else {
        btnText.innerHTML = "Read less";
        moreText.forEach(e => {
            if (e.tagName.toLowerCase() === 'li') {
                e.style.display = "list-item";
            }else{
                e.style.display = "block";
            }
        })
    }
}

const setAsideInfo = (data) => {
    const info_c = document.querySelector('.info-crypto')
    const info = document.querySelector('.info-crypto .description-text')
    const duplicated_info = document.querySelector('.duplicated-info')
    const container = document.querySelector('.crypto-info')
    const symbol = document.querySelector('.crypto-info-symbol')
    const read_more = document.querySelector(".read-more");

    if(data == "null" || data.length === 1){
        container.closest('.container-split').classList.add('no-more-info')
        container.closest('.col-more-info .crypto-info').classList.add('hidden')
        container.closest('.col-more-info .w_bg').classList.add('padUpd')
        container.closest('.col-more-info').querySelector('.crypto-info-error').classList.remove('hidden')
        duplicated_info.classList.add('hidden')
        info_c.classList.add('hidden')
        suggestMoreCrypto()
        return
    } else{
        symbol.innerText = data.symbol
        info.innerHTML = data.description
    
        const all = info.querySelectorAll('*')
        if(all.length <= 2){
            read_more.classList.add('hidden')
        }else{
            all.forEach((e, i) => {
                if(i > 2)
                    e.classList.add('more')
            })
        }
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
    // percent_change_24h.innerText = `${data.quotes.USD.percent_change_24h}%`
    let calc_market_cap = data.supply*data.last_price_usd
    price.innerText = data.last_price_usd.toLocaleString("us-US", {style: "currency", currency: "USD"})
    price_dup.innerText = data.last_price_usd.toLocaleString("us-US", {style: "currency", currency: "USD"})
    market_cap.innerText = calc_market_cap.toLocaleString("us-US", {style: "currency", currency: "USD"})
    dup_market_cap.innerText = "?"
    // market_cap_change.innerText = `${data.quotes.USD.market_cap_change_24h}%`
    volume_24h.innerText = data.volume_24_usd.toLocaleString("us-US", {style: "currency", currency: "USD"})
    dup_volume_24h.innerText = data.volume_24_usd.toLocaleString("us-US", {style: "currency", currency: "USD"})
    // volume_24h_change.innerText = `${data.quotes.USD.volume_24h_change_24h}%`
    if(data.total_supply !== null){
        max_supply.innerText = data.total_supply.toLocaleString("us-US", {style: "currency", currency: data.symbol})
    }else{
        max_supply.classList.add('max-supply-no-info')
    }
    circulating_supply.innerText = data.supply.toLocaleString("us-US", {style: "currency", currency: data.symbol})
    refresh_date.innerText = new Date(data.last_update).toLocaleString()
}

const suggestMoreCrypto = async () => {
    if(variables.version === "2.0.0"){
        const card = document.querySelector('.more-crypto-redirect')
        const grid = document.querySelector('.grid-elements')
        card.classList.remove('hidden')
        try {
            const response = await fetch(LINK_TO_DATA__Files);
            data = await response.json()
            const shuffledFiles = data.files.sort(() => Math.random() - 0.5);
            const selectedFiles = shuffledFiles.slice(0, 4);
            if (selectedFiles.includes(query)) {
                selectedFiles = selectedFiles.filter(file => file !== query);
                const remainingFilesCount = 4 - selectedFiles.length;
                const remainingFiles = shuffledFiles.filter(file => file !== query);
                const additionalFiles = remainingFiles.slice(0, remainingFilesCount);
                selectedFiles = selectedFiles.concat(additionalFiles);
            }
            selectedFiles.forEach(async (e) => {
                const container = document.createElement('a')
                container.classList.add('suggested-currency')
                const text = document.createElement('p')
                const img = document.createElement('img')
                text.innerHTML = e
                container.href = `crypto.html?q=${e}`
                fLoad_cryptoIMG(e).then(r => {
                    if(r.type == 'image/png'){
                        img.src = `resources/logos/${e}.png`
                        container.appendChild(img)
                    }
                })
                container.appendChild(text)
                document.querySelector('.grid-elements').appendChild(container)
            })
        } catch (error) {
            return error.message
        }
    }
}

const createLabelArray = () => {
    const row_table_def = document.querySelectorAll('.row_table_def')
    row_table_def.forEach(td => {
        variables.arrayCryptoLabel.forEach(element => {
            const th = document.createElement('th')
            th.innerText = element
            td.appendChild(th)
        });  
    })
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
        pagingType: 'simple',
        // initComplete: function (settings) {
        //     const dataTables_length = document.querySelector('.dataTables_length')
        //     const dataTables_info = document.querySelector('.dataTables_info')
        //     dataTables_info.appendChild(dataTables_length)
        // }
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