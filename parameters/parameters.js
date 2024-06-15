const LINK_TO_DATA__main = "resources/data_scrap/main.json"
const LINK_TO_DATA__gainers = "resources/data_scrap/gainers.json"
const LINK_TO_DATA__losers = "resources/data_scrap/losers.json"
const LINK_TO_DATA__trends = "resources/data_scrap/trends.json"
const LINK_TO_DATA__trends_user = "resources/php/data/trends_user.json"
const LINK_TO_DATA__coin = "resources/data_coins/__COIN__.json"
const LINK_TO_DATA__tx = "resources/data_tx/tx___COIN__.json"
const LINK_TO_DATA__Files = "resources/php/data/getFiles_coin.json"
const LINK_TO_DATA__hints = "resources/php/data/tips.json"

const settings = {
    ERROR:{
        'error-loading-data-text':'No data loaded'
    },
    HAMBURGER:{
        'menu-2':'Force refresh (entire page)',
        'menu-3':'Mode',
        'menu-4':'Clean Localstorage',
        'menu-4-explanation':'We use LocalStorage of your browser to store information such as favorite cryptocurrencies. <b>By clearing this storage, you may lose some of your preferences.</b>',
        'menu-5':'Toggle tips',
        'seperator-default':"Tools",
        'seperator-links':"Links"
    },
    GENERAL_text:{
        'intro-banner': 'Get to know us and stay informed by subscribing to the following links.',
        'backToTop-Text': 'Back to Top',
        'next-tips': 'Next tip'
    },
    HOMEPAGE_text:{
        'home-h2-transactions': 'Live Crypto Prices',
        'top-trend-user': 'Favorite',
        'latest-top': 'Top transactions',
        'modal-text':'Open Crypto',
        'git-issue-text':'Open an issue',
        'git-suggestion-text':'Make a suggestion'
    },
    PRIVACY_PAGE_text:{
        'privacy-aside':'Summary'
    },
    CRYPTO_PAGE_text:{
        'description-array-crypto': 'The latest transactions appear on top.',
        'quote-USD-price-label':'Quote price',
        'market-cap-label':'Market cap',
        'market-cap-no-info':'No Market cap data',
        'volume-24h-label':'Volume (24h)',
        'circulating-supply-label':'Circulating supply',
        'circulating-supply-no-info':'No Circulating supply data',
        'max-supply-label':'Max supply',
        'max-supply-no-info':'No Max supply data',
        'refresh-date-label':'Last refresh',
        'info-crypto-text': 'Description',
        'more-crypto-redirect-text':'Discover other cryptocurrencies',
        'fav-crypto-label':'Set as favorite'
    },
    SUGGESTION_PAGE_text:{
        'text-explanation-suggestion': "Didn't find the cryptocurrency you were looking for? Fill out this form to tell us!<br><br>Try to fill out the form completely so that we can process your request as quickly as possible.",
        'no-data': 'No data'
    }
}

const variables = {
    refreshRate: ["30s", "1m", "10m"],
    arrayCryptoLabel: ["Amount", "Value", "Supply (%)", "Link"],
    version: 2,
    suggestionPage: false
}

const label__darkMode = 'dark-mode-WhalesAlert'
const label__favorite_elements = "fav-c"
const label__stored = "data"