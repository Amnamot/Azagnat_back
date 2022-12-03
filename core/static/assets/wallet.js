(window.innerWidth < 1024 || window.innerHeight < 500) &&
    (document.querySelector(".mobile-thumb").classList.remove("hide"),
    (document.body.style.overflow = "hidden"),
    (els = document.querySelectorAll(".mobile-thumb-example-container__item")).forEach((a) => {
        a.removeAttribute("height"), a.removeAttribute("width");
    }));
const getProvider = () => {
    if ("solana" in window) {
        let a = window.solana;
        if (a.isPhantom) return a;
    }
    window.open("https://phantom.app/", "_blank");
};
async function connect_wallet() {
    let c = getProvider();
    try {
        await c.connect();
    } catch (d) {}
    sessionStorage.setItem("islog", !0);
    let b = {};
    (b.publickey = c.publicKey.toString()), (b = JSON.stringify(b));
    let a = new XMLHttpRequest();
    a.open("POST", "/auth"),
        (a.responseType = "json"),
        a.setRequestHeader("Content-Type", "application/json"),
        a.send(b),
        (a.onload = () => {
            200 == a.status && (document.querySelector(".header-wallet").src = "static/img/wallet_off.svg");
        });
}
async function connect_wallet_warn() {
    let c = getProvider();
    try {
        await c.connect();
    } catch (d) {}
    sessionStorage.setItem("islog", !0);
    let b = {};
    (b.publickey = c.publicKey.toString()), (b = JSON.stringify(b));
    let a = new XMLHttpRequest();
    a.open("POST", "/auth"),
        (a.responseType = "json"),
        a.setRequestHeader("Content-Type", "application/json"),
        a.send(b),
        (a.onload = () => {
            200 == a.status && ((document.querySelector(".header-wallet").src = "static/img/wallet_off.svg"), document.querySelector(".warning-access-prem").classList.add("hide"));
        });
}
let wallet = document.querySelector(".header-wallet");
async function hide_over() {
    let a = getProvider();
    a.isConnected || (await new Promise((a) => setTimeout(a, 600)), document.querySelector(".warning-access-prem").classList.remove("hide"));
}
wallet.addEventListener("click", function () {
    let c = getProvider();
    if (c.isConnected) {
        let b = {};
        (b.publickey = c.publicKey.toString()), (b = JSON.stringify(b));
        let a = new XMLHttpRequest();
        a.open("POST", "/auth"),
            (a.responseType = "json"),
            a.setRequestHeader("Content-Type", "application/json"),
            a.send(b),
            (a.onload = () => {
                if (200 == a.status) {
                    let b = document.querySelectorAll(".warning-minted-tokens-token");
                    b.forEach((a) => {
                        a.remove();
                    }),
                        (document.querySelector(".wallet-address").innerHTML = c.publicKey.toString()),
                        (tp = document.querySelector(".wallet-address")),
                        (template = document.querySelector("#ref_template")),
                        a.response.refs.forEach((a) => {
                            let b = template.content.cloneNode(!0);
                            (b.querySelector(".warning-minted-tokens-token__img").src = a.screen),
                                (b.querySelector(".token-content__title span").innerHTML = a.token_id),
                                ((p = b.querySelector(".token-content").querySelectorAll("p"))[0].querySelector("span").innerHTML = a.cost),
                                (p[1].querySelector("span").innerHTML = a.paid),
                                (p[2].querySelector("span").innerHTML = a.deals),
                                ((l = b.querySelectorAll(".token-content__links a"))[0].href = a.token_link),
                                (l[1].href = "https://explorer.solana.com/address/" + a.contract + "/metadata?cluster=devnet"),
                                (l[2].href = "https://solscan.io/token/" + a.contract + "?cluster=devnet"),
                                (l[3].href = "https://solana.fm/address/" + a.contract + "?cluster=devnet-solana");
                            let c = b.querySelector(".token-content__button");
                            c.setAttribute("title", a.ref_link), tp.after(b);
                        }),
                        document.querySelector(".warning-minted-tokens").classList.remove("hide");
                }
            });
    } else connect_wallet();
}),
    (warn_wallet = document.querySelectorAll(".warning-access-prem")[1]).addEventListener("click", connect_wallet_warn);
