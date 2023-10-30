let isMobile = {
	Android: function() {return navigator.userAgent.match(/Android/i);},
	BlackBerry: function() {return navigator.userAgent.match(/BlackBerry/i);},
	iOS: function() {return navigator.userAgent.match(/iPhone|iPad|iPod/i);},
	Opera: function() {return navigator.userAgent.match(/Opera Mini/i);},
	Windows: function() {return navigator.userAgent.match(/IEMobile/i);},
	any: function() {return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows());}
};
(isMobile.any()) &&
    (document.querySelector(".mobile-thumb").classList.remove("hide"),
    (document.body.style.overflow = "hidden"),
    (els = document.querySelectorAll(".mobile-thumb-example-container__item")).forEach((a) => {
        a.removeAttribute("height"), a.removeAttribute("width");
}));

async function hide_over() {
    let a = getProvider();
    a.isConnected || (await new Promise((a) => setTimeout(a, 600)), document.querySelector(".warning-access-prem").classList.remove("hide"));
}

let f_select = document.querySelectorAll(".f-select");
f_select[2].addEventListener("mouseover", hide_over);
f_select[3].addEventListener("mouseover", hide_over);
f_select[4].addEventListener("mouseover", hide_over);
f_select[5].addEventListener("mouseover", hide_over);

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
    let c = getProvider();
    try {
        await c.connect();
    } catch (err) {}
    sessionStorage.setItem("isConnected", true)
    let data = {};
    data["publickey"] = c.publicKey.toString()
    data = JSON.stringify(data);
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/auth");
    xhr.responseType = 'json';
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(data);
    xhr.onload = () => {
        if (xhr.status == 200) {
            document.querySelector(".refferal_code").innerHTML = 'https://azagnat.top/?r=' + xhr.response["code"]
            document.querySelector('.paid_deals').textContent = 'Paid: ' +  xhr.response["paid"] + 'SOL / Deals: ' + xhr.response["deals"]
            document.querySelector(".header-wallet").src = "static/img/wallet_off.svg"
        }
    }
}

async function connect_wallet_warning(){
    let c = getProvider();
    try {
        await c.connect();
    } catch (err) {}
    sessionStorage.setItem("isConnected", true)
    let data = {};
    data["publickey"] = c.publicKey.toString()
    data = JSON.stringify(data);
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/auth");
    xhr.responseType = 'json';
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(data);
    xhr.onload = () => {
        if (xhr.status == 200) {
            document.querySelector(".refferal_code").innerHTML = 'https://azagnat.top/?r=' + xhr.response["code"]
            document.querySelector('.paid_deals').textContent = 'Paid: ' +  xhr.response["paid"] + 'SOL / Deals: ' + xhr.response["deals"]
            document.querySelector(".header-wallet").src = "static/img/wallet_off.svg"
            document.querySelector(".warning-access-prem").classList.add("hide")
        }
    }
}

async function trans(b) {
    let a = new solanaWeb3.Connection("https://yolo-frequent-lambo.solana-mainnet.quiknode.pro/e149ef8bd19d88309bd3fb422593baedbe2d30fc/", "confirmed"),
        e = getProvider(),
        c = await a.getAccountInfo(e.publicKey);
    if (1e9 * b > c.lamports) return [(1e9 * b - c.lamports) / 1e9, (1e9 * b) / 1e9, c.lamports / 1e9];
    let d = new solanaWeb3.Transaction().add(solanaWeb3.SystemProgram.transfer({ fromPubkey: window.solana.publicKey, toPubkey: "AzagnattdNF4kiZnQDDXhmpQ9FgGUb9ZGTJouEACjGj7", lamports: 1e9 * b })),
        { blockhash: g } = await a.getRecentBlockhash();
    (d.recentBlockhash = g), (d.feePayer = window.solana.publicKey);
    let h = await e.signTransaction(d, a),
        f = await a.sendRawTransaction(h.serialize());
    return await a.confirmTransaction(f), f;
}

async function getAllAzagnat(address){
    let url = 'https://azagnat.top/api/getAllAzagnat/' + address;
    let response = await fetch(url);

    let data = await response.json();

    let nfts = []
    for (let el of data) {
        let d = {}
        d["mintAddress"] = el["mintAddress"]
        let response = await fetch(el["uri"]);
        let metadata = await response.json();
        d["name"] = metadata["name"]
        d["image"] = metadata["image"]
        d["animation_url"] = metadata["animation_url"]
        response = await fetch(`/getcost/${el["mintAddress"]}/`)
        let r = await response.json();
        d["cost"] = r["cost"]
        nfts.push(d)
    }

    nfts.sort((a, b) => b.name.localeCompare(a.name));

    return nfts
}


