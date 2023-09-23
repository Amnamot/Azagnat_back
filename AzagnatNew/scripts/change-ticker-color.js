const sel = document.querySelector('.change-ticker-color')

export function changeTickerColor (textConfig, tickerInitColor) {
  const addContainer = document.querySelector('.change-ticker-color-add')

  if (sessionStorage.getItem('tickerColor')) {
    textConfig.color = sessionStorage.getItem('tickerColor')
  }

  sel.addEventListener('change', () => {
    sessionStorage.setItem("tickerId", sel.value)
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
    try {
      xhr.send(data); 
    } catch (e) {
      console.error(e);
    }
    xhr.onload = () => {
        if (xhr.status == 200 && xhr.response) {
            document.getElementsByClassName("sol text")[0].getElementsByTagName("span")[0].innerHTML = xhr.response.model_price.toFixed(2)
            document.getElementsByClassName("sol text")[1].getElementsByTagName("span")[0].innerHTML = xhr.response.body_price.toFixed(2)
            document.getElementsByClassName("sol text")[2].getElementsByTagName("span")[0].innerHTML = xhr.response.bg_price.toFixed(2)
            document.getElementsByClassName("sol text")[3].getElementsByTagName("span")[0].innerHTML = xhr.response.ticker_price.toFixed(2)
            document.getElementsByClassName("mint__sum")[0].getElementsByTagName("span")[0].innerHTML = xhr.response.global_price.toFixed(3)
            document.querySelector(".warning-mint span").innerHTML = xhr.response.global_price.toFixed(3)
        }
    }
    //= ============default

    if (sel.value === '0') {
      addContainer.innerHTML = ''
      textConfig.color = tickerInitColor
      sessionStorage.getItem('tickerColor') ? sessionStorage.removeItem('tickerColor') : ''
    }

    //= ============color picker

    if (sel.value === '1') {
      addContainer.innerHTML = `
      <input type="color">
      `
      const colorPicker = addContainer.querySelector('input')
      colorPicker.addEventListener('input', () => {
        textConfig.color = colorPicker.value
        sessionStorage.setItem('tickerColor', colorPicker.value)
      })
    }
  })
}