let f_select = document.querySelectorAll(".f-select");
f_select[2].addEventListener("mouseover", hide_over),
    f_select[3].addEventListener("mouseover", hide_over),
    f_select[4].addEventListener("mouseover", hide_over),
    f_select[5].addEventListener("mouseover", hide_over),
    (welcome_b1 = document.querySelector(".warning-welcomes-buttons").querySelectorAll(".warning__button")[0]).addEventListener("click", () => {
        localStorage.setItem("iswelcome", !0);
    }),
    window.addEventListener("load", () => {
        null != localStorage.getItem("iswelcome") ? document.querySelector(".warning-welcomes").classList.add("hide") : document.querySelector(".warning-welcomes").classList.remove("hide"),
            sessionStorage.getItem("islog") && connect_wallet();
        let a = {};
        a.model = parseInt(localStorage.getItem("mId"));
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
                200 == b.status &&
                    ((document.getElementsByClassName("sol text")[0].getElementsByTagName("span")[0].innerHTML = b.response.model_price.toFixed(2)),
                    (document.getElementsByClassName("sol text")[1].getElementsByTagName("span")[0].innerHTML = b.response.body_price.toFixed(2)),
                    (document.getElementsByClassName("sol text")[2].getElementsByTagName("span")[0].innerHTML = b.response.bg_price.toFixed(2)),
                    (document.getElementsByClassName("sol text")[3].getElementsByTagName("span")[0].innerHTML = b.response.ticker_price.toFixed(2)),
                    (document.getElementsByClassName("mint__sum")[0].getElementsByTagName("span")[0].innerHTML = b.response.global_price.toFixed(2)),
                    (document.querySelector(".warning-mint span").innerHTML = b.response.global_price.toFixed(2)),
                    localStorage.setItem("model_price", b.response.model_price),
                    sessionStorage.setItem("body_price", b.response.body_price),
                    sessionStorage.setItem("bg_price", b.response.bg_price),
                    sessionStorage.setItem("ticker_price", b.response.ticker_price),
                    sessionStorage.setItem("global_price", b.response.global_price));
            });
    });
