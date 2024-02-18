backToTop.addEventListener('click', () => {
    window.scrollTo(0, 0)
})

const fLoad_main = async() => {
    try {
        const response = await fetch(LINK_TO_DATA__main);
        return await response.json()
    } catch (error) {
        return error.message
    }
}

const fLoad_trends = async() => {
    try {
        const response = await fetch(LINK_TO_DATA__trends);
        return await response.json()
    } catch (error) {
        return error.message
    }
}

const fLoad_trends_user = async() => {
    try {
        const response = await fetch(LINK_TO_DATA__trends_user);
        return await response.json()
    } catch (error) {
        return error.message
    }
}

const fEdit_main = (data) => {
    const cryptocurrencies = data.cryptocurrencies

    const result = data.cryptocurrencies.filter(obj => obj.Rank === 1 || obj.Rank === 2 || obj.Rank === 3);

    const location = document.querySelector('.col-left-sc')
    result.forEach((e, i) => {
        const element = document.createElement('a')
        const text = document.createElement('p')
        const value = document.createElement('span')
        element.classList.add('card-sh')
        text.innerHTML = e.Name
        element.href = `crypto.html?q=${e.Name}`
        value.innerHTML = (i+1).toString()
        element.appendChild(value)
        element.appendChild(text)
        location.appendChild(element)
    })

    let leaderboard_table = $('#table_crypto').DataTable({
        data: data.cryptocurrencies,
        lengthMenu: [
            [10, 25, 50],
            [10, 25, 50],
        ],
        columns: [
            { data: 'Rank'},
            { data: 'Name' },
            { data: 'Symbol' },
            { data: 'Price' },
            { data: 'Volume' },
            { data: '1h' },
            { data: '24h' },
            { data: '7d' }
        ],
        columnDefs: [{
            "defaultContent": "-",
            "targets": "_all"
        }],
        order: [[0, 'asc']],
        scrollX: "300px",
        "searching": true,
        "ordering": true,
        "autoWidth": true,
        "responsive": true
    });

    $('#table_crypto tbody').on('click', 'tr', function (e) {
        const crypto = $(this)[0].querySelectorAll('td')[1].innerText
        const cryptoDef = crypto.includes(' ') ? crypto.replace(/ /g, '_').toLowerCase() : crypto.toLowerCase()
        if ($(this).hasClass('selected')) {
            $(this).removeClass('selected');
        } else {
            leaderboard_table.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
        contextMenuCreation(cryptoDef, e.clientX, e.clientY)
    })
}

const contextMenuCreation = (text, x, y) => {
    const modal = document.getElementById('modal');
    const actionButton = document.getElementById('open_crypto_from_table');
    const text_modal = document.querySelector('.text_modal');
    modal.style.top = y + 'px';
    modal.style.left = x + 'px';
    actionButton.innerText = `Open ${text}`
    modal.style.display = 'flex';
    actionButton.addEventListener('click', function() {
        window.open(`crypto.html?q=${text}`, "_self")
        modal.style.display = 'none';
    });
}
const close_btn = document.querySelector('.close-btn');
close_btn.addEventListener('click', function() {
    modal.style.display = 'none';
});

const fEdit_Trend_user = (data) => {
    if(data !== 'error'){
        data.forEach((e, i) => {
            const init = document.querySelector('.user-trend-card[data-value="init"]')
            const element = init.cloneNode(true)
            element.setAttribute('data-value', false)
            element.href = `crypto.html?q=${e.urlPart}`
            element.querySelector('.user-trend-card-nb').innerText = (i+1).toString()
            element.querySelector('.user-trend-card-name').innerText = e.title
            element.querySelector('.user-trend-card-value').innerText = e.changeValue
            element.querySelector('.user-trend-card-value').classList.add(`${e.changeDirection}`)
            document.querySelector('.user-trends').appendChild(element)
        })
    }
}

const fEdit_Trend = (data) => {
    const location = document.querySelector('.container-overflow')
    data.forEach(e => {
        const {urlPart, changeValue, changeDirection} = e 
        const element = document.createElement('a')
        element.classList.add('trends-e')
        const status = document.createElement('div')
        status.classList.add('col')
        const status_dir = document.createElement('i')
        status_dir.classList.add('fa-solid', 'fa-caret-up')
        if(changeDirection === 'down'){
            status_dir.classList.add('fa-caret-down')
            status.classList.add('down')
        }else{
            status.classList.add('up')
            status_dir.classList.add('fa-caret-up')
        }
        const status_val = document.createElement('p')
        status_val.innerHTML = changeValue
        status.appendChild(status_dir)
        status.appendChild(status_val)
        const text = document.createElement('p')
        text.innerHTML = urlPart
        element.href = `crypto.html?q=${urlPart}`
        element.appendChild(status)
        element.appendChild(text)
        location.appendChild(element)
    })
}

const fLoad_gainers = async() => {
    try {
        const response = await fetch(LINK_TO_DATA__gainers);
        return await response.json()
    } catch (error) {
        return error.message
    }
}
const fEdit_GL = (data, loc) => {
    const location = document.querySelector('.card-content-gainers')
    data.forEach((element, index) => {
        const {urlPart, title, changeDirection, changeValue} = element 

        // console.log(element);

        const line = document.createElement('a')
        line.classList.add('line')
        line.href = `crypto.html?q=${urlPart}`
        const first_col = document.createElement('div')
        first_col.classList.add('left')
        const name = document.createElement('p')
        name.innerText = `${index+1}. ${urlPart.charAt(0).toUpperCase() + urlPart.slice(1)}`
        name.classList.add('stock-name')
        const sh = document.createElement('p')
        sh.classList.add('stock-title')
        sh.innerText = title.trim()
        first_col.appendChild(name)
        first_col.appendChild(sh)

        const sec_col = document.createElement('div')
        sec_col.classList.add('right')
        const value = document.createElement('p')
        value.classList.add('stock-value')
        value.innerHTML = changeValue
        const dir = document.createElement('i')
        dir.classList.add('fa-solid')
        if(changeDirection === 'down'){
            dir.classList.add('fa-caret-down')
            sec_col.classList.add('down')
        }else{
            sec_col.classList.add('up')
            dir.classList.add('fa-caret-up')
        }
        sec_col.appendChild(value)
        sec_col.appendChild(dir)
        
        line.appendChild(first_col)
        line.appendChild(sec_col)
        // location.appendChild(line)
        document.querySelector(`.${loc}`).appendChild(line)
    })
}
const fLoad_losers = async() => {
    try {
        const response = await fetch(LINK_TO_DATA__losers);
        return await response.json()
    } catch (error) {
        return error.message
    }
}
const fEdit_losers = (data) => {
    // console.log(data)
    const location = document.querySelector('.card-content-losers')
    const dataEdited = data
    // fShow_GL(location, dataEdited)
}

const fShow_GL = (parent, data) => {
    parent.innerHTML = data.toString()
}

const toggle_table = document.querySelector('.type-table-toggle')
const table_crypto = document.querySelector('.array-content')
const grid_crypto = document.querySelector('.grid_crypto')
toggle_table.addEventListener('click', () => {
    console.log(toggle_table.classList);
    if(toggle_table.querySelector('i').classList.contains('fa-list')){
        toggle_table.querySelector('i').classList.replace('fa-list', 'fa-table-cells-large')
        table_crypto.classList.remove('hidden')
        grid_crypto.classList.add('hidden')
    }else{
        table_crypto.classList.add('hidden')
        grid_crypto.classList.remove('hidden')
        toggle_table.querySelector('i').classList.replace('fa-table-cells-large', 'fa-list')
    }
})

fLoad_main()
    .then(r => {
        const data = (typeof r === 'object') ? r : "error"
        fEdit_main(data)
    })

fLoad_trends()
    .then(r => {
        const data = (typeof r === 'object') ? r : "error"
        fEdit_Trend(data)
    })

fLoad_trends_user()
    .then(r => {
        const data = (typeof r === 'object') ? r : "error"
        fEdit_Trend_user(data)
    })

fLoad_gainers()
    .then(r => {
        const data = (typeof r === 'object') ? r : "error"
        fEdit_GL(data, "card-content-gainers")
    })
    
fLoad_losers()
    .then(r => {
        const data = (typeof r === 'object') ? r : "error"
        // fEdit_losers(data)
        fEdit_GL(data, "card-content-losers")
    })