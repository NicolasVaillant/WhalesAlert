const query = decodeURIComponent(window.location.search.split("?q=")[1])
const form = document.querySelector('.suggest-form')
const post_form = document.querySelector('.result-post-form')
const post_form_result = document.querySelector('.result-post-form .result')
const input_name = document.querySelector('#sc-input-name')
const input_symbol = document.querySelector('#sc-input-symbol')
const input_url = document.querySelector('#sc-input-url')
const input_img = document.querySelector('#sc-input-img')
if(query !== undefined || query !== "undefined"){
    input_name.value = query
    input_symbol.value = query.slice(0, 3).toUpperCase()
    input_url.value = `https://${query}.com`
    input_img.value = `https://${query}.png`
}

form.addEventListener('submit', function(event) {
    event.preventDefault();
    const form_data = new FormData(form)
    fLoad_files()
        .then(r => {
            const data = (typeof r === 'object' && r.length !== 0) ? r : "error"
            data.files.forEach(element => {
                if(element.toLowercase() === form.querySelector('#sc-input-name').value.toLowercase()){
                    post_form.classList.remove('hidden')
                    post_form_result.innerText = 'Data'
                }
            });
        })
    
    fetch('submit_form.php', {
        method: 'POST',
        body: form_data
    }).then(response => {
        if (response.ok) {
            return response.text();
        }
        throw new Error('Network response was not ok.');
    }).then(data => {
        console.log(data);
        post_form.classList.remove('hidden')
        post_form_result.innerText = error
    }).catch(error => {
        console.error('Error:', error);
        post_form.classList.remove('hidden')
        post_form_result.innerText = error
    });
});

const no_data_btn_img = document.querySelector('.btn-sc-input-img')
const no_data_btn_url = document.querySelector('.btn-sc-input-url')

const noData = (element) => {
    console.log(element);
}

no_data_btn_img.onclick = function(){
    console.log(this);
}
no_data_btn_url.onclick = function(){
    console.log(this);
}

const fLoad_files = async() => {
    try {
        const response = await fetch(LINK_TO_DATA__Files);
        return await response.json()
    } catch (error) {
        return error.message
    }
}