let body_color = document.querySelector(".body-color");
body_color.addEventListener("change", function () {
    if ("0" == body_color.value) {
        let a = {};
        a.model = parseInt(localStorage.getItem("mId"));
        for (let c = 0; c < sessionStorage.length; c++) {
            let d = sessionStorage.key(c);
            a[d] = sessionStorage.getItem(d);
        }
        a.idBodyColor = body_color.value;
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
                200 == b.status &&
                    ((document.getElementsByClassName("sol text")[0].getElementsByTagName("span")[0].innerHTML = b.response.model_price.toFixed(2)),
                    (document.getElementsByClassName("sol text")[1].getElementsByTagName("span")[0].innerHTML = b.response.body_price.toFixed(2)),
                    (document.getElementsByClassName("sol text")[2].getElementsByTagName("span")[0].innerHTML = b.response.bg_price.toFixed(2)),
                    (document.getElementsByClassName("sol text")[3].getElementsByTagName("span")[0].innerHTML = b.response.ticker_price.toFixed(2)),
                    (document.getElementsByClassName("mint__sum")[0].getElementsByTagName("span")[0].innerHTML = b.response.global_price.toFixed(2)),
                    (document.querySelector(".warning-mint span").innerHTML = b.response.global_price.toFixed(2)),
                    localStorage.setItem("model_price", b.response.model_price),
                    sessionStorage.setItem("body_price", b.response.body_price),
                    sessionStorage.setItem("bg_price", b.response.bg_price),
                    sessionStorage.setItem("ticker_price", b.response.ticker_price),
                    sessionStorage.setItem("global_price", b.response.global_price));
            });
    }
});
let background = document.querySelector(".background-settings");
background.addEventListener("change", function () {
    if ("0" == background.value) {
        let c = document.querySelector(".background-settings-add");
        for (; c.firstChild; ) c.removeChild(c.firstChild);
        let a = {};
        a.model = parseInt(localStorage.getItem("mId"));
        for (let d = 0; d < sessionStorage.length; d++) {
            let e = sessionStorage.key(d);
            a[e] = sessionStorage.getItem(e);
        }
        (a.idBackground = background.value), sessionStorage.setItem("idBackground", background.value);
        let f = window.location.search
            .replace("?", "")
            .split("&")
            .reduce(function (a, c) {
                var b = c.split("=");
                return (a[decodeURIComponent(b[0])] = decodeURIComponent(b[1])), a;
            }, {});
        (a.get_par = f), (a = JSON.stringify(a));
        let b = new XMLHttpRequest();
        b.open("POST", "/getprice"),
            (b.responseType = "json"),
            b.setRequestHeader("Content-Type", "application/json"),
            b.send(a),
            (b.onload = () => {
                200 == b.status &&
                    ((document.getElementsByClassName("sol text")[0].getElementsByTagName("span")[0].innerHTML = b.response.model_price.toFixed(2)),
                    (document.getElementsByClassName("sol text")[1].getElementsByTagName("span")[0].innerHTML = b.response.body_price.toFixed(2)),
                    (document.getElementsByClassName("sol text")[2].getElementsByTagName("span")[0].innerHTML = b.response.bg_price.toFixed(2)),
                    (document.getElementsByClassName("sol text")[3].getElementsByTagName("span")[0].innerHTML = b.response.ticker_price.toFixed(2)),
                    (document.getElementsByClassName("mint__sum")[0].getElementsByTagName("span")[0].innerHTML = b.response.global_price.toFixed(2)),
                    (document.querySelector(".warning-mint span").innerHTML = b.response.global_price.toFixed(2)),
                    localStorage.setItem("model_price", b.response.model_price),
                    sessionStorage.setItem("body_price", b.response.body_price),
                    sessionStorage.setItem("bg_price", b.response.bg_price),
                    sessionStorage.setItem("ticker_price", b.response.ticker_price),
                    sessionStorage.setItem("global_price", b.response.global_price));
            });
    }
});
let ticker = document.querySelector(".change-ticker-color");
async function trans(b) {
    let a = new solanaWeb3.Connection(solanaWeb3.clusterApiUrl("mainnet"), "confirmed"),
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
ticker.addEventListener("change", function () {
    if ("0" == ticker.value) {
        let a = {};
        a.model = parseInt(localStorage.getItem("mId"));
        for (let c = 0; c < sessionStorage.length; c++) {
            let d = sessionStorage.key(c);
            a[d] = sessionStorage.getItem(d);
        }
        a.tickerColor = "#004f20";
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
                200 == b.status &&
                    ((document.getElementsByClassName("sol text")[0].getElementsByTagName("span")[0].innerHTML = b.response.model_price.toFixed(2)),
                    (document.getElementsByClassName("sol text")[1].getElementsByTagName("span")[0].innerHTML = b.response.body_price.toFixed(2)),
                    (document.getElementsByClassName("sol text")[2].getElementsByTagName("span")[0].innerHTML = b.response.bg_price.toFixed(2)),
                    (document.getElementsByClassName("sol text")[3].getElementsByTagName("span")[0].innerHTML = b.response.ticker_price.toFixed(2)),
                    (document.getElementsByClassName("mint__sum")[0].getElementsByTagName("span")[0].innerHTML = b.response.global_price.toFixed(2)),
                    (document.querySelector(".warning-mint span").innerHTML = b.response.global_price.toFixed(2)),
                    localStorage.setItem("model_price", b.response.model_price),
                    sessionStorage.setItem("body_price", b.response.body_price),
                    sessionStorage.setItem("bg_price", b.response.bg_price),
                    sessionStorage.setItem("ticker_price", b.response.ticker_price),
                    sessionStorage.setItem("global_price", b.response.global_price));
            });
    }
});
let mint = document.querySelectorAll(".warning__button")[2];
mint.addEventListener("click", async () => {
    if (null == localStorage.getItem("userObj")) document.querySelector(".warning-req-param").classList.remove("hide");
    else if (5 == Object.keys(JSON.parse(localStorage.getItem("userObj"))).length) {
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
                                    console.log(a);
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
    } else document.querySelector(".warning-req-param").classList.remove("hide");
});
const wallet_info_warn = document.querySelector(".warning-minted-img");
wallet_info_warn.addEventListener("click", () => {
    document.querySelector(".warning-minted").classList.add("hide");
    let c = getProvider();
    if (c.isConnected) {
        let b = {};
        (b.publickey = c.publicKey.toString()), (b = JSON.stringify(b));
        let a = new XMLHttpRequest();
        a.open("POST", "/auth"),
            (a.responseType = "json"),
            a.setRequestHeader("Content-Type", "application/json"),
            a.send(b),
            (a.onload = () => {
                if (200 == a.status) {
                    let b = document.querySelectorAll(".warning-minted-tokens-token");
                    b.forEach((a) => {
                        a.remove();
                    }),
                        (document.querySelector(".wallet-address").innerHTML = c.publicKey.toString()),
                        (tp = document.querySelector(".wallet-address")),
                        (template = document.querySelector("#ref_template")),
                        a.response.refs.forEach((a) => {
                            let b = template.content.cloneNode(!0);
                            (b.querySelector(".warning-minted-tokens-token__img").src = a.screen),
                                (b.querySelector(".token-content__title span").innerHTML = a.token_id),
                                ((p = b.querySelector(".token-content").querySelectorAll("p"))[0].querySelector("span").innerHTML = a.cost),
                                (p[1].querySelector("span").innerHTML = a.paid),
                                (p[2].querySelector("span").innerHTML = a.deals),
                                ((l = b.querySelectorAll(".token-content__links a"))[0].href = a.token_link),
                                (l[1].href = "https://explorer.solana.com/address/" + a.contract + "/metadata?cluster=devnet"),
                                (l[2].href = "https://solscan.io/token/" + a.contract + "?cluster=devnet"),
                                (l[3].href = "https://solana.fm/address/" + a.contract + "?cluster=devnet-solana");
                            let c = b.querySelector(".token-content__button");
                            c.setAttribute("title", a.ref_link), tp.after(b);
                        }),
                        document.querySelector(".warning-minted-tokens").classList.remove("hide");
                }
            });
    } else connect_wallet();
});
let dis = document.querySelectorAll(".warning__button")[3];
dis.addEventListener("click", () => {
    let a = getProvider();
    a.disconnect(), (document.querySelector(".header-wallet").src = "static/img/WalletON.svg");
});

