const dev_1 = 'NicolasVaillant'
const dev_2 = 'Charles-84'
const colors = ['#5e5eb775', '#5eb7ab9c', '#b75e92b5'];
const roadmap = {
    'dark-mode':{
        'title': 'Better Dark Mode',
        'status': 'wip',
        'cosmetic':'<i class="fa-solid fa-circle-half-stroke"></i>',
        'release':'2',
        'advancement': 0.5, 
        'assign': {
            'dev_1': true,
            'dev_2': false
        }
    },
    'crypto-suggestion':{
        'title': 'Cryptocurrencies suggestions',
        'cosmetic':'<i class="fa-solid fa-magnifying-glass-chart"></i>',
        'status': 'wip',
        'release':'2',
        'advancement': 1, 
        'assign': {
            'dev_1': true,
            'dev_2': false
        }
    },
    'widget':{
        'title': 'Widget currency conversion integration',
        'cosmetic':'<i class="fa-solid fa-square-poll-vertical"></i>',
        'status': 'wip',
        'release':'X',
        'advancement': 0.1, 
        'assign': {
            'dev_1': true,
            'dev_2': false
        }
    },
    'hint':{
        'title': 'Hint for users in website',
        'cosmetic':'<i class="fa-solid fa-lightbulb"></i>',
        'status': 'wip',
        'release':'X',
        'advancement': 0, 
        'assign': {
            'dev_1': true,
            'dev_2': false
        }
    },
    'logo':{
        'title': 'New Logo creation',
        'status': 'soon',
        'cosmetic':'<i class="fa-solid fa-dice-d6"></i>',
        'release':'X',
        'advancement': 0, 
        'assign': {
            'dev_1': true,
            'dev_2': true
        }
    },
    'bdd':{
        'title': 'Historical and graphical BDD',
        'status': 'wip',
        'cosmetic':'<i class="fa-solid fa-database"></i>',
        'release':'X',
        'advancement': 0.5, 
        'assign': {
            'dev_1': false,
            'dev_2': true
        }
    },
    'bdd_py':{
        'title': 'Rework BDD used in python files',
        'status': 'wip',
        'cosmetic':'<i class="fa-solid fa-database"></i>',
        'release':'X',
        'advancement': 0.5, 
        'assign': {
            'dev_1': false,
            'dev_2': true
        }
    },
    'bdd_coins':{
        'title': 'Rework management of database data_coins 2/2',
        'status': 'wip',
        'cosmetic':'<i class="fa-solid fa-database"></i>',
        'release':'X',
        'advancement': 0.5, 
        'assign': {
            'dev_1': false,
            'dev_2': true
        }
    },
    'a_sb':{
        'title': 'Advanced search bar website integration',
        'status': 'wip',
        'cosmetic':'<i class="fa-solid fa-magnifying-glass"></i>',
        'release':'2',
        'advancement': 0.75, 
        'assign': {
            'dev_1': true,
            'dev_2': false
        }
    },
    'whats_new':{
        'title': 'What’s new splash screen + banner at bottom',
        'status': 'soon',
        'cosmetic':'<i class="fa-solid fa-wand-magic-sparkles"></i>',
        'release':'X',
        'advancement': 0, 
        'assign': {
            'dev_1': true,
            'dev_2': false
        }
    },
    'icon_table':{
        'title': 'Add cryptocurrencies icons in table',
        'status': 'soon',
        'cosmetic':'<i class="fa-solid fa-icons"></i>',
        'release':'X',
        'advancement': 0, 
        'assign': {
            'dev_1': true,
            'dev_2': false
        }
    },
    'social':{
        'title': 'Social Links in crypto.html',
        'status': 'soon',
        'cosmetic':'<i class="fa-solid fa-bullhorn"></i>',
        'release':'X',
        'advancement': 0.1, 
        'assign': {
            'dev_1': true,
            'dev_2': false
        }
    },
    'whats_new_extended':{
        'title': "Put 'What's new' in hamburger menu",
        'status': 'soon',
        'cosmetic':'<i class="fa-solid fa-bullhorn"></i>',
        'release':'X',
        'advancement': 0, 
        'assign': {
            'dev_1': true,
            'dev_2': false
        }
    },
    'social_eng':{
        'title': 'Delete the names from the footer (advice to avoid social engineering)',
        'status': 'oneday',
        'cosmetic':'<i class="fa-solid fa-triangle-exclamation"></i>',
        'release':'X',
        'advancement': 0, 
        'assign': {
            'dev_1': true,
            'dev_2': true
        }
    },
    'twitter':{
        'title': 'Twitter ads',
        'status': 'wip',
        'cosmetic':'<i class="fa-solid fa-hashtag"></i>',
        'release':'X',
        'advancement': 0.5, 
        'assign': {
            'dev_1': false,
            'dev_2': true
        }
    },
    'suggestion':{
        'title': "Added a cryptocurrency suggestion page",
        'status': 'wip',
        'cosmetic':'<i class="fa-solid fa-coins"></i>',
        'release':'X',
        'advancement': 0.75, 
        'assign': {
            'dev_1': true,
            'dev_2': false
        }
    },
    'new_coins':{
        'title': "Add of new coins",
        'status': 'wip',
        'cosmetic':'<i class="fa-solid fa-coins"></i>',
        'release':'X',
        'advancement': 0.5, 
        'assign': {
            'dev_1': false,
            'dev_2': true
        }
    },
    'websocket':{
        'title': "Modifying websocket",
        'status': 'wip',
        'cosmetic':'<i class="fa-brands fa-docker"></i>',
        'release':'X',
        'advancement': 0.9, 
        'assign': {
            'dev_1': false,
            'dev_2': true
        }
    }
}

