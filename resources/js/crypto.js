const query = decodeURIComponent(window.location.search.split("?q=")[1])
const name_c = document.querySelector('.name-crypto');
name_c.innerHTML = `${query.charAt(0).toUpperCase() + query.slice(1)}`