window.onload = function () {
    copyrightDate()

    fLoad_main()
        .then(r => {
            const data = (typeof r === 'object') ? r : "error reading data main"
            fEdit_main(data)
            fEdit_Trend(data)
        })
    
    fLoad_gainers()
        .then(r => {
            const data = (typeof r === 'object') ? r : "error reading data gainers"
            fEdit_GL(data, "card-content-gainers")
        })
        
    fLoad_losers()
        .then(r => {
            const data = (typeof r === 'object') ? r : "error reading data losers"
            // fEdit_losers(data)
            fEdit_GL(data, "card-content-losers")
        })
}

const copyrightDate = () => {
    const element = document.querySelector('.copyright-date')
    const date = new Date().getFullYear()
    element.innerText = `© ${date}`
}

const fLoad_main = async() => {
    try {
        const response = await fetch(LINK_TO_DATA__main);
        return await response.json()
    } catch (error) {
        return error.message
    }
}

const fEdit_main = (data) => {
    // console.log(data)
    const cryptocurrencies = data.cryptocurrencies

    const result = data.cryptocurrencies.filter(obj => obj.Rank === 1 || obj.Rank === 2 || obj.Rank === 3);

    // console.log(result);
    const location = document.querySelector('.col-left-sc')
    result.forEach(e => {
        const element = document.createElement('div')
        const text = document.createElement('p')
        element.classList.add('card-sh')
        text.innerHTML = e.Name
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
            // { data: 'name'},
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
        // "paging": pagingAllow,
        // "lengthChange": lengthChangeAllow,
        "searching": true,
        "ordering": true,
        // "info": pagingAllow,
        "autoWidth": false,
        "responsive": false,
        // "language": translation[languageSelect].dataTable,
        // "initComplete": function() {
        //     initComplete_leaderboard = true
        //     changeImageTable(player.players, this[0].querySelector('tbody'))
        // }
    });
}

const fEdit_Trend = (data) => {
    console.log(data)
    const location = document.querySelector('.container-overflow')
    data.cryptocurrencies.forEach(e => {
        const {Name} = e 
        const element = document.createElement('div')
        element.classList.add('trends-e')
        const status = document.createElement('div')
        const status_dir = document.createElement('i')
        status_dir.classList.add('fa-solid', 'fa-caret-up')
        // if(changeDirection === 'down'){
        //     dir.classList.add('fa-caret-down')
        //     sec_col.classList.add('down')
        // }else{
        //     sec_col.classList.add('up')
        //     dir.classList.add('fa-caret-up')
        // }
        const status_val = document.createElement('p')
        status.appendChild(status_dir)
        status.appendChild(status_val)
        const text = document.createElement('p')
        text.innerHTML = Name
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