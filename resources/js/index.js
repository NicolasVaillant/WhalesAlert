window.onload = function () {
    loadResult()
        .then(r => {
            const data = (typeof r === 'object') ? r : "error reading data"
            console.log(data)
        })
}

const loadResult = async() => {
    try {
        const response = await fetch(LINK_TO_DATA);
        return await response.json()
    } catch (error) {
        return error.message
    }
}