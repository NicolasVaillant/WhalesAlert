const LINK_TO_DATA__main = "resources/data_scrap/main.json"
const LINK_TO_DATA__gainers = "resources/data_scrap/gainers.json"
const LINK_TO_DATA__losers = "resources/data_scrap/losers.json"
const LINK_TO_DATA__trends = "resources/data_scrap/trends.json"
const LINK_TO_DATA__trends_user = "resources/php/data/trends_user.json"
const LINK_TO_DATA__coin = "resources/data_coins/__COIN__.json"
const LINK_TO_DATA__tx = "resources/data_tx/tx___COIN__.json"
const LINK_TO_DATA__Files = "resources/php/data/getFiles_coin.json"

const settings = {
    ERROR:{
        'error-loading-data-text':'No data loaded'
    },
    HAMBURGER:{
        'menu-2':'Force refresh',
        'seperator-default':"Tools",
        'seperator-links':"Links"
    },
    GENERAL_text:{
        'intro-banner': 'Get to know us and stay informed by subscribing to the following links.',
        'backToTop-Text': 'Back to Top'
    },
    HOMEPAGE_text:{
        'home-h2-transactions': 'Latest transactions',
        'top-trend-user': 'Top user trends',
        'latest-top': 'Top transactions',
        'modal-text':'Open Crypto'
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
        'refresh-date-label':'Last refresh',
        'info-crypto-text': 'Description',
        'more-crypto-redirect-text':'Discover other cryptocurrencies'
    }
}

const variables = {
    refreshRate: ["30s", "1m", "10m"],
    arrayCryptoLabel: ["Amount", "Value", "Supply (%)", "Link"],
    version: "1.0.0"
}

const label__darkMode = 'dark-mode-WhalesAlert'