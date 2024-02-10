let exact_type = window.location.pathname.split("/").at(-1).split('.')[0]
exact_type.length === 0 ? exact_type = 'index' : exact_type;

const copyrightDate = () => {
    const element = document.querySelector('.copyright-date')
    const date = new Date().getFullYear()
    element.innerText = `© ${date}`
}
window.onscroll = function () {
    if(exact_type === "index")
        modal.style.display = 'none';
}
window.onload = function () {
    copyrightDate()
    setTextFromParameters()
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