import * as THREE from 'three'

const sel = document.querySelector('.background-settings')

export function changeBackground (scene, bgTexture, customInput, images) {

  let imgArr = images[0].backgroundImages

  function setBackground (scene, texture) {
    bgTexture = texture
    const container3d = document.querySelector('.container3d')
    const canvasAspect = container3d.clientWidth / container3d.clientHeight
    const imageAspect = bgTexture.image ? bgTexture.image.width / bgTexture.image.height : 1
    const aspectBg = imageAspect / canvasAspect

    bgTexture.offset.x = aspectBg > 1 ? (1 - 1 / aspectBg) / 2 : 0
    bgTexture.repeat.x = aspectBg > 1 ? 1 / aspectBg : 1

    bgTexture.offset.y = aspectBg > 1 ? 0 : (1 - aspectBg) / 2
    bgTexture.repeat.y = aspectBg > 1 ? 1 : aspectBg

    scene.background = bgTexture
  }

  let color = 0x1C1C1C
  const addContainer = document.querySelector('.background-settings-add')
  changeHandler(1)
  sel.addEventListener('change', changeHandler)
  function changeHandler (load) {
    sessionStorage.setItem("idBack", sel.value)
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
    if (load === 1) {
      const backgroundId = sessionStorage.getItem('idBackground')
      if (backgroundId && backgroundId === '0') {
        setBackground(scene, bgTexture)
        return
      }
      if (backgroundId && backgroundId === '1') {
        const color = sessionStorage.getItem('backgroundColor')
        const canvas = document.createElement('canvas')
        canvas.width = 100
        canvas.height = 100
        const ctx = canvas.getContext('2d')
        const gradient = ctx.createLinearGradient(0, 0, 100, 100)
        gradient.addColorStop(0, color)
        gradient.addColorStop(1, color)
        ctx.fillStyle = gradient
        ctx.fillRect(0, 0, 100, 100)
        const texture = new THREE.CanvasTexture(canvas)
        setBackground(scene, texture)
        return
      }
      if (backgroundId && backgroundId === '2') {
        const color1 = sessionStorage.getItem('backgroundColor1') ?? ''
        const color2 = sessionStorage.getItem('backgroundColor2') ?? ''
        const canvas = document.createElement('canvas')
        canvas.width = 100
        canvas.height = 100
        const ctx = canvas.getContext('2d')
        const gradient = ctx.createLinearGradient(0, 0, 100, 100)
        gradient.addColorStop(0, color1)
        gradient.addColorStop(1, color2)
        ctx.fillStyle = gradient
        ctx.fillRect(0, 0, 100, 100)
        const texture = new THREE.CanvasTexture(canvas)
        setBackground(scene, texture)
        return
      }
      if (backgroundId && backgroundId === '3') {
        const color1 = sessionStorage.getItem('backgroundColor3') ?? ''
        const color2 = sessionStorage.getItem('backgroundColor4') ?? ''
        const canvas = document.createElement('canvas')
        canvas.width = 100
        canvas.height = 100
        const ctx = canvas.getContext('2d')
        const gradient = ctx.createRadialGradient(50, 50, 25, 50, 50, 50)
        gradient.addColorStop(0, color1)
        gradient.addColorStop(1, color2)
        ctx.fillStyle = gradient
        ctx.fillRect(0, 0, 100, 100)
        const texture = new THREE.CanvasTexture(canvas)
        setBackground(scene, texture)
        return
      }
      if (backgroundId && backgroundId === '4') {
        const canvas = document.createElement('canvas')
        const tempImg = document.createElement('img')
        tempImg.src = 'data:image/png;base64,' + sessionStorage.getItem('customBgImgData')
        setTimeout(() => {
          canvas.width = tempImg.naturalWidth
          canvas.height = tempImg.naturalHeight
          const ctx = canvas.getContext('2d')
          ctx.drawImage(tempImg, 0, 0)

          const texture = new THREE.CanvasTexture(canvas)

          setBackground(scene, texture)
        }, 100)
        return
      }
      if (backgroundId && backgroundId === '5') {
        const texture = new THREE.TextureLoader().load(
          imgArr[Number(sessionStorage.getItem('selectedBgImgId'))].path, t => {
            setBackground(scene, t)
          }
        )
        return
      }
    }

    //= ============default

    if (sel.value === '0') {
      // addContainer.innerHTML = ''
      // setBackground(scene, bgTexture)
      // sessionStorage.setItem('idBackground', sel.value)

      const canvas = document.createElement('canvas')
      canvas.width = 100
      canvas.height = 100
      const ctx = canvas.getContext('2d')
      const gradient = ctx.createLinearGradient(0, 0, 100, 100)
      gradient.addColorStop(0, '#061A03')
      gradient.addColorStop(1, '#061A03')
      ctx.fillStyle = gradient
      ctx.fillRect(0, 0, 100, 100)
      const texture = new THREE.CanvasTexture(canvas)
      setBackground(scene, texture)

      return
    }

    //= ============color picker

    if (sel.value === '1') {
      addContainer.innerHTML = `
      <input type="color">
      `
      const colorPicker = addContainer.querySelector('input')
      colorPicker.value = sessionStorage.getItem('backgroundColor') ?? ''
      colorPicker.addEventListener('input', () => {
        color = colorPicker.value
        sessionStorage.setItem('backgroundColor', color)
        sessionStorage.setItem('idBackground', sel.value)

        const canvas = document.createElement('canvas')
        canvas.width = 100
        canvas.height = 100
        const ctx = canvas.getContext('2d')
        const gradient = ctx.createLinearGradient(0, 0, 100, 100)
        gradient.addColorStop(0, color)
        gradient.addColorStop(1, color)
        ctx.fillStyle = gradient
        ctx.fillRect(0, 0, 100, 100)
        const texture = new THREE.CanvasTexture(canvas)
        setBackground(scene, texture)
      })
    }

    //= ============linear gradient

    if (sel.value === '2') {
      addContainer.innerHTML = `
      <input type="color">
      <input type="color">
      `
      const colorPickers = addContainer.querySelectorAll('input')
      colorPickers[0].value = sessionStorage.getItem('backgroundColor1') ?? ''
      colorPickers[1].value = sessionStorage.getItem('backgroundColor2') ?? ''
      colorPickers.forEach((i, id) => i.addEventListener('input', () => {
        const color1 = colorPickers[0].value
        const color2 = colorPickers[1].value

        sessionStorage.setItem('backgroundColor1', color1)
        sessionStorage.setItem('backgroundColor2', color2)
        sessionStorage.setItem('idBackground', sel.value)

        const canvas = document.createElement('canvas')
        canvas.width = 100
        canvas.height = 100
        const ctx = canvas.getContext('2d')
        const gradient = ctx.createLinearGradient(0, 0, 100, 100)
        gradient.addColorStop(0, color1)
        gradient.addColorStop(1, color2)
        ctx.fillStyle = gradient
        ctx.fillRect(0, 0, 100, 100)
        const texture = new THREE.CanvasTexture(canvas)
        setBackground(scene, texture)
      })
      )
    }

    //= ============radial gradient

    if (sel.value === '3') {
      addContainer.innerHTML = `
      <input type="color">
      <input type="color">
      `
      const colorPickers = addContainer.querySelectorAll('input')
      colorPickers[0].value = sessionStorage.getItem('backgroundColor3') ?? ''
      colorPickers[1].value = sessionStorage.getItem('backgroundColor4') ?? ''

      colorPickers.forEach((i, id) => i.addEventListener('input', () => {
        const color1 = colorPickers[0].value
        const color2 = colorPickers[1].value

        sessionStorage.setItem('backgroundColor3', color1)
        sessionStorage.setItem('backgroundColor4', color2)
        sessionStorage.setItem('idBackground', sel.value)

        const canvas = document.createElement('canvas')
        canvas.width = 100
        canvas.height = 100
        const ctx = canvas.getContext('2d')
        const gradient = ctx.createRadialGradient(50, 50, 25, 50, 50, 50)
        gradient.addColorStop(0, color1)
        gradient.addColorStop(1, color2)
        ctx.fillStyle = gradient
        ctx.fillRect(0, 0, 100, 100)
        const texture = new THREE.CanvasTexture(canvas)
        setBackground(scene, texture)
      })
      )
    }

    //  ===========custom image

    if (sel.value === '4') {
      addContainer.innerHTML = `
      <label>
          <input type="file" class="custom-bg-img-input hide">
          <span class="input text">select image</span>
      </label>
      `
      const input = document.querySelector('.custom-bg-img-input')
      const tempImg = document.createElement('img')
      const canvas = document.createElement('canvas')



      input.onchange = () => readURL(input)

      function readURL (input) {
        input.nextElementSibling.innerText = input.files[0].name.split(".")[0].slice(0, 16)
        sessionStorage.setItem("backgroundCustomName", input.files[0].name.split(".")[0].slice(0, 16))
        if (input.files && input.files[0]) {
          const reader = new FileReader()

          reader.onload = function (e) {
            tempImg.src = e.target.result.toString()
            setTimeout(() => {
              canvas.width = tempImg.naturalWidth
              canvas.height = tempImg.naturalHeight
              const ctx = canvas.getContext('2d')
              ctx.drawImage(tempImg, 0, 0)

              let dataURL = e.target.result.toString()
              dataURL = dataURL.replace(/^data:image\/(png|jpg|jpeg);base64,/, '')

              if (dataURL.length > 2000000) {
                document.querySelector('.warning-img-exceed').classList.remove('hide')
                return
              }

              sessionStorage.setItem('customBgImgData', dataURL)
              sessionStorage.setItem('idBackground', sel.value)

              const texture = new THREE.CanvasTexture(canvas)

              setBackground(scene, texture)
            }, 100)
          }

          reader.readAsDataURL(input.files[0])
        }
      }
    }

    //  ===========select image

    if (sel.value === '5') {
      addContainer.innerHTML = `
      <select class="select-bg-img-input hide"></select>
      <div class="f-select">
          <div class="f-select-container f-select-container__bg-image">
              <div class="f-select-option placeholder"><span>Select image</span></div>
          </div>
      </div>
      `
      document.querySelector('.background-settings-add').style.zIndex = '21'
      const input = document.querySelector('.select-bg-img-input')
      let fakeSelect = document.querySelector('.f-select-container__bg-image')

      imgArr.forEach((i, id) => {
        const option = document.createElement('option')
        option.value = id.toString()
        option.classList.add('text')
        option.innerText = i.name
        input.appendChild(option)

        let fakeOption = document.createElement('div')
        fakeOption.classList.add('f-select-option')
        fakeOption.innerText = i.name
        fakeSelect.appendChild(fakeOption)
      })
      customInput()
      input.addEventListener('change', () => {
        const texture = new THREE.TextureLoader().load(
          imgArr[Number(input.value)].path, t => {
            setBackground(scene, t)
            sessionStorage.setItem('selectedBgImgId', input.value)
            sessionStorage.setItem('idBackground', sel.value)
          }
        )
      })
    }
  }
}
