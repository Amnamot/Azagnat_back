(window.innerWidth < 1024 || window.innerHeight < 500) &&
    (document.querySelector(".mobile-thumb").classList.remove("hide"),
    (document.body.style.overflow = "hidden"),
    (els = document.querySelectorAll(".mobile-thumb-example-container__item")).forEach((a) => {
        a.removeAttribute("height"), a.removeAttribute("width");
}));

const getProvider = () => {
    if ('phantom' in window) {
      const provider = window.phantom?.solana;
  
      if (provider?.isPhantom) {
        return provider;
      }
    }
    window.open('https://phantom.app/', '_blank');
};


async function connect_wallet(){
    provider = getProvider();
    try {
        await provider.connect();
    } catch(err) {
        console.log(err);
    }
}


async function connect_wallet_warning(){
    provider = getProvider();
    try {
        await provider.connect();
    } catch(err) {
        console.log(err);
    }
}

async function hide_over() {
    let a = getProvider();
    a.isConnected || (await new Promise((a) => setTimeout(a, 600)), document.querySelector(".warning-access-prem").classList.remove("hide"));
}


const header_wallet = document.querySelector('.header-wallet')
header_wallet.addEventListener('click', () => {
    provider = getProvider();
    if (provider.isConnected){
        let d = {};
        d['publickey'] = provider.publicKey.toString();
        d = JSON.stringify(d);
        let xhr = new XMLHttpRequest();
        xhr.open('GET', '/article/xmlhttprequest/example/load');
        xhr.send();
        xhr.onload = function() {
            if (xhr.status != 200) {
                alert(`Ошибка ${xhr.status}: ${xhr.statusText}`);
            } else {
                alert(`Готово, получили ${xhr.response.length} байт`);
            }
        };
    }
})

window.addEventListener('load', () => {
    
})