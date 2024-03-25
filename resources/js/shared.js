const getIP = "https://api.ipify.org?format=json"
const getVersion = "https://whales-alert.fr/version_upd.php?ip=__IP__"
const toggle_hamburger = document.querySelector('.info-more')
const aside = document.querySelector('.content-displayed')
const backToTop = document.querySelector('.backToTop')
const hb_container = document.querySelector('.hb-container')
const darkM = document.querySelector("#darkMode-input")
const tog_dm_icon = document.querySelectorAll(".tog_dm_icon")
let exact_type = window.location.pathname.split("/").at(-1).split('.')[0]
exact_type.length === 0 ? exact_type = 'index' : exact_type;
let refreshRateUserSelect = 'default'
const closer_banner = document.querySelector('.close-banner')
closer_banner.addEventListener('click', () => {
    closer_banner.closest('.new').classList.add('hidden')
})

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
    if(exact_type == "index")
        modal.style.display = 'none';
    
    if(window.scrollY > 200){
        backToTop.classList.remove('hidden')
    } else{
        backToTop.classList.add('hidden')
    }
    hb_container.classList.add('hidden')
}
window.onload = function () {
    copyrightDate()
    setTextFromParameters()
    // storeDataUsers()

    if(exact_type == "privacy")
        setSummary()

    fLoadIP().then(r => {
        fLoadVersionFromServer(r.ip);
    })
}

const storeDataUsers = () => {
    console.log('storage');
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
        showButton = true
        toast_text = `No URL to copy`
    }
    const Toast = Swal.mixin(options_toast)
    Toast.fire({
        icon: type,
        title: toast_text,
        showConfirmButton: showButton,
        confirmButtonText: 'Copy error'
    })
    // .then((result) => {
    //     if (result.isConfirmed) {
    //         navigator.clipboard.writeText(debug_text).then(
    //             () => {
    //                 setToast('success',
    //                     translation[languageSelect].content_page.toast.gToastSuccess.replace(
    //                         '__RESULT__',
    //                         'Error'
    //                     ),
    //                     5000)
    //             },
    //             () => {
    //                 setToast('error',translation[languageSelect].content_page.toast.gToastError,  5000)
    //             }
    //         )
    //     }
    // })
}

toggle_hamburger.addEventListener('click', () => {
    if(hb_container.classList.contains('hidden')){
        hb_container.classList.remove('hidden')
    }else{
        hb_container.classList.add('hidden')
    }
})

let currentIndex = 0;
const refreshRate = document.querySelector('.refreshRate');
refreshRate.addEventListener('click', () => {
  const duration = variables.refreshRate[currentIndex];
  refreshRate.querySelector('text').innerHTML = duration
  refreshRateUserSelect = duration
  currentIndex = (currentIndex + 1) % variables.refreshRate.length;
});

const contextMenuCreation = (text, x, y, url = false) => {
    const modal = document.getElementById('modal');
    const actionButton = document.getElementById('open_crypto_from_table');
    const text_modal = document.querySelector('.text_modal');
    modal.style.top = y + 'px';
    modal.style.left = x + 'px';
    modal.style.display = 'flex';
    actionButton.innerText = (url) ? `Open URL` : `Open ${text}`
    actionButton.addEventListener('click', function() {
        if(url){
            window.open(text, "_self")
        }else{
            window.open(`crypto.html?q=${text}`, "_self")
        }
        modal.style.display = 'none';
    });
}
const close_btn = document.querySelector('.close-btn');
close_btn.addEventListener('click', function() {
    modal.style.display = 'none';
    $('#table_crypto tbody tr').removeClass('selected');
    $('#table_crypto_unique tbody tr').removeClass('selected');
});
