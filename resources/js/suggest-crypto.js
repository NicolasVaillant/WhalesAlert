const query = decodeURIComponent(window.location.search.split("?q=")[1])
const form = document.querySelector('.suggest-form')
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
    
    fetch('submit_form.php', {
        method: 'POST',
        body: new FormData(form)
    }).then(response => {
        if (response.ok) {
            return response.text();
        }
        throw new Error('Network response was not ok.');
    }).then(data => {
        console.log(data);
    }).catch(error => {
        console.error('Error:', error);
        console.log("kdkd");
    });
});

const no_data_btn_img = document.querySelector('.btn-sc-input-img')
const no_data_btn_url = document.querySelector('.btn-sc-input-url')

const noData = (element) => {
    // console.log(element);
}

no_data_btn_img.addEventListener('click', noData(this))
no_data_btn_url.addEventListener('click', noData(this))


// resources/php/data/getFiles_coin.json