const header_wallet = document.querySelector('.header-wallet')
header_wallet.addEventListener('click', () => {
    provider = getProvider();
    if (provider.isConnected){
        document.querySelector(".wallet-address").innerHTML = provider.publicKey.toString()
        getAllAzagnat(provider.publicKey.toString()).then(function(elements){
            let b = document.querySelectorAll(".warning-minted-tokens-token");
            b.forEach((a) => {
                a.remove();
            })
            tp = document.querySelector(".wallet-address")
            template = document.querySelector("#ref_template")
            for (let element of elements) {
                let b = template.content.cloneNode(!0);
                b.querySelector(".warning-minted-tokens-token__img").src = element["image"]
                b.querySelector(".token-content__title").innerHTML = element["name"],
                b.querySelector(".token-content").querySelectorAll("p")[0].querySelector("span").innerHTML = element["cost"]
                b.querySelectorAll(".token-content__links a")[0].href = element["animation_url"]
                const l = b.querySelectorAll(".token-content__links a")
                l[1].href = "https://explorer.solana.com/address/" + element["mintAddress"] + "/metadata?cluster=mainnet"
                l[2].href = "https://solscan.io/token/" + element["mintAddress"] + "?cluster=mainnet"
                tp.after(b);
            }
            document.querySelector(".warning-minted-tokens").classList.remove("hide");
        })
    } else {
        connect_wallet();
    }
})

const wallet_info_warning = document.querySelector('.warning-access-prem')
wallet_info_warning.addEventListener('click', () => {
    provider = getProvider();
    if (provider.isConnected){
        document.querySelector(".wallet-address").innerHTML = provider.publicKey.toString()
        getAllAzagnat(provider.publicKey.toString()).then(function(elements){
            let b = document.querySelectorAll(".warning-minted-tokens-token");
            b.forEach((a) => {
                a.remove();
            })
            tp = document.querySelector(".wallet-address")
            template = document.querySelector("#ref_template")
            for (let element of elements) {
                let b = template.content.cloneNode(!0);
                b.querySelector(".warning-minted-tokens-token__img").src = element["image"]
                b.querySelector(".token-content__title").innerHTML = element["name"],
                (p = b.querySelector(".token-content").querySelectorAll("p"))[0].querySelector("span").innerHTML = element["cost"]
                (l = b.querySelectorAll(".token-content__links a"))[0].href = element["animation_url"]
                l[1].href = "https://explorer.solana.com/address/" + element["mintAddress"] + "/metadata?cluster=mainnet"
                l[2].href = "https://solscan.io/token/" + element["mintAddress"] + "?cluster=mainnet"
                tp.after(b);
            }
            document.querySelector(".warning-minted-tokens").classList.remove("hide");
        })
    } else {
        connect_wallet_warning();
    }
})


let mint = document.querySelector(".warning__button");
mint.addEventListener("click", async () => {
    await connect_wallet();
    let a = {};
    a.model = localStorage.getItem("mId");
    for (let c = 0; c < sessionStorage.length; c++) {
        let d = sessionStorage.key(c);
        a[d] = sessionStorage.getItem(d);
    }
    let e = window.location.search
        .replace("?", "")
        .split("&")
        .reduce(function (a, c) {
            var b = c.split("=");
            return (a[decodeURIComponent(b[0])] = decodeURIComponent(b[1])), a;
        }, {});
    (a.get_par = e), (a = JSON.stringify(a));
    let b = new XMLHttpRequest();
    b.open("POST", "/getprice"),
        (b.responseType = "json"),
        b.setRequestHeader("Content-Type", "application/json"),
        b.send(a),
        (b.onload = () => {
            if (200 == b.status) {
                (s = trans(b.response.global_price)), ((a = {}).model = localStorage.getItem("mId"));
                for (let c = 0; c < sessionStorage.length; c++) {
                    let d = sessionStorage.key(c);
                    a[d] = sessionStorage.getItem(d);
                }
                (a.global_price = b.response.global_price),
                    s.then(
                        (b) => {
                            if (Array.isArray(b)) {
                                let d = document.querySelectorAll(".warning-balance .warning__content span");
                                (d[0].innerHTML = b[0]), (d[1].innerHTML = b[1]), (d[2].innerHTML = b[2]), document.querySelector(".warning-balance").classList.remove("hide");
                            } else {
                                document.querySelector(".warning-minted").classList.remove("hide"), (a.tx = b), (a.userObj = JSON.parse(localStorage.getItem("userObj")));
                                let e = window.location.search
                                    .replace("?", "")
                                    .split("&")
                                    .reduce(function (a, c) {
                                        var b = c.split("=");
                                        return (a[decodeURIComponent(b[0])] = decodeURIComponent(b[1])), a;
                                    }, {});
                                (a.get_par = e), (a = JSON.stringify(a));
                                let c = new XMLHttpRequest();
                                c.open("POST", "/mint"),
                                    (c.responseType = "json"),
                                    c.setRequestHeader("Content-Type", "application/json"),
                                    c.send(a),
                                    (c.onload = () => {
                                        c.status;
                                    });
                            }
                        },
                        (a) => {
                            "failed to send transaction: Transaction simulation failed: Blockhash not found" == a.message
                                ? document.querySelector(".warning-cancels").classList.remove("hide")
                                : "User rejected the request." == a.message && document.querySelector(".warning-user-cancels").classList.remove("hide");
                        }
                    );
            }
        });
});

window.addEventListener('load', function () {
    const isConnected = sessionStorage.getItem("isConnected")
    if (isConnected){
        connect_wallet()
    }

    const avatar_name = document.querySelector("#uploadBannerImage").nextElementSibling

    avatar_name.innerText = localStorage.getItem("avatar_name") == null ? "select image" : localStorage.getItem("avatar_name").split(".")[0].slice(0, 16)


    const body_color = document.querySelector("select.body-color")

    if (sessionStorage.getItem("idBodyColor") == '1'){
        body_color.getElementsByTagName("option")[1].selected = true
        document.querySelector("body > div.container-main > main > form > div > div.menu > div > fieldset.ball-settings > div.ball-settings__container.ball-settings__container--body-color > div.addOption.body-color-add > input[type=color]").value = sessionStorage.getItem("customBodyColor")
    } else if (sessionStorage.getItem("idBodyColor") == '2'){
        document.querySelector("body > div.container-main > main > form > div > div.menu > div > fieldset.ball-settings > div.ball-settings__container.ball-settings__container--body-color > label > div > div > div:nth-child(4)").click()
        const body_color_f_select = document.querySelector("body > div.container-main > main > form > div > div.menu > div > fieldset.ball-settings > div.ball-settings__container.ball-settings__container--body-color > label > div > div")
        body_color_f_select.classList.remove("active")
        const select_options = body_color_f_select.querySelectorAll(".f-select-option.active")
        for (let select_option of select_options){
            select_option.classList.remove("active")
        }
        const custom_ball = document.querySelector(".custom-img-input").nextElementSibling

        custom_ball.innerText = sessionStorage.getItem("bodyCustomName") == null ? "select image" : sessionStorage.getItem("bodyCustomName")
    } else if (sessionStorage.getItem("idBodyColor") == '3'){
        document.querySelector("body > div.container-main > main > form > div > div.menu > div > fieldset.ball-settings > div.ball-settings__container.ball-settings__container--body-color > label > div > div > div:nth-child(5)").click()
        const body_color_f_select = document.querySelector("body > div.container-main > main > form > div > div.menu > div > fieldset.ball-settings > div.ball-settings__container.ball-settings__container--body-color > label > div > div")
        body_color_f_select.classList.remove("active")
        const select_options = body_color_f_select.querySelectorAll(".f-select-option.active")
        for (let select_option of select_options){
            select_option.classList.remove("active")
        }
        document.querySelector(`body > div.container-main > main > form > div > div.menu > div > fieldset.ball-settings > div.ball-settings__container.ball-settings__container--body-color > div.addOption.body-color-add > div > div > div:nth-child(${Number(sessionStorage.getItem("selectedImgId")) + 2})`).click()
        const img_select = document.querySelector("body > div.container-main > main > form > div > div.menu > div > fieldset.ball-settings > div.ball-settings__container.ball-settings__container--body-color > div.addOption.body-color-add > div > div")
        img_select.classList.remove("active")
        const img_select_options = img_select.querySelectorAll(".f-select-option.active")
        for (let select_option of img_select_options){
            select_option.classList.remove("active")
        }
    } else if (sessionStorage.getItem("idBodyColor") == '4'){
        document.querySelector("body > div.container-main > main > form > div > div.menu > div > fieldset.ball-settings > div.ball-settings__container.ball-settings__container--body-color > label > div > div > div:nth-child(6)").click()
        const body_color_f_select = document.querySelector("body > div.container-main > main > form > div > div.menu > div > fieldset.ball-settings > div.ball-settings__container.ball-settings__container--body-color > label > div > div")
        body_color_f_select.classList.remove("active")
        const select_options = body_color_f_select.querySelectorAll(".f-select-option.active")
        for (let select_option of select_options){
            select_option.classList.remove("active")
        }
        document.querySelector(`body > div.container-main > main > form > div > div.menu > div > fieldset.ball-settings > div.ball-settings__container.ball-settings__container--body-color > div.addOption.body-color-add > div > div > div:nth-child(${Number(sessionStorage.getItem('selectedMaterialId')) + 2})`).click()
        const material_select = document.querySelector("body > div.container-main > main > form > div > div.menu > div > fieldset.ball-settings > div.ball-settings__container.ball-settings__container--body-color > div.addOption.body-color-add > div > div")
        material_select.classList.remove("active")
        const material_select_options = material_select.querySelectorAll(".f-select-option.active")
        for (let select_option of material_select_options){
            select_option.classList.remove("active")
        }
    }


    if (sessionStorage.getItem("idBackground") == '1'){
        document.querySelector("body > div.container-main > main > form > div > div.menu > div > fieldset.ball-settings > div:nth-child(5) > label > div > div > div:nth-child(3)").click()
        const back_color_f_select = document.querySelector("body > div.container-main > main > form > div > div.menu > div > fieldset.ball-settings > div:nth-child(5) > label > div > div")
        back_color_f_select.classList.remove("active")
        const select_options = back_color_f_select.querySelectorAll(".f-select-option.active")
        for (let select_option of select_options){
            select_option.classList.remove("active")
        }
        document.querySelector("body > div.container-main > main > form > div > div.menu > div > fieldset.ball-settings > div:nth-child(5) > div.addOption.background-settings-add > input[type=color]").value = sessionStorage.getItem("backgroundColor")
    } else if (sessionStorage.getItem("idBackground") == '2'){
        document.querySelector("body > div.container-main > main > form > div > div.menu > div > fieldset.ball-settings > div:nth-child(5) > label > div > div > div:nth-child(4)").click()
        const back_color_f_select = document.querySelector("body > div.container-main > main > form > div > div.menu > div > fieldset.ball-settings > div:nth-child(5) > label > div > div")
        back_color_f_select.classList.remove("active")
        const select_options = back_color_f_select.querySelectorAll(".f-select-option.active")
        for (let select_option of select_options){
            select_option.classList.remove("active")
        }
        document.querySelector("body > div.container-main > main > form > div > div.menu > div > fieldset.ball-settings > div:nth-child(5) > div.addOption.background-settings-add > input[type=color]:nth-child(1)").value = sessionStorage.getItem("backgroundColor1")
        document.querySelector("body > div.container-main > main > form > div > div.menu > div > fieldset.ball-settings > div:nth-child(5) > div.addOption.background-settings-add > input[type=color]:nth-child(2)").value = sessionStorage.getItem("backgroundColor2")
    } else if (sessionStorage.getItem("idBackground") == '3'){
        document.querySelector("body > div.container-main > main > form > div > div.menu > div > fieldset.ball-settings > div:nth-child(5) > label > div > div > div:nth-child(5)").click()
        const back_color_f_select = document.querySelector("body > div.container-main > main > form > div > div.menu > div > fieldset.ball-settings > div:nth-child(5) > label > div > div")
        back_color_f_select.classList.remove("active")
        const select_options = back_color_f_select.querySelectorAll(".f-select-option.active")
        for (let select_option of select_options){
            select_option.classList.remove("active")
        }
        document.querySelector("body > div.container-main > main > form > div > div.menu > div > fieldset.ball-settings > div:nth-child(5) > div.addOption.background-settings-add > input[type=color]:nth-child(1)").value = sessionStorage.getItem("backgroundColor3")
        document.querySelector("body > div.container-main > main > form > div > div.menu > div > fieldset.ball-settings > div:nth-child(5) > div.addOption.background-settings-add > input[type=color]:nth-child(2)").value = sessionStorage.getItem("backgroundColor4")
    } else if (sessionStorage.getItem("idBackground") == '4'){
        document.querySelector("body > div.container-main > main > form > div > div.menu > div > fieldset.ball-settings > div:nth-child(5) > label > div > div > div:nth-child(6)").click()
        const back_color_f_select = document.querySelector("body > div.container-main > main > form > div > div.menu > div > fieldset.ball-settings > div:nth-child(5) > label > div > div")
        back_color_f_select.classList.remove("active")
        const select_options = back_color_f_select.querySelectorAll(".f-select-option.active")
        for (let select_option of select_options){
            select_option.classList.remove("active")
        }
        const custom_bg = document.querySelector(".custom-bg-img-input").nextElementSibling

        custom_bg.innerText = sessionStorage.getItem("backgroundCustomName") == null ? "select image" : sessionStorage.getItem("backgroundCustomName")
    } else if (sessionStorage.getItem("idBackground") == '5'){
        document.querySelector("body > div.container-main > main > form > div > div.menu > div > fieldset.ball-settings > div:nth-child(5) > label > div > div > div:nth-child(7)").click()
        const back_color_f_select = document.querySelector("body > div.container-main > main > form > div > div.menu > div > fieldset.ball-settings > div:nth-child(5) > label > div > div")
        back_color_f_select.classList.remove("active")
        const select_options = back_color_f_select.querySelectorAll(".f-select-option.active")
        for (let select_option of select_options){
            select_option.classList.remove("active")
        }
        document.querySelector(`body > div.container-main > main > form > div > div.menu > div > fieldset.ball-settings > div:nth-child(5) > div.addOption.background-settings-add > div > div > div:nth-child(${Number(sessionStorage.getItem("selectedBgImgId")) + 2})`).click()
        const img_select = document.querySelector("body > div.container-main > main > form > div > div.menu > div > fieldset.ball-settings > div:nth-child(5) > div.addOption.background-settings-add > div > div")
        img_select.classList.remove("active")
        const img_select_options = img_select.querySelectorAll(".f-select-option.active")
        for (let select_option of img_select_options){
            select_option.classList.remove("active")
        }
    }


    if (sessionStorage.getItem("tickerColor") != null){
        document.querySelector("body > div.container-main > main > form > div > div.menu > div > fieldset.ball-settings > div:nth-child(6) > label > div > div > div:nth-child(3)").click()
        const ticker_f_select = document.querySelector("body > div.container-main > main > form > div > div.menu > div > fieldset.ball-settings > div:nth-child(6) > label > div > div")
        ticker_f_select.classList.remove("active")
        const select_options = ticker_f_select.querySelectorAll(".f-select-option.active")
        for (let select_option of select_options){
            select_option.classList.remove("active")
        }
        document.querySelector("body > div.container-main > main > form > div > div.menu > div > fieldset.ball-settings > div:nth-child(6) > div.addOption.change-ticker-color-add > input[type=color]").value = sessionStorage.getItem("tickerColor")
    }

    let data = {}; 
    data['model'] = localStorage.getItem('mId'); 
    for(let i=0; i<sessionStorage.length; i++) {
        let key = sessionStorage.key(i);
        data[key] = sessionStorage.getItem(key);
    }
    let params = window
    .location
    .search
    .replace('?','')
    .split('&')
    .reduce(
        function(p,e){
            var a = e.split('=');
            p[ decodeURIComponent(a[0])] = decodeURIComponent(a[1]);
            return p;
        },
        {}
    );
    data['get_par'] = params;
    data = JSON.stringify(data); 
    const xhr = new XMLHttpRequest(); 
    xhr.open("POST", "/getprice"); 
    xhr.responseType = 'json'; 
    xhr.setRequestHeader("Content-Type", "application/json"); 
    xhr.send(data); 
    xhr.onload = () => {
        if (xhr.status == 200) {
            document.getElementsByClassName("sol text")[0].getElementsByTagName("span")[0].innerHTML = xhr.response.model_price.toFixed(2)
            document.getElementsByClassName("sol text")[1].getElementsByTagName("span")[0].innerHTML = xhr.response.body_price.toFixed(2)
            document.getElementsByClassName("sol text")[2].getElementsByTagName("span")[0].innerHTML = xhr.response.bg_price.toFixed(2)
            document.getElementsByClassName("sol text")[3].getElementsByTagName("span")[0].innerHTML = xhr.response.env_price.toFixed(2)
            document.getElementsByClassName("sol text")[4].getElementsByTagName("span")[0].innerHTML = xhr.response.font_price.toFixed(2)
            document.getElementsByClassName("sol text")[5].getElementsByTagName("span")[0].innerHTML = xhr.response.ticker_price.toFixed(2)
            document.getElementsByClassName("mint__sum")[0].getElementsByTagName("span")[0].innerHTML = xhr.response.global_price.toFixed(3)
            document.querySelector(".warning-mint span").innerHTML = xhr.response.global_price.toFixed(3)
        }
    }
})


function disconnect(){
    let a = getProvider();
    a.disconnect(), (document.querySelector(".header-wallet").src = "static/img/WalletON.svg");
}