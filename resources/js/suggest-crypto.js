const query = decodeURIComponent(window.location.search.split("?q=")[1])
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
