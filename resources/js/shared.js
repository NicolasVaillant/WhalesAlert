const getIP = "https://api.ipify.org?format=json"
const getVersion = "https://whales-alert.fr/version_upd.php?ip=__IP__"
const toggle_hamburger = document.querySelector('.info-more')
const aside = document.querySelector('.content-displayed')
const l_col = document.querySelector('.col-more-info')
const r_col = document.querySelector('.col-content')
const backToTop = document.querySelector('.backToTop')
const sb = document.querySelector('.search-bar')
const wrapper_sb = document.querySelector('.wrapper-sub-header-sb')
const hb_container = document.querySelector('.hb-container')
const hamburger_menu = document.querySelector('.hamburger-menu')
const tooltip_content = document.querySelector('.tooltip-content')
const darkM = document.querySelector("#darkMode-input")
const LS = document.querySelector("#toggle-ls")
const tog_dm_icon = document.querySelectorAll(".tog_dm_icon")
const li_foldable = document.querySelector('.collapsible .collapsible-header')
const i_foldable = document.querySelector('.collapsible .foldable')
let toggle_icon = false
let exact_type = window.location.pathname.split("/").at(-1).split('.')[0]
exact_type.length === 0 ? exact_type = 'index' : exact_type;
const closer_banner = document.querySelector('.close-banner')
let refreshRateUserSelect = 'default'

// ===================
// Refresh State
// ===================
const refreshForce = document.querySelector('.refreshForce');
if(refreshForce !== null){
    const refreshForce_icon = refreshForce.querySelector('i');
    if(refreshForce_icon !== null){
        refreshForce.addEventListener('click', () => {
            if(!refreshForce_icon.classList.contains('spin')){
                refreshForce_icon.classList.add('spin')
                setTimeout(() => {
                    refreshForce_icon.classList.remove('spin')
                }, 900)
        
                if ($.fn.dataTable.isDataTable('#table_crypto')){
                    table = $('#table_crypto').DataTable();
                } else {
                    table = $('#table_crypto').DataTable( {
                        ajax: 'data/arrays.txt'
                    });
                }
                // table.clear().draw()
                callFunctions()
            }
        })
    }
}
// ===================

closer_banner.addEventListener('click', () => {
    hide(closer_banner.closest('.new'))
})

const changeIconButton = (e) => {
    if(toggle_icon){
        toggle_icon = false
        e.querySelector('i').classList.replace('fa-down-left-and-up-right-to-center', 'fa-up-right-and-down-left-from-center')
    } else{
        toggle_icon = true
        e.querySelector('i').classList.replace('fa-up-right-and-down-left-from-center','fa-down-left-and-up-right-to-center')
    }
}

function setToast(type, text, timer){
    let options_toast, toast_text, showButton, debug_text
    if(timer !== 0){
        options_toast = {
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            timer: timer,
            timerProgressBar: true,
            showCloseButton: true,
            didOpen: (toast) => {
                toast.addEventListener('mouseenter', Swal.stopTimer)
                toast.addEventListener('mouseleave', Swal.resumeTimer)
            }
        }
    }else{
        options_toast = {
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            showCloseButton: false,
        }
    }
    if (type !== "error") {
        showButton = false
        toast_text = text
    } else {
        showButton = false //TBM & TBD
        toast_text = `Error when copying value`
    }
    const Toast = Swal.mixin(options_toast)
    Toast.fire({
        icon: type,
        title: toast_text,
        showConfirmButton: showButton,
        confirmButtonText: 'Copy error'
    })
}

const expandView = (e) => {
    l_col.classList.toggle('hidden')
    checkGridPage()
    changeIconButton(e, )
}

if(variables.version > 1){
    const cleanLSConfirmButton = document.querySelector('.cleanLSConfirmButton')
    const cleanLSCancelButton = document.querySelector('.cleanLSCancelButton')
    if(cleanLSCancelButton !== null){
        cleanLSCancelButton.addEventListener('click', (e) => {
            LS.checked = false
            LS.closest('label').classList.remove('active')
            hide(tooltip_content.querySelector('span'))
        })
    }
    if(cleanLSConfirmButton !== null){
        cleanLSConfirmButton.addEventListener('click', (e) => {
            const checkbox_fav_crypto = document.querySelector('#fav-crypto');
            const toggle_fav = document.querySelector('.toggle_fav')
            const btn = e.target
            const status = btn.getAttribute('btn-clean')
            if(status === 'true'){
                LS.checked = false
                btn.innerText = 'Confirm'
                LS.closest('label').classList.remove('active')
                hide(tooltip_content.querySelector('span'))
                btn.setAttribute('btn-clean', 'false')
            } else {
                if(checkbox_fav_crypto){
                    checkbox_fav_crypto.checked = false
                    toggle_fav.classList.replace('fa-solid', 'fa-regular')
                }
                localStorage.removeItem(label__favorite_elements)
                btn.innerText = 'Done!'
                btn.setAttribute('btn-clean', 'true')
            }
        })
    }
    const ttc = document.querySelector('.tooltip-content')
    if(ttc !== null){ttc.classList.remove('hidden')}
    LS.addEventListener('change', (e) => {
        const stored_fav = JSON.parse(localStorage.getItem(label__favorite_elements))
        if(e.target.checked){
            if(stored_fav === null){
                const status = cleanLSConfirmButton.getAttribute('btn-clean')
                cleanLSConfirmButton.innerText = 'Already empty'
                cleanLSConfirmButton.setAttribute('btn-clean', 'true')
            } else {
                cleanLSConfirmButton.innerText = 'Confirm'
                cleanLSConfirmButton.setAttribute('btn-clean', 'false')
            }
            LS.closest('label').classList.add('active')
            tooltip_content.querySelector('span').classList.remove('hidden')
        }else{
            LS.closest('label').classList.remove('active')
            hide(tooltip_content.querySelector('span'))
        }
    })
}

