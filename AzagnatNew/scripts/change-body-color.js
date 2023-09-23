import * as THREE from 'three'

const sel = document.querySelector('.body-color')
// const options = document.querySelectorAll('.body-color option')

const fakeSelPlaceholder = document.querySelector('.f-select-container__body-color .placeholder')
const es = document.querySelectorAll('input[type="range"].slider-progress')

const metallnesInput = document.querySelector('.metalness')
const roughnessInput = document.querySelector('.roughness')

export function changeBodyColor (material, bodySettings, materialData, customInput, images) {

  let imgArr = images[0].bodyImages

  //  =========================change material settings

  material.metalness = sessionStorage.getItem('metalness') ?? bodySettings.metalness
  material.roughness = sessionStorage.getItem('roughness') ?? bodySettings.roughness
  material.needsUpdate = true

  metallnesInput.value = material.metalness
  roughnessInput.value = material.roughness

  metallnesInput.addEventListener('input', () => {
    material.metalness = Number(metallnesInput.value)
    material.needsUpdate = true
    sessionStorage.setItem('metalness', metallnesInput.value)
  })
  roughnessInput.addEventListener('input', () => {
    material.roughness = Number(roughnessInput.value)
    material.needsUpdate = true
    sessionStorage.setItem('roughness', roughnessInput.value)
  })

  //  =========================change material settings end

  let color = 0x1C1C1C
  const addContainer = document.querySelector('.body-color-add')
  const options = sel.querySelectorAll('option')


  selChangeHandler(1)

  sel.addEventListener('change', selChangeHandler)

  function selChangeHandler (load) {
    sessionStorage.setItem("idBody", sel.value)
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

      const materialId = sessionStorage.getItem('idBodyColor')
      if (materialId && materialId === '0') {
        addContainer.innerHTML = ''
        color = 0x1C1C1C
        material.color.set(color)
        material.map = null
        material.needsUpdate = true
        return
      }
      if (materialId && materialId === '1') {
        addContainer.innerHTML = `
      <input type="color">
      `
        const colorPicker = addContainer.querySelector('input')
        colorPicker.value = sessionStorage.getItem('customBodyColor') ?? '#1C1C1C'
        color = colorPicker.value
        colorPicker.addEventListener('input', setColor)
        material.color.set(color)
        function setColor () {
          color = colorPicker.value
          material.color.set(color)
          material.map = null
          material.normalMap = null
          material.roughnessMap = null
          material.needsUpdate = true
          metallnesInput.value = material.metalness
          roughnessInput.value = material.roughness
          sessionStorage.setItem('customBodyColor', color)
        }
        material.map = null
        material.needsUpdate = true
        options[1].setAttribute('selected', 'selected')
        fakeSelPlaceholder.innerText = options[1].innerText
        return
      }
      if (materialId && materialId === '2') {
        const canvas = document.createElement('canvas')
        const tempImg = document.createElement('img')
        tempImg.src = 'data:image/png;base64,' + sessionStorage.getItem('customImgData')
        setTimeout(() => {
          canvas.width = tempImg.naturalWidth
          canvas.height = tempImg.naturalHeight
          const ctx = canvas.getContext('2d')
          ctx.drawImage(tempImg, 0, 0)

          const texture = new THREE.CanvasTexture(canvas)
          texture.wrapS = texture.wrapT = THREE.RepeatWrapping

          material.color.set(0xffffff)
          material.map = texture
          material.needsUpdate = true
        }, 100)
        return
      }
      if (materialId && materialId === '3') {
        fakeSelPlaceholder.innerHTML = `<span>Select view</span>`
        const texture = new THREE.TextureLoader().load(
          imgArr[Number(sessionStorage.getItem('selectedImgId'))].path, t => {
            material.color.set(0xffffff)
            t.wrapS = t.wrapT = THREE.RepeatWrapping
            material.map = t
            material.needsUpdate = true
          }
        )
        return
      }
      if (materialId && materialId === '4') {
        fakeSelPlaceholder.innerHTML = `<span>Select view</span>`
        let id = Number(sessionStorage.getItem('selectedMaterialId'))
        !materialData[id] ? id = 0 : '';

        const textureLoader = new THREE.TextureLoader()

        const map = textureLoader.loadAsync(materialData[id].map)
        const normal = textureLoader.loadAsync(materialData[id].normalMap)
        const roughness = textureLoader.loadAsync(materialData[id].roughnessMap)
        const dispPath = materialData[id].displacementMap ?? null
        const displacement = dispPath? textureLoader.loadAsync(dispPath) : new Promise(resolve => resolve(null))

        Promise.allSettled([map, normal, roughness, displacement])
          .then(([m, n, r, d]) => {
            m = m.status === "fulfilled" ? m.value : null
            n = n.status === "fulfilled" ? n.value : null
            r = r.status === "fulfilled" ? r.value : null
            d = d.status === "fulfilled" ? d.value : null

            m ? m.wrapS = m.wrapT = THREE.RepeatWrapping : ''
            n ? n.wrapS = n.wrapT = THREE.RepeatWrapping : ''
            r ? r.wrapS = r.wrapT = THREE.RepeatWrapping : ''
            d ? d.wrapS = d.wrapT = THREE.RepeatWrapping : ''
            material.color.set(0xffffff)
            material.map = m
            material.normalMap = n
            material.roughnessMap = r
            material.displacementMap = d
            material.displacementScale = materialData[id].displacementScale ?? 1
            material.displacementBias = Number(materialData[id].displacementBias) ?? 0
            material.metalness = sessionStorage.getItem('metalness') ?? materialData[id].metalness
            material.needsUpdate = true
            metallnesInput.value = material.metalness
            roughnessInput.value = material.roughness
          })
          .catch(console.error)

        return
      }
    }
    //= ============default

    if (sel.value === '0') {
      addContainer.innerHTML = ''
      color = 0x1C1C1C
      material.color.set(color)
      material.map = null
      material.normalMap = null
      material.roughnessMap = null
      material.metalness = bodySettings.metalness
      material.roughness = bodySettings.roughness
      material.needsUpdate = true
      metallnesInput.value = material.metalness
      roughnessInput.value = material.roughness
      sessionStorage.setItem('idBodyColor', sel.value)
      sessionStorage.setItem('metalness', metallnesInput.value)
      sessionStorage.setItem('roughness', roughnessInput.value)
    }

    //= ============color picker

    if (sel.value === '1') {
      addContainer.innerHTML = `
      <input type="color">
      `
      const colorPicker = addContainer.querySelector('input')
      colorPicker.value = sessionStorage.getItem('customBodyColor') ?? '#1C1C1C'
      color = colorPicker.value
      material.color.set(color)
      material.map = null
      material.normalMap = null
      material.roughnessMap = null
      material.needsUpdate = true
      colorPicker.addEventListener('input', setColor)
      function setColor () {
        color = colorPicker.value
        material.color.set(color)
        material.map = null
        material.normalMap = null
        material.roughnessMap = null
        material.needsUpdate = true
        metallnesInput.value = material.metalness
        roughnessInput.value = material.roughness
        sessionStorage.setItem('customBodyColor', color)
      }
      sessionStorage.setItem('idBodyColor', sel.value)
    }

    //  ===========custom image

    if (sel.value === '2') {
      // sessionStorage.setItem('idBodyColor', sel.value)
      addContainer.innerHTML = `
       <label>
          <input type="file" value="Select image" class="custom-img-input hide">
          <span class="input text">select image</span>
      </label>
      `
      const input = document.querySelector('.custom-img-input')
      const tempImg = document.createElement('img')
      const canvas = document.createElement('canvas')

      input.onchange = () => readURL(input)

      function readURL (input) {
        input.nextElementSibling.innerText = input.files[0].name.split(".")[0].slice(0, 16)
        sessionStorage.setItem("bodyCustomName", input.files[0].name.split(".")[0].slice(0, 16))
        if (input.files && input.files[0]) {
          const reader = new FileReader()

          reader.onload = function (e) {
            tempImg.src = e.target.result
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

              sessionStorage.setItem('customImgData', dataURL)
              sessionStorage.setItem('idBodyColor', sel.value)

              const texture = new THREE.CanvasTexture(canvas)
              texture.wrapS = texture.wrapT = THREE.RepeatWrapping
              material.normalMap = null
              material.roughnessMap = null
              material.color.set(0xffffff)
              material.map = texture
              material.needsUpdate = true
              metallnesInput.value = material.metalness
              roughnessInput.value = material.roughness
            }, 100)
          }

          reader.readAsDataURL(input.files[0])
        }
      }
    }

    //  ===========select image

    if (sel.value === '3') {
      // sessionStorage.setItem('idBodyColor', sel.value)
      addContainer.innerHTML = `
      <select class="select-img-input  hide"></select>
      <div class="f-select">
          <div class="f-select-container f-select-container__body-image">
              <div class="f-select-option placeholder"><span>Select image</span></div>
          </div>
      </div>
      `
      const input = document.querySelector('.select-img-input')
      let fakeSelect = document.querySelector('.f-select-container__body-image')

      document.querySelector('.body-color-add').style.zIndex = '27'

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
            material.color.set(0xffffff)
            t.wrapS = t.wrapT = THREE.RepeatWrapping
            material.map = t
            material.color.set(0xffffff)
            material.normalMap = null
            material.roughnessMap = null
            material.needsUpdate = true
            metallnesInput.value = material.metalness
            roughnessInput.value = material.roughness
            sessionStorage.setItem('selectedImgId', input.value)
            sessionStorage.setItem('idBodyColor', sel.value)
          }
        )
      })
    }

    //  ===========select material

    if (sel.value === '4') {
      // sessionStorage.setItem('idBodyColor', sel.value)
      addContainer.innerHTML = `
      <select class="select-material-input  text hide"></select>
      <div class="f-select">
          <div class="f-select-container f-select-container__material">
              <div class="f-select-option placeholder"><span>Select material</span></div>
          </div>
      </div>
      `
      const input = document.querySelector('.select-material-input')
      let fakeSelect = document.querySelector('.f-select-container__material')

      document.querySelector('.body-color-add').style.zIndex = '27'

      materialData.forEach((i, id) => {
        const option = document.createElement('option')
        option.value = id.toString()
        option.classList.add('text')
        option.innerText = materialData[id].name
        input.appendChild(option)

        let fakeOption = document.createElement('div')
        fakeOption.classList.add('f-select-option')
        fakeOption.innerText = i.name
        fakeSelect.appendChild(fakeOption)
      })
      customInput()
      input.addEventListener('change', () => {
        let data = {}; 
        data['model'] = localStorage.getItem('mId'); 
        for(let i = 0; i < sessionStorage.length; i++) {
            let key = sessionStorage.key(i);
            data[key] = sessionStorage.getItem(key);
        }
        data["selectedMaterialId"] = input.value
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
        
        const id = Number(input.value)

        const textureLoader = new THREE.TextureLoader()

        const map = textureLoader.loadAsync(materialData[id].map)
        const normal = textureLoader.loadAsync(materialData[id].normalMap)
        const roughness = textureLoader.loadAsync(materialData[id].roughnessMap)
        const dispPath = materialData[id].displacementMap ?? null
        const displacement = dispPath? textureLoader.loadAsync(dispPath) : new Promise(resolve => resolve(null))

        Promise.allSettled([map, normal, roughness, displacement])
          .then(([m, n, r, d]) => {

            m = m.status === "fulfilled" ? m.value : null
            n = n.status === "fulfilled" ? n.value : null
            r = r.status === "fulfilled" ? r.value : null
            d = d.status === "fulfilled" ? d.value : null

            m ? m.wrapS = m.wrapT = THREE.RepeatWrapping : ''
            n ? n.wrapS = n.wrapT = THREE.RepeatWrapping : ''
            r ? r.wrapS = r.wrapT = THREE.RepeatWrapping : ''
            d ? d.wrapS = d.wrapT = THREE.RepeatWrapping : ''

            material.color.set(0xffffff)
            material.map = m
            material.normalMap = n
            material.roughnessMap = r
            material.displacementMap = d
            material.displacementScale = materialData[id].displacementScale ?? 1
            material.displacementBias = Number(materialData[id].displacementBias) ?? 0
            material.metalness = sessionStorage.getItem('metalness') ?? materialData[id].metalness
            material.needsUpdate = true
            metallnesInput.value = material.metalness
            roughnessInput.value = material.roughness
            sessionStorage.setItem('selectedMaterialId', input.value)
            sessionStorage.setItem('idBodyColor', sel.value)
            sessionStorage.setItem('metalness', metallnesInput.value)
            sessionStorage.setItem('roughness', roughnessInput.value)
            es.forEach(e => e.style.setProperty('--value', e.value))
          })
          .catch(console.error)
      })
    }
  }
}
