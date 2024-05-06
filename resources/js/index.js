const gain_lose_content = document.querySelector('.gain-lose-content')
const wp_search_bar_result = document.querySelector('.wp-search-bar-result')
const wp_search_bar_result_ex = document.querySelector('.extend-suggestion')
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
        element.classList.add('btn-main', 'card-sh')
        text.innerHTML = e.Name
        element.href = `crypto.html?q=${e.Name}`
        value.innerHTML = (i+1).toString()
        element.appendChild(value)
        element.appendChild(text)
        location.appendChild(element)
    })

    let result_draw_cb = []
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
            "targets": "_all",
            "defaultContent": "-",
        }],
        order: [[0, 'asc']],
        scrollX: "300px",
        "searching": true,
        "ordering": true,
        "autoWidth": true,
        "responsive": true,
        pagingType: 'simple',
        drawCallback: function (settings) {
            var api = this.api();
            const result = api.rows({ page: 'current' }).data()
            for (let i = 0; i < 5; i++) {
                result_draw_cb.push(result[i])   
            }
            displayResultSB(result_draw_cb)
        },
        initComplete: function (settings) {
            const dock = document.querySelector('.dataTables_paginate')
            // dock.classList.add('pin-dock')
            const element = document.createElement('span')
            const element_icon = document.createElement('i')
            element.classList.add('element_icon')
            element_icon.classList.add('fa-solid', 'fa-thumbtack')
            element.appendChild(element_icon)
            element.onclick = function(){dockedDock(dock, element_icon)}
            // dock.appendChild(element)
        }
    });

    $('#table_crypto tbody').on('click', 'tr', function (e) {
        const crypto = $(this)[0].querySelectorAll('td')[1].innerText
        const cryptoDef = crypto.includes(' ') ? crypto.replace(/ /g, '_').toLowerCase() : crypto.toLowerCase()
        
        if ($(this).hasClass('selected')) {
            $(this).removeClass('selected');
            modal.style.display = 'none';
        } else {
            leaderboard_table.$('tr.selected').removeClass('selected');
            contextMenuCreation(cryptoDef, e.clientX, e.clientY)
            $(this).addClass('selected');
        }
    })
    if(variables.version > 1){
        const collapsible_body = document.querySelector('.collapsible-body')
        $('.search-bar-input').on('keyup change keypress', function () {
            setTimeout(() => {
                result_draw_cb.length = 0
                const child = wp_search_bar_result.querySelectorAll('.sb-result')
                child.forEach(e => {e.remove()})
                leaderboard_table.search(this.value).draw()
            }, 100)
        } );
        $('.search-bar-input').on('keydown', function () {
            const collapsible_hd = document.querySelector('.collapsible-header')
            const collapsible_bd = document.querySelector('.collapsible-body')
            if(window.getComputedStyle(collapsible_bd).display !== 'block'){
                setTimeout(() => {
                    collapsible_hd.click()
                }, 200)
            }
        } );
    }
}

const btn_clear_sb = document.querySelector('.clear-input-sb')
const input_sb = document.querySelectorAll('.search-bar-input')
btn_clear_sb.addEventListener('click', () => {
    input_sb.forEach(e => {
        e.value = ''
    })
})

const fallback_crypto = document.querySelector('.fallback-crypto')
const suggest_crypto = document.querySelector('.suggest-crypto')
const displayResultSB = (elements) => {
    const error_no_data = document.querySelector('.error_no_data')
    elements.forEach(e => {
        if(e !== undefined){
            const line = document.createElement('a')
            const line_text = document.createElement('p')
            const line_sb = document.createElement('p')
            const line_tt = document.createElement('p')
            line.classList.add('sb-result')
            line_text.innerText = e.Name
            line_sb.innerText = e.Symbol
            line_tt.innerText = `${e["1h"]} (1h)`
            line.appendChild(line_text)
            line.appendChild(line_sb)
            line.appendChild(line_tt)
            line.onclick = () => {
                window.open(`crypto.html?q=${e.Name}`, '_self')
            }
            wp_search_bar_result.appendChild(line)
        }
    })
    function isArrayOnlyNull(arr) {
        return arr.every(item => item === undefined);
    }

    if(isArrayOnlyNull(elements)){
        error_no_data.classList.remove('hidden')
        wp_search_bar_result_ex.classList.remove('hidden')
        if (window.matchMedia("(max-width: 550px)").matches) {
            fallback_crypto.innerText = `Go to ${input_sb[1].value} page`
            suggest_crypto.innerText = `Suggest ${input_sb[1].value}`
            fallback_crypto.href = `crypto.html?q=${input_sb[1].value}`
            suggest_crypto.href = `suggest-crypto.html?q=${input_sb[1].value}`
        }
    } else {
        error_no_data.classList.add('hidden')
        wp_search_bar_result_ex.classList.add('hidden')
    }
}

document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.collapsible');
    M.Collapsible.init(elems);
});


li_foldable.addEventListener('click', () => {
    i_foldable.classList.toggle('fold')
})

window.onresize = function () {
    const size = window.getComputedStyle(hamburger_menu).width
    i_foldable.parentElement.style.width = size
}

const dockedDock = (dock, span) => {
    dock.classList.toggle('pin-dock')
    span.classList.toggle('unpin')
}

const fEdit_Trend_user = (data) => {
    const user_trends = document.querySelector('.user-trends')
    const fav_crypto_load = JSON.parse(localStorage.getItem(label__favorite_elements))
    if(data !== 'error'){
        const init = document.querySelector('.user-trend-card[data-value="init"]')
        data.forEach((e, i) => {
            const element_card = init.cloneNode(true)
            element_card.setAttribute('data-value', false)
            element_card.setAttribute('data-urlPart', e.urlPart)
            element_card.href = `crypto.html?q=${e.urlPart}`
            element_card.querySelector('.user-trend-card-nb').innerText = (i+1).toString()
            element_card.querySelector('.user-trend-card-name').innerText = e.title
            element_card.querySelector('.user-trend-card-value').innerText = e.changeValue
            element_card.querySelector('.user-trend-card-value').classList.add(`${e.changeDirection}`)
            
            if(variables.version > 1){
                if(fav_crypto_load !== null && fav_crypto_load.data.length !== 0){
                    const array = fav_crypto_load.data
                    array.forEach(a => {
                        if(e.urlPart === a){
                            element_card.querySelector('.liked').classList.remove('hidden')
                        }
                    })
                }
            }

            user_trends.appendChild(element_card)
        });

        // setCardMore()
        const setCardMore = () => {
            const more = init.cloneNode(true)
            more.setAttribute('data-value', false)
            more.classList.add('see-stats')
            more.querySelector('.user-trend-card-nb').classList.add('hidden')
            more.querySelector('.user-trend-card-name').innerText = "test"
            user_trends.appendChild(more)
        }

        const dup = document.querySelector('.duplicated-user-trends')
        const user_trends_node = user_trends.cloneNode(true)
        user_trends_node.classList.replace('user-trends', 'user-trends-dup')
        dup.appendChild(user_trends_node)
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
        text.innerHTML = `${urlPart.charAt(0).toUpperCase() + urlPart.slice(1)}`
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
    if(data === "error"){
        if(loc.includes('losers')){
            gain_lose_content.querySelector('.col:last-child').classList.add('hidden')
        } else{
            gain_lose_content.querySelector('.col:first-child').classList.add('hidden')
        } 
        return
    }

    data.forEach((element, index) => {
        const {urlPart, title, changeDirection, changeValue} = element 
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
        const data = (typeof r === 'object' && r.length !== 0) ? r : "error"
        fEdit_GL(data, "card-content-losers")
    })