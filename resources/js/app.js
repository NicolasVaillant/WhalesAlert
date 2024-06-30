const gain_lose_content = document.querySelector('.gain-lose-content')
const tips = document.querySelector('.tips')
const btn_clear_sb = document.querySelector('.clear-input-sb')

// sb mobile
const wp_search_bar_result = document.querySelector('.wp-search-bar-result')
//sb desktop
const wp_search_bar_result_top = document.querySelector('.res-sb-top')

const wp_search_bar_result_ex = wp_search_bar_result.querySelector('.extend-suggestion')
const wp_search_bar_result_ex_top = wp_search_bar_result_top.querySelector('.extend-suggestion')
const fallback_crypto = document.querySelectorAll('.fallback-crypto')
const suggest_crypto = document.querySelectorAll('.suggest-crypto')

if(variables.version > 1){
    const toggle_hints = document.querySelector("#toggle-tips")
    const icon = toggle_hints.parentElement.querySelector('i')
    toggle_hints.addEventListener('change', (e) => {
        if(e.target.checked){
            hide(tips)
            icon.classList.replace('fa-toggle-off', 'fa-toggle-on')
        } else{
            hide(tips, true)
            icon.classList.replace('fa-toggle-on', 'fa-toggle-off')
        }
    })
    
    const closer_h = document.querySelector('.close-tips')
    closer_h.addEventListener('click', () => {
        hide(closer_h.closest('.tips'))
    })

    if(!settings.suggestionPage){
        suggest_crypto.forEach(e => {e.classList.add('hidden')})
    }
}

const loadMain = async () => {
    try {
        const response = await fetch(LINK_TO_DATA__main);
        const result = await response.json();
        const data = (typeof result === 'object') ? result : "error"
        fEdit_main(data)
        saveData(data)
    } catch (error) {
        fEdit_main("error")
        saveData("error")
    }
};

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

const loadTips = async () => {
    try {
        const response = await fetch(LINK_TO_DATA__hints);
        const data = await response.json();
        displayTips(data);
    } catch (error) {
        displayTips("error");
    }
};

const loadLosers = async () => {
    try {
        const response = await fetch(LINK_TO_DATA__losers);
        const result = await response.json();
        const data = (Array.isArray(result) && result.length !== 0) ? result : "error";
        fEdit_GL(data, "card-content-losers");
    } catch (error) {
        console.log(error)
        fEdit_GL("error", "card-content-losers");
    }
};

const loadGainers = async() => {
    try {
        const response = await fetch(LINK_TO_DATA__gainers);
        const result = await response.json();
        const data = (Array.isArray(result) && result.length !== 0) ? result : "error";
        fEdit_GL(data, "card-content-gainers")
    } catch (error) {
        console.log(error)
        fEdit_GL("error", "card-content-gainers");
    }
}