const setImages = () => {
    const elements = document.querySelectorAll('.rm-milestone[data-value="false"]')
    elements.forEach(e => {
        if(e.getAttribute('data-dev_1') == 'true'){
            e.querySelector('.dev_1').classList.remove('hidden')
        }

        if(e.getAttribute('data-dev_2') == 'true'){
            e.querySelector('.dev_2').classList.remove('hidden')
        }

        if(e.getAttribute('data-dev_1') == 'true' && e.getAttribute('data-dev_2') == 'true'){
            e.querySelector('.assign').classList.add('both')
        }

    })
}

const createCard = (item, i) => {
    const parent = document.querySelector(`.milestone-container .rm-${item.status} .container-cards`)
    const card = document.querySelector('.rm-milestone')
    const clone = card.cloneNode(true)
    let version = null
    clone.setAttribute('data-value', false)
    clone.querySelector('.text').innerText = item.title
    clone.querySelector('.cosmetic').innerHTML = item.cosmetic
    clone.querySelector('.progress-bar').style.width = `${(100*item.advancement)}%`
    if(item.advancement == 1){
        clone.querySelector('.progress-bar-check').classList.remove('hidden')
        clone.querySelector('.progress-bar').classList.add('full')
    }
    const release_container = clone.querySelector('.release')
    release_container.innerHTML = `v${item.release}.0.0`

    let colorIndex;
    if (item.release === 'X') {
        colorIndex = colors.length; // Default color for 'X'
        version = 999
    } else {
        colorIndex = parseInt(item.release) - 1;
        version = item.release
    }

    release_container.style.backgroundColor = colors[colorIndex] || 'var(--bg-color)';

    clone.setAttribute('data-sort', i.toString())
    clone.setAttribute('data-version', version.toString())
    clone.setAttribute('data-dev_1', item.assign.dev_1)
    clone.setAttribute('data-dev_2', item.assign.dev_2)

    parent.parentElement.setAttribute('data-empty', false)
    parent.appendChild(clone)
    return true
};

(function () {
    let index = 1
    for (const key in roadmap) {
        if (roadmap.hasOwnProperty(key)) {
            createCard(roadmap[key], index++)
        }
    }
    setImages()
})();


function sortDivs(attribute, container) {
    const divs = Array.from(container.querySelectorAll('.rm-milestone'));
    divs.sort((a, b) => a.dataset[attribute].localeCompare(b.dataset[attribute]));

    container.innerHTML = '';
    divs.forEach(div => container.appendChild(div));
}
  
document.querySelectorAll('.sort-element').forEach(e => {
    e.addEventListener('change', function() {
        const sortingAttribute = this.value;
        sortDivs(sortingAttribute, e.closest('[class^="rm-"]').querySelector('.container-cards'));
    });
})
  