const fLoadIP = async() => {
    try {
        const response = await fetch(getIP);
        return await response.json();
    } catch (error) {
        console.log(error.message);
    }
}

const fLoadVersionFromServer = async(r) => {
    try {
        const response = await fetch(
            getVersion.replaceAll(
                '__IP__', r
            )
        );
        return await response.json();
    } catch (error) {
        console.log(error.message);
    }
}

backToTop.addEventListener('click', () => {
    window.scrollTo(0, 0)
})

darkM.addEventListener('change', (e) => {
    /**
     * Function: /
     * Description: Modification of dark mode
     * If button darkM is checked we add class 'toggle_dark_mode' to document.documentElement
     * Then, we locally store state to manage cross page
     * return: none
     * */
    if(e.target.checked){
        //Dark Mode
        document.documentElement.classList.add('toggle_dark_mode');
        sessionStorage.setItem(label__darkMode, 'true')
    }else{
        //Light Mode
        document.documentElement.classList.remove('toggle_dark_mode');
        sessionStorage.setItem(label__darkMode, 'false')
    }
    //rotation of dark mode icon
    tog_dm_icon.forEach(e => {
        e.classList.toggle('rotate180')
    })
})
const ss_dm = sessionStorage.getItem(label__darkMode)
if(ss_dm === 'true' || settings.force_darkMode){
    document.documentElement.classList.add('toggle_dark_mode')
    darkM.checked = true
}

const copyrightDate = () => {
    const element = document.querySelector('.copyright-date')
    const date = new Date().getFullYear()
    element.innerText = `© ${date}`
}

window.onscroll = function () {
    if(exact_type == "app")
        modal.style.display = 'none';
    
    if(window.scrollY > 200){
        backToTop.classList.remove('hidden')
    } else{
        hide(backToTop)
    }
    hide(hb_container)
}
window.onload = function () {
    if(exact_type == "app"){
        const size = window.getComputedStyle(hamburger_menu).width
        i_foldable.parentElement.style.width = size
        const size_sb = window.getComputedStyle(sb).height
        if(size_sb === "auto"){
            document.querySelector('.info-more').style.width = size
        } else {
            document.querySelector('.info-more').style.width = size_sb
        }

        if(variables.version > 1){
            wrapper_sb.classList.remove('hidden')
            setTimeRefresh()
        }        
    } else if(exact_type == "crypto"){
        setTimeRefresh()
    }

    checkGridPage()

    copyrightDate()
    setTextFromParameters()
    // storeDataUsers()

    if(exact_type == "privacy")
        setSummary()

    fLoadIP().then(r => {
        fLoadVersionFromServer(r.ip);
    })
}

const dateFct = (type) => {
    const date = new Date()
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    const day = String(date.getDate()).padStart(2, "0");
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const year = date.getFullYear().toString().slice(-2);
    const day_in_week = date.toLocaleString('fr-FR', { weekday: 'long' })
    if(type === "full"){
        return {
            'full': `${day}/${month}/${year}`,
            'date_day': `${day_in_week} ${day}`,
            'day': day,
            'month': month,
            'year': year,
            'day_in_week': day_in_week,
            'hour': `${hours}:${minutes}`
        }
    } else {
        return `${day}/${month}/${year}`
    }
}

const setTimeRefresh = () => {
    document.querySelector('.seperator-refresh').innerText = `Last refresh at ${dateFct("full").hour}`
}

const storeDataUsers = () => {
    console.log('storage');
}

const checkGridPage = () => {
    if(l_col.classList.contains('hidden')){
        r_col.classList.add('span2')
        let element = document.querySelector('th');
        if(element){
            element.click();
            element.click();
        }
    } else {
        r_col.classList.remove('span2')
    }
}

const fLoad_cryptoIMG = async(input) => {
    try {
        const response = await fetch(`resources/logos/${input.toLowerCase().replace(/ /g, '_')}.png`);
        return await response.blob();
    } catch (error) {
        return error.message
    }
}

const setSummary = () => {
    const location = document.querySelector('.summary')
    const paragraph = document.querySelectorAll('.privacy-content .text-paragraph')
    paragraph.forEach(e => {
        const container = document.createElement('div')
        container.classList.add('container')

        const h2 = e.querySelectorAll('h2')
        const h3 = e.querySelectorAll('h3')

        h2.forEach(a => {
            a.id = a.textContent.toLowerCase().replaceAll(' ', '_')
            const clone = a.cloneNode(true)
            const h4 = document.createElement('a')
            h4.classList.add('h4')
            h4.href = `#${a.textContent.toLowerCase().replaceAll(' ', '_')}`
            h4.innerText = clone.textContent
            h4.onclick = function(e){
                document.querySelectorAll('.summary .h4').forEach(u => {u.classList.remove('clicked')})
                document.querySelectorAll('.summary .h5').forEach(u => {u.classList.remove('clicked')})
                e.target.classList.add('clicked')
            }
            container.appendChild(h4)
        })
        h3.forEach(a => {
            a.id = a.textContent.toLowerCase().replaceAll(' ', '_')
            const clone = a.cloneNode(true)
            h5 = document.createElement('a')
            h5.classList.add('h5')
            h5.href = `#${a.textContent.toLowerCase().replaceAll(' ', '_')}`
            h5.innerText = clone.textContent
            h5.onclick = function(e){
                document.querySelectorAll('.summary .h4').forEach(u => {u.classList.remove('clicked')})
                document.querySelectorAll('.summary .h5').forEach(u => {u.classList.remove('clicked')})
                e.target.classList.add('clicked')
            }
            container.appendChild(h5)
        })


        location.appendChild(container)
    })
}

const setTextFromParameters = () => {
    Object.entries(settings).forEach(([topKey, topValue]) => {
    const keys = Object.keys(topValue);
    keys.forEach(key => {
        const value = topValue[key];
        const elements = document.querySelectorAll(`.${key}`);
        elements.forEach(element => {
        element.innerHTML = value;
        })
    })
    })
}

toggle_hamburger.addEventListener('click', () => {
    if(hb_container.classList.contains('hidden')){
        hb_container.classList.remove('hidden')
        if(variables.version > 1){
            document.addEventListener('click', function(event) {
                if (!hamburger_menu.contains(event.target)) {
                    hide(hb_container)
                }
            });
        }
    }else{
        hide(hb_container)
    }
})

let currentIndex = 0;
const refreshRate = document.querySelector('.refreshRate');
refreshRate.addEventListener('click', () => {
//   const duration = variables.refreshRate[currentIndex];
//   refreshRate.querySelector('text').innerHTML = duration
//   refreshRateUserSelect = duration
//   currentIndex = (currentIndex + 1) % variables.refreshRate.length;
});

const contextMenuCreation = (display, text, x, y, url = false) => {
    const modal = document.getElementById('modal');
    const actionButton = document.getElementById('open_crypto_from_table');
    const text_modal = document.querySelector('.text_modal');
    modal.style.top = y + 'px';
    modal.style.left = x + 'px';
    modal.style.display = 'flex';
    actionButton.innerText = (url) ? `Open URL` : `Open ${display}`
    actionButton.addEventListener('click', function() {
        if(url){
            window.open(text, "_self")
        }else{
            window.open(`crypto.html?q=${text}`, "_self")
        }
        modal.style.display = 'none';
    });
}

if(exact_type === 'crypto' || exact_type === 'app'){
    const close_btn = document.querySelector('.close-btn');
    close_btn.addEventListener('click', function() {
        modal.style.display = 'none';
        $('#table_crypto tbody tr').removeClass('selected');
        $('#table_crypto_unique tbody tr').removeClass('selected');
    });
}

function changeImageTable(crypto, container){
    container.querySelectorAll('img').forEach(async a => {
        //Avoiding unnecessary calls
        if(a.dataset.type !== 'default') return
        let img_url
        const filteredCrypto = crypto.filter(crypto => crypto.Name.toLowerCase() === a.dataset.name.toLowerCase());
        const uniqueCrypto = filteredCrypto.find(crypto => crypto.Name.toLowerCase() === a.dataset.name.toLowerCase());
        if(uniqueCrypto !== undefined){
            await fLoad_cryptoIMG(uniqueCrypto.Name).then(r => {
                if(r !== undefined && r.type == 'image/png'){
                    img_url = `resources/logos/${uniqueCrypto.Name.toLowerCase().replace(/ /g, '_')}.png`
                } else{
                    img_url = null
                }
            })
            if(img_url !== null){a.src = img_url}
            a.dataset.type = 'crypto'
        }
    })
}

const copy2Clipboard = (value, name, type) => {
    navigator.clipboard.writeText(value).then(
        () => {
            setToast('success', `${name} ${type} copied successfully`, 5000)
        },
        () => {
            setToast('error', "", 5000)
        }
    )
}

const openPage = (value) => {
    let res = null
    if(value.includes(' ')){
        res = value.replace(/ /g, '_').toLowerCase()
    } else {
        res = value.toLowerCase()
    }
    window.open(`crypto.html?q=${res}`, "_self")
}

const hide = (element, value = false) => {
    if(value){
        element.classList.remove('hidden')
    } else {
        element.classList.add('hidden')
    }
}