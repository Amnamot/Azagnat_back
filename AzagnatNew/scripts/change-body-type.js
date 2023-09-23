export function changeBodyType () {
  const sel = document.querySelector('.body-type')
  const opts = sel.querySelectorAll('option')
  opts.forEach(i => i.removeAttribute('selected'))
  opts[Number(localStorage.getItem('mId'))].setAttribute('selected', 'selected')
  document.querySelector('.f-select-container__body-type .placeholder').innerHTML = opts[Number(localStorage.getItem('mId'))].innerText
  sel.addEventListener('change', () => {
    let data = {}; 
    data['model'] = sel.value
    for(let i = 0; i < sessionStorage.length; i++) {
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
    localStorage.setItem('mId', sel.value)
    location.reload()
  })
}