const fEdit_main = async (data) => {
    const cryptocurrencies = data.cryptocurrencies
    let name
    for (let i = 0; i < cryptocurrencies.length; i++) {
        const crypto = cryptocurrencies[i]
        if(crypto.Name.length > 10){
            name = crypto.Name.slice(0, 10) + "...";
        } else {
            name = crypto.Name
        }
        crypto.Name_mod = `<img class="img" data-name="${crypto.Name}"  data-type="default" src="resources/img/logo.png" alt="crypto_logo"> ${name} <span>${crypto.Symbol}</span> <button class="btn-main" onclick="openPage(this.parentElement.querySelector('img').getAttribute('data-name'))"><i class="fa-solid fa-arrow-up-right-from-square"></i></button>`
        crypto.Price_mod = `${crypto.Price} <button class="btn-main" data-type="price" onclick="copy2Clipboard(this.parentElement.innerText.trim(), this.closest('tr').querySelector('img').getAttribute('data-name'), this.getAttribute('data-type'))"><i class="fa-regular fa-copy"></i></button>`
        crypto.Volume_mod = `${crypto.Volume} <button class="btn-main" data-type="volume" onclick="copy2Clipboard(this.parentElement.innerText.trim(), this.closest('tr').querySelector('img').getAttribute('data-name'), this.getAttribute('data-type'))"><i class="fa-regular fa-copy"></i></button>`
    }

    const result = cryptocurrencies.filter(obj => obj.Rank === 1 || obj.Rank === 2 || obj.Rank === 3);

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
        data: cryptocurrencies,
        lengthMenu: [
            [10, 25, 50],
            [10, 25, 50],
        ],
        columns: [
            { data: 'Rank'},
            // { data: 'Name' },
            { data: 'Name_mod' },
            // { data: 'Symbol' },
            // { data: 'Price' },
            { data: 'Price_mod' },
            // { data: 'Volume' },
            { data: 'Volume_mod' },
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
            changeImageTable(cryptocurrencies, wp_search_bar_result_top)
            changeImageTable(cryptocurrencies, wp_search_bar_result)
            changeColorText(this[0].querySelectorAll('tbody td'))
        },
        initComplete: function (settings) {
            changeImageTable(cryptocurrencies, this[0].querySelector('tbody'))
            changeColorText(this[0].querySelectorAll('tbody td'))
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
        if (!$(e.target).is('button') && !$(e.target).is('i')) {
            // const crypto = $(this)[0].querySelectorAll('td')[1].querySelector('img').getAttribute('data-name')
            // const cryptoDef = crypto.includes(' ') ? crypto.replace(/ /g, '_').toLowerCase() : crypto.toLowerCase()
            if ($(this).hasClass('selected')) {
                $(this).removeClass('selected');
                // modal.style.display = 'none';
            } else {
                leaderboard_table.$('tr.selected').removeClass('selected');
                // contextMenuCreation(crypto, cryptoDef, e.clientX, e.clientY)
                $(this).addClass('selected');
            }
        } else{
            $(this).removeClass('selected');
            // modal.style.display = 'none';
        }
    })
    if(variables.version > 1){
        $('.search-bar-input').on('keyup change keypress', function () {
            setTimeout(() => {
                result_draw_cb.length = 0
                const child = wp_search_bar_result.querySelectorAll('.sb-result')
                const child_top = wp_search_bar_result_top.querySelectorAll('.sb-result')
                child.forEach(e => {e.remove()})
                child_top.forEach(e => {e.remove()})
                leaderboard_table.search(this.value).draw()
                if(window.matchMedia('(max-width: 550px)').matches){
                    changeImageTable(cryptocurrencies, wp_search_bar_result)
                } else {
                    changeImageTable(cryptocurrencies, wp_search_bar_result_top)
                }
                if(this.value.length !== 0){
                    btn_clear_sb.classList.remove('hidden')
                    this.classList.add('btn-on')
                } else {
                    btn_clear_sb.classList.add('hidden')
                    this.classList.remove('btn-on')
                }
                return
            }, 200)
        } );
        $('.search-bar-input').on('click', function () {
            const collapsible_hd = document.querySelector('.collapsible-header')
            const collapsible_bd = document.querySelector('.collapsible-body')
            if(window.getComputedStyle(collapsible_bd).display !== 'block'){
                setTimeout(() => {
                    collapsible_hd.click()
                }, 200)
            }
        } );
        $('#table_crypto_length').on('change', function (){
            changeImageTable(cryptocurrencies, $('#table_crypto').find('tbody')[0])
        })
        $('.row_table_def').on('click', function (){
            changeImageTable(cryptocurrencies, $('#table_crypto').find('tbody')[0])
        })
        $('#table_crypto_paginate').on('click', function (){
            changeImageTable(cryptocurrencies, $('#table_crypto').find('tbody')[0])
        })
    }
}

document.addEventListener('click' , (e) => {
    const collapsible_hd = document.querySelector('.collapsible-header')
    const collapsible_bd = document.querySelector('.collapsible-body')
    var isInsideWrapper = e.target.closest('.wrapper-sub-header-sb');
    if (!isInsideWrapper) {
        if(window.getComputedStyle(collapsible_bd).display == 'block'){
            setTimeout(() => {
                collapsible_hd.click()
            }, 200)
        }
    }
})

const input_sb = document.querySelectorAll('.search-bar-input')
btn_clear_sb.addEventListener('click', () => {
    input_sb.forEach(e => {
        e.value = ''
    })
})

const displayResultSB = (elements) => {
    const error_no_data = wp_search_bar_result.querySelector('.error_no_data')
    const error_no_data_top = wp_search_bar_result_top.querySelector('.error_no_data')
    
    elements.forEach(e => {
        if(e !== undefined){
            const line = document.createElement('a')
            const line_img = document.createElement('img')
            const line_text = document.createElement('p')
            const line_sb = document.createElement('p')
            const line_tt = document.createElement('p')
            line.classList.add('sb-result')
            line_img.src = "resources/img/logo.png"
            line_img.setAttribute('data-type', "default")
            line_img.setAttribute('data-name', e.Name)
            line_text.innerText = e.Name
            line_sb.innerText = e.Symbol
            line_tt.innerText = `${e["1h"]} (1h)`
            line.appendChild(line_img)
            line.appendChild(line_text)
            line.appendChild(line_sb)
            line.appendChild(line_tt)
            line.onclick = () => {
                window.open(`crypto.html?q=${e.Name}`, '_self')
            }
            const lineClone = line.cloneNode(true);
            lineClone.onclick = () => {
                window.open(`crypto.html?q=${e.Name}`, '_self')
            }

            wp_search_bar_result.appendChild(lineClone)
            wp_search_bar_result_top.appendChild(line)
        }
    })
    function isArrayOnlyNull(arr) {
        return arr.every(item => item === undefined);
    }

    if(isArrayOnlyNull(elements)){
        error_no_data.classList.remove('hidden')
        error_no_data_top.classList.remove('hidden')
        wp_search_bar_result_ex.classList.remove('hidden')
        wp_search_bar_result_ex_top.classList.remove('hidden')
        fallback_crypto.forEach((e, i) => {
            e.innerText = `Go to ${input_sb[i].value} page`
            e.href = `crypto.html?q=${input_sb[i].value}`
        })
        suggest_crypto.forEach((e, i) => {
            e.innerText = `Suggest ${input_sb[i].value}`
            e.href = `suggest-crypto.html?q=${input_sb[i].value}`
        })
    } else {
        hide(error_no_data)
        hide(error_no_data_top)
        hide(wp_search_bar_result_ex)
        hide(wp_search_bar_result_ex_top)
    }


    const child = wp_search_bar_result.querySelectorAll('.sb-result')
    const child_top = wp_search_bar_result_top.querySelectorAll('.sb-result')

    if(child.length > 5)
        child.forEach((e, i) => {
            if(i >= 5){e.remove()}
        })

    if(child_top.length > 5)
        child_top.forEach((e, i) => {
            if(i >= 5){e.remove()}
        })

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
    const createCard = (element, c, i, last = false) => {
        const dv = element.getAttribute('data-value')
        const element_card = element.cloneNode(true)
        if(dv == 'sep'){
            element_card.setAttribute('data-value', 'separator')
            user_trends.appendChild(element_card)
            return
        }
        element_card.setAttribute('data-value', false)
        element_card.setAttribute('data-urlPart', ((last)) ? c : c.urlPart)
        element_card.setAttribute('data-colorized', ((last)) ? true : false)
        element_card.href = `crypto.html?q=${((last)) ? c : c.urlPart}`
        element_card.querySelector('.user-trend-card-nb').innerText = (i+1).toString()
        element_card.querySelector('.user-trend-card-name').innerText = ((last)) ? c : c.title
        if(last){
            element_card.querySelector('.user-trend-card-value').innerText = 'Saved by user'
        } else {
            element_card.querySelector('.user-trend-card-value').innerText = c.changeValue
            element_card.querySelector('.user-trend-card-value').classList.add(`${c.changeDirection}`)
        }
        if(variables.version > 1){
            if(last){element_card.querySelector('.liked').classList.remove('hidden')}
            if(fav_crypto_load !== null && fav_crypto_load.data.length !== 0){
                const array = fav_crypto_load.data
                array.forEach(a => {
                    if(c.urlPart === a){
                        element_card.querySelector('.liked').classList.remove('hidden')
                    }
                })
            }
        }
        user_trends.appendChild(element_card)
    }

    if(data !== 'error'){
        const user_trends = document.querySelector('.user-trends')
        const init = document.querySelector('.user-trend-card[data-value="init"]')
        data.forEach((e, i) => {
            // createCard(init, e, i) //disable for now
        });
        
        const fAdd_Favorite_user = () => {
            const fav_crypto_load = JSON.parse(localStorage.getItem(label__favorite_elements))
            if(fav_crypto_load !== null && fav_crypto_load.data.length !== 0){
                const fav = fav_crypto_load.data
                const user_trends_dup = document.querySelector('.user-trends-dup')
                let user_trends_arr = []
                const childElements = Array.from(user_trends.children)
                childElements.forEach(ut => {
                    const dataUrlPart = ut.getAttribute('data-urlPart');
                    if (dataUrlPart) {
                        user_trends_arr.push(dataUrlPart);
                    }
                })
                const unique_in_fav = fav.filter(value => !user_trends_arr.includes(value));
                return unique_in_fav
            } else return []
        }

        const value_unique = fAdd_Favorite_user()
        if(value_unique.length !== 0){
            const separator = document.querySelector('div[data-value="sep"]')
            // createCard(separator)
            value_unique.forEach((e, i) => {
                createCard(init, e, i, true)
            })
        } else {
            const dup = document.querySelector('.duplicated-user-trends')
            hide(dup)
            hide(user_trends)
            hide(user_trends.parentElement.querySelector('h3'))
        }

        // setCardMore()
        const setCardMore = () => {
            const more = init.cloneNode(true)
            more.setAttribute('data-value', false)
            more.classList.add('see-stats')
            hide(more.querySelector('.user-trend-card-nb'))
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
    data.forEach(e=> {
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
    return true
}

const fEdit_GL = (data, loc) => {

    const parent = document.querySelector(`.${loc}`)
    const test_child = parent.querySelector('a')

    if(test_child !== null){
        while (parent.firstChild) {
            parent.removeChild(parent.firstChild);
        }
    }
    if(data === "error"){
        if(loc.includes('losers')){
            hide(gain_lose_content.querySelector('.col:last-child'))
        } else{
            hide(gain_lose_content.querySelector('.col:first-child'))
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
        const img = document.createElement('img')
        img.src = "resources/img/logo.png"
        img.setAttribute('data-type', "default")
        img.setAttribute('data-name', urlPart)
        name.innerText = `${index+1}. ${urlPart.charAt(0).toUpperCase() + urlPart.slice(1)}`
        name.classList.add('stock-name')
        const sh = document.createElement('p')
        sh.classList.add('stock-title')
        sh.innerText = title.trim()
        first_col.appendChild(img)
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
        parent.appendChild(line)
    })
    let storedData = sessionStorage.getItem(label__stored);
    if (storedData !== null) {
        changeImageTable(JSON.parse(storedData).data.cryptocurrencies, document.querySelector(`.${loc}`));
    }
}

const fEdit_losers = (data) => {
    // console.log(data)
    const location = document.querySelector('.card-content-losers')
    const dataEdited = data
    fShow_GL(location, dataEdited)
}

const fShow_GL = (parent, data) => {
    parent.innerHTML = data.toString()
}

const toggle_table = document.querySelector('.type-table-toggle')
const table_crypto = document.querySelector('.array-content')
const grid_crypto = document.querySelector('.grid_crypto')
toggle_table.addEventListener('click', () => {
    if(toggle_table.querySelector('i').classList.contains('fa-list')){
        toggle_table.querySelector('i').classList.replace('fa-list', 'fa-table-cells-large')
        table_crypto.classList.remove('hidden')
        hide(grid_crypto)
    }else{
        hide(table_crypto)
        grid_crypto.classList.remove('hidden')
        toggle_table.querySelector('i').classList.replace('fa-table-cells-large', 'fa-list')
    }
})

const displayTips = (data) => {
    const valuesArray = Object.values(data);
    const obj = valuesArray[Math.floor(Math.random() * valuesArray.length)];
    document.querySelector('.hints_title').innerText = obj.title
    document.querySelector('.hints_text').innerHTML = obj.text
}

const saveData = (data) => {
    sessionStorage.setItem(label__stored, JSON.stringify({
        status: 'success',
        data: data
    }));
}

fLoad_trends()
    .then(r => {
        const data = (typeof r === 'object') ? r : "error"
        if(data === "error"){
            document.querySelector('.error-loading-data-text').classList.remove('hidden')
        } else {
            const fct = fEdit_Trend(data);
            if(fct){
                hide(document.querySelector('.line-content-trend .shimmer'))
            }
        }
    })
    
fLoad_trends_user()
    .then(r => {
        const data = (typeof r === 'object') ? r : "error"
        fEdit_Trend_user(data)
    })


const callFunctions = () => {
    setTimeRefresh()
    loadTips()
    loadLosers()
    loadGainers()
}

loadMain()
callFunctions()
