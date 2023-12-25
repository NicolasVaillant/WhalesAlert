window.onload = function () {
    fLoad_main()
        .then(r => {
            const data = (typeof r === 'object') ? r : "error reading data main"
            console.log(data)
        })
    
    fLoad_gainers()
        .then(r => {
            const data = (typeof r === 'object') ? r : "error reading data gainers"
            console.log(data)
        })
        
    fLoad_losers()
        .then(r => {
            const data = (typeof r === 'object') ? r : "error reading data losers"
            console.log(data)
        })
}

const fLoad_main = async() => {
    try {
        const response = await fetch(LINK_TO_DATA__main);
        return await response.json()
    } catch (error) {
        return error.message
    }
}
const fLoad_gainers = async() => {
    try {
        const response = await fetch(LINK_TO_DATA__gainers);
        return await response.json()
    } catch (error) {
        return error.message
    }
}
const fLoad_losers = async() => {
    try {
        const response = await fetch(LINK_TO_DATA__losers);
        return await response.json()
    } catch (error) {
        return error.message
    }
}