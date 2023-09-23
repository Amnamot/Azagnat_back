import '../styles/styles.scss'
import slider from './slider';
import { gsap } from 'gsap'

import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader'
import { DRACOLoader } from 'three/examples/jsm/loaders/DRACOLoader.js'

import {
  Text,
} from 'troika-three-text'

import './air-date-picker'
import './user-form'
import { scroll } from './scroll'
import { customInput } from './custom-inputs'
import { changeBodyType } from './change-body-type'
import { changeBodyColor } from './change-body-color'
import { changeBackground } from './change-background'
import { changeTickerColor } from './change-ticker-color'
import { Screenshot } from './screenshot'
import { Warnings } from "./warnings";
import { TokenFs } from "./token-fs";


import {
  EffectComposer,
  EffectPass,
  RenderPass,
  SMAAEffect
} from 'postprocessing'

const wait = {
  hide: function () {
    if (!document.querySelector('#wait')) return 
    document.querySelector('#wait').classList.remove('hide');
    document.querySelector('body').style.overflowY='hidden';
  },
  show: function () {
    if (!document.querySelector('#wait')) return 
    document.querySelector('#wait').classList.add('hide')
    document.querySelector('body').style.overflowY='visible'
  },
  pass: 'smiv',
  Userpass: '',
  waitPass: function () {
    const self = this;
    document.addEventListener('keydown', function (event) {
      if (event.key === 'c') {
        self.Userpass = '';
        return;
      }

      self.Userpass += event.key;
      if (self.Userpass=== self.pass) {
        self.show()
      }

    });
  }
} 


if (window.innerWidth < 1024 || window.innerHeight < 500) {
  document.querySelector('.mobile-thumb').classList.remove('hide')
  document.body.style.overflow = 'hidden'
}


// console.log(navigator.userAgent);
if (
  (navigator.userAgent.search(/Chrome/) > -1 &&
  navigator.userAgent.search(/Chromium/) === -1 &&
  navigator.userAgent.search(/OPR/) === -1 &&
  navigator.userAgent.search(/Edg/) === -1 &&
  navigator.userAgent.search(/MSIE/) === -1 &&
  navigator.userAgent.search(/Trident/) === -1
  )
||
  (navigator.userAgent.search(/Safari/) > -1 &&
  navigator.userAgent.search(/Chromium/) === -1 &&
  navigator.userAgent.search(/Chrome/) === -1)
) {
  console.log('%c OK! ', 'background: #222; color: #bada55');
} else {
  console.log('%c browser not supported! ', 'background: #222; color: red');
  document.querySelector('.mobile-thumb').classList.remove('hide')
  document.body.style.overflow = 'hidden'
}

console.log(window.location.search.replace('?','').split('&').reduce(
  function(p,e){
    var a = e.split('=');
    p[ decodeURIComponent(a[0])] = decodeURIComponent(a[1]);
    return p;
  },
  {}
));

// ==========================request models

let modelsArr

function makeRequestModels (url, cb) {
  let httpRequest = false

  if (window.XMLHttpRequest) {
    httpRequest = new XMLHttpRequest()
    if (httpRequest.overrideMimeType) {
      httpRequest.overrideMimeType('text/json')
    }
  } else if (window.ActiveXObject) {
    try {
      httpRequest = new ActiveXObject('Msxml2.XMLHTTP')
    } catch (e) {
      try {
        httpRequest = new ActiveXObject('Microsoft.XMLHTTP')
      } catch (e) {}
    }
  }

  if (!httpRequest) {
    alert('Failed : ( Unable to instantiate XMLHTTP class')
    return false
  }
  httpRequest.onreadystatechange = function () { alertContents(httpRequest, cb) }
  httpRequest.open('GET', url, true)
  httpRequest.send(null)
}

function alertContents (httpRequest, cb) {
  if (httpRequest.readyState == 4) {
    if (httpRequest.status == 200) {
      const p = new Promise(resolve => {
        modelsArr = JSON.parse(httpRequest.responseText)
        resolve()
      })

      p.then(() => cb())
    } else {
      alert('There was a problem with the request.')
    }
  }
}
function cb () {

  let select = document.querySelector('.body-type')
  let fakeSelect = document.querySelector('.f-select-container__body-type')
  modelsArr.forEach((i, id) => {
    let option = document.createElement('option')
    option.value = id
    option.innerText = i.name
    select.appendChild(option)

    let fakeOption = document.createElement('div')
    fakeOption.classList.add('f-select-option')
    fakeOption.innerText = i.name
    fakeSelect.appendChild(fakeOption)
  })


  changeBodyType()


  load().then(initialize).catch(console.error)
}

makeRequestModels('../data/models.json', cb)

// ==========================request models end

// ==========================request texts
let dataTexts
let ticker_eng
let ticker_rus
(() => {
  const requestURL = '../data/tickers_eng.json'
  const request = new XMLHttpRequest()
  request.open('GET', requestURL)
  request.responseType = 'json'
  request.send()

  request.onload = () => {
    ticker_eng = request.response
  }
})();
(() => {
  const requestURL = '../data/tickers_rus.json'
  const request = new XMLHttpRequest()
  request.open('GET', requestURL)
  request.responseType = 'json'
  request.send()

  request.onload = () => {
    ticker_rus = request.response
  }
})();


// ==========================request texts end

// ==========================request materials

let materialData
(() => {
  const requestURL = '../data/materials.json'
  const request = new XMLHttpRequest()
  request.open('GET', requestURL)
  request.responseType = 'json'
  request.send()

  request.onload = () => {
    materialData = request.response
  }
})()

// ==========================request materials end

//============================images

let images
(() => {
  const requestURL = '../data/images.json'
  const request = new XMLHttpRequest()
  request.open('GET', requestURL)
  request.responseType = 'json'
  request.send()

  request.onload = () => {
    images = request.response
  }
})()

//============================images end

let renderer,
  scene,
  camera

const T = THREE

let ballMode = 'deftext'
let userDataObj = JSON.parse(localStorage.getItem('userObj'))

let userName = userDataObj && userDataObj.name
  ? userDataObj.name
  : 'неопознанный лепрекон'

const switchMode = document.querySelector('.switch-mode')
const switchModeText = switchMode.querySelector('i')
const switchModeArrows = switchMode.querySelectorAll('span')
let switchModeArrowsEnabled = 1

let bd = userDataObj && userDataObj.date
  ? userDataObj.date
  : new Date()
bd = new Date(bd)
let td = new Date()
let bdEnabled = bd.getDate() === td.getDate() && bd.getMonth() === td.getMonth()

switchMode.addEventListener('click', () => {
  if (ballMode === 'deftext') {
    // switchModeText.innerText = 'question mode'
    switchMode.style.background = 'url("https://arweave.net/iaBkLVU5Iw3NE_BRBavWW__TLmb89Mcot7rLQd32vm8") no-repeat center/cover'
    ballMode = "answer"
  } else {
    // switchModeText.innerText = 'wise advice mode'
    switchMode.style.background = 'url("https://arweave.net/IhKJ0AatVeIgLedcQgpOAQ8gosYP1m7kiNFH06bVZwQ") no-repeat center/cover'
    ballMode = 'deftext'
  }
})



const modelsPathId = localStorage.getItem('mId') ?? '0'

const openModal = (modalSelector, buttonSelector) => {
  document.querySelector(buttonSelector).addEventListener('click', () => {
    document.querySelector(modalSelector).classList.contains('hide') && document.querySelector(modalSelector).classList.remove('hide');
  });

  document.querySelector(modalSelector).addEventListener('click', ({ currentTarget }) => {
    if (currentTarget !== document.querySelector(modalSelector)) return;
    document.querySelector(modalSelector).classList.contains('hide') && document.querySelector(modalSelector).classList.add('hide');
  });
}

function load () {
  const assets = new Map()

  const loadingManager = new T.LoadingManager()
  const gltfLoader = new GLTFLoader(loadingManager)
  const dracoLoader = new DRACOLoader()
  dracoLoader.setDecoderPath('../draco/')
  gltfLoader.setDRACOLoader(dracoLoader)

  const textureLoader = new T.TextureLoader(loadingManager)

  return new Promise((resolve, reject) => {
    loadingManager.onError = reject
    loadingManager.onProgress = (item, loaded, total) => {
      document.querySelector('.preloader-element__scale').style.transform = `scaleX(${1 - (loaded / total)})`

      if (loaded === total) {

        resolve(assets)
        const preloader = document.querySelector('.preloader')
        const t1 = gsap.timeline()
          .to(preloader, {
            opacity: 0,
            duration: 1,
            delay: 0.5,
            ease: 'none'
          })
          .to(preloader, {
            display: 'none'
          })

          //удалить стартовую страницу
          wait.hide();
          wait.waitPass();
        
      }
    }

    const modelsPath = []
    modelsArr.forEach(i => modelsPath.push(i['local-path']))

    gltfLoader.load(modelsPath[Number(modelsPathId)], g => assets.set('ball', g.scene))

    const gradient1 = textureLoader.load('./img/beautiful_13.jpg')

    const envMapJpg = textureLoader.load('./img/old_hall_1k.jpg', texture => {
      texture.mapping = THREE.EquirectangularReflectionMapping
    })

    loadingManager.onLoad = () => {
      assets.set('gradient1', gradient1)
      assets.set('envMap', envMapJpg)

      const es = document.querySelectorAll('input[type="range"].slider-progress')
      setTimeout(() => es.forEach(e => e.style.setProperty('--value', e.value)))
      customInput()
    }

    const searchImage = new Image(); const areaImage = new Image()

    searchImage.addEventListener('load', function () {
      assets.set('smaa-search', this)
      loadingManager.itemEnd('smaa-search')
    })

    areaImage.addEventListener('load', function () {
      assets.set('smaa-area', this)
      loadingManager.itemEnd('smaa-area')
    })

    loadingManager.itemStart('smaa-search')
    loadingManager.itemStart('smaa-area')

    searchImage.src = SMAAEffect.searchImageDataURL
    areaImage.src = SMAAEffect.areaImageDataURL
  })
}

function initialize (assets) {
  const container3d = document.querySelector('.container3d')
  const width = container3d.clientWidth
  const height = container3d.clientHeight
  const aspect = width / height

  const clock = new T.Clock();

  // (container3d.getBoundingClientRect().height < document.querySelector('.menu-container').getBoundingClientRect().height) ||
  // window.innerWidth < 1024 ? scroll() : ''

  scroll()

  // console.log(container3d.getBoundingClientRect().height)
  // console.log(document.querySelector('.menu').getBoundingClientRect().height)

  renderer = new T.WebGLRenderer({
    powerPreference: 'high-performance',
    antialias: false,
    stencil: false,
    depth: false,
    preserveDrawingBuffer: true
  })
  renderer.setSize(width, height)
  renderer.setClearColor(0xf0f0f0)
  window.innerWidth <= 1920 ? renderer.setPixelRatio(Math.min(2, window.devicePixelRatio)) : ''

  const desktop = document.documentElement.clientWidth > 767

  container3d.appendChild(renderer.domElement)


  scene = new T.Scene()
  scene.environment = assets.get('envMap')

  let bgTexture = assets.get('gradient1')

  const canvasAspect = container3d.clientWidth / container3d.clientHeight
  const imageAspect = bgTexture.image ? bgTexture.image.width / bgTexture.image.height : 1
  const aspectBg = imageAspect / canvasAspect

  bgTexture.offset.x = aspectBg > 1 ? (1 - 1 / aspectBg) / 2 : 0
  bgTexture.repeat.x = aspectBg > 1 ? 1 / aspectBg : 1

  bgTexture.offset.y = aspectBg > 1 ? 0 : (1 - aspectBg) / 2
  bgTexture.repeat.y = aspectBg > 1 ? 1 : aspectBg;

  (() => {
    const canvas = document.createElement('canvas')
    canvas.width = 100
    canvas.height = 100
    const ctx = canvas.getContext('2d')
    const gradient = ctx.createLinearGradient(0, 0, 100, 100)
    gradient.addColorStop(0, '#061A03')
    gradient.addColorStop(1, '#061A03')
    ctx.fillStyle = gradient
    ctx.fillRect(0, 0, 100, 100)
    bgTexture = new THREE.CanvasTexture(canvas)
  })()

  scene.background = bgTexture
  let fov
  function setCameraAspect () {
    const initFov = 30
    const aspectC = (container3d.clientWidth / container3d.clientHeight)
    fov = (initFov / aspectC) + ((container3d.clientWidth / container3d.clientHeight) * 10)
  }
  setCameraAspect()

  camera = new T.PerspectiveCamera(
    fov,
    aspect,
    1,
    300
  )
  camera.lookAt(scene.position)
  camera.position.set(
    47,
    -64,
    126
  ) // 47 -64 126

  let controls = new OrbitControls(camera, renderer.domElement)
  controls.enableDamping = false
  controls.enablePan = false
  controls.enableZoom = false
  controls.minDistance = 50
  controls.maxDistance = 300
  // controls.rotateSpeed = 2;

  // ---------------------------------------------------------------------------------meshes-------------------------//

  const root = assets.get('ball').children[0]
  scene.add(root)
  root.rotation.set(
    Math.PI / 2,
    0,
    0
  )

  const ball = root.getObjectByName('Ball')
  const screen = root.getObjectByName('Screen')
  const glass = root.getObjectByName('Glass')
  const ring = root.getObjectByName('Border') ?? root.getObjectByName('Border001')
  const videoFrame = root.getObjectByName('Video')

  const hat = root.getObjectByName('Hat') ?? null
  
  fetch('/data/add-materials.json')
  .then(r => r.json())
  .then(json => {
    hat? console.log(json[0].metalness) : ''
    hat ? hat.material = new T.MeshStandardMaterial({
      color : json[0].color,
      metalness: json[0].metalness,
      roughness: json[0].roughness,
      roughnessMap  : new T.TextureLoader().load(json[0].roughnessMap),
      map : new T.TextureLoader().load(json[0].map),
      normalMap : new T.TextureLoader().load(json[0].normalMap),
      displacementMap   : new T.TextureLoader().load(json[0].displacementMap),
      displacementScale : json[0].displacementScale,
      envMapIntensity : json[0].envMapIntensity
    }) : ''
  })
    .catch(console.error)
  
  root.remove(glass)
  // root.remove(screen)

  const screenColor = 0xd2e8d4
  const tickerInitColor = '#004f20'

  //= ===================ball shader

  const bodyColor = 0x1C1C1C

  const bodySettings = {
    metalness: 0,
    roughness: 0.1
  }

  ball.material = new T.MeshPhysicalMaterial({
    emissiveIntensity: 0,
    metalness: bodySettings.metalness,
    roughness: bodySettings.roughness,
    color: bodyColor,
    side: T.DoubleSide,
    envMapIntensity: 1.5
  })

  ball.material.needsUpdate

  //= ===================ball shader end

  ring.material = new T.MeshStandardMaterial({
    emissiveIntensity: 0,
    metalness: 0.5,
    roughness: 0,
    envMapIntensity: 2,
    color: 0x7E7E7E
  })

  // glass.material = new T.MeshPhysicalMaterial({
  //   color: 0x232323,
  //   transparent: true,
  //   opacity: 1,
  //   roughness: 0,
  //   metalness: 0,
  //   clearcoat: 1,
  //   transmission: 1,
  //   clearcoatRoughness: 0,
  //   // wireframe: true
  //   blending: T.AdditiveBlending
  // })

  screen.material = new T.MeshBasicMaterial({
    color: screenColor
  })

  // ---------------------------------------------------------------------------------interactions-------------------//
  let t1
  function initT1 () {
    t1 = gsap.timeline({
      paused: true
    })

    t1.to(root.position, {
      y: '+=2',
      yoyo: true,
      repeat: -1,
      duration: 2.3,
      ease: 'sine.inOut',
      overwrite: 'auto'
    })
    t1.to(root.position, {
      x: '+=2',
      yoyo: true,
      repeat: -1,
      duration: 4.2,
      ease: 'sine.inOut',
      overwrite: 'auto'
    }, '<')
    t1.to(root.rotation, {
      y: `+=${T.MathUtils.degToRad(10)}`,
      yoyo: true,
      repeat: -1,
      duration: 3,
      ease: 'sine.inOut',
      overwrite: 'auto'
    }, '<')
    t1.to(root.rotation, {
      x: `+=${T.MathUtils.degToRad(3)}`,
      yoyo: true,
      repeat: -1,
      duration: 3.5,
      ease: 'sine.inOut',
      overwrite: 'auto'
    }, '<')
    t1.to(root.rotation, {
      z: `+=${T.MathUtils.degToRad(13)}`,
      yoyo: true,
      repeat: -1,
      duration: 15,
      ease: 'sine.inOut',
      overwrite: 'auto'
    }, '<')
    t1.play()
  }

  let t2

  initT1()

  let MAEnabled = 0

  function mainAnimation () {
    t1 ? t1.kill() : ''

    const mainTl = gsap.timeline({
      onStart: () => {
        window.removeEventListener('mouseup', mouseUpHandler)
        window.removeEventListener('touchend', mouseUpHandler)
        controls.enabled ? controls.enabled = false : ''
      },
      onComplete: () => {
        addText()
      }
    })
    mainTl.to(camera.position, {
      x: 0,
      y: 0,
      z: desktop ? 65 : 80,
      duration: 1,
      overwrite: 'auto'
    })
    mainTl.to(root.position, {
      x: 0,
      z: 0,
      y: 0,
      overwrite: 'auto'
    }, '<')
    mainTl.to(root.rotation, {
      x: Math.PI / 2,
      z: 0,
      y: 0,
      overwrite: 'auto'
    }, '<')
  }

  //= ========================screen

  function randomInteger (min, max) {
    const rand = min - 0.5 + Math.random() * (max - min + 1)
    return Math.round(rand)
  }

  const videoSources = [
    './flaticon/1.mp4',
    './flaticon/2.mp4',
    './flaticon/3.mp4',
    './flaticon/4.mp4',
    './flaticon/5.mp4',
    './flaticon/6.mp4',
    './flaticon/7.mp4',
    './flaticon/8.mp4',
    './flaticon/9.mp4'
  ]

  const videoEl = document.createElement('video')

  videoEl.setAttribute('playsinline', 'playsinline')
  videoEl.defaultMuted = true
  videoEl.autoplay = true
  videoEl.loop = true
  videoEl.src = videoSources[0]
  const videoTexture = new THREE.VideoTexture(videoEl)
  videoTexture.minFilter = THREE.LinearFilter
  videoTexture.magFilter = THREE.LinearFilter
  videoTexture.format = THREE.RGBFormat
  videoTexture.anisotropy = renderer.capabilities.getMaxAnisotropy()

  videoFrame.material = new T.MeshBasicMaterial({
    transparent: true,
    opacity: 0,
    map: videoTexture,
    color: screenColor
  })
  videoFrame.material.needsUpdate

  function addVideo () {
    if (!MAEnabled) {
      const p1 = new Promise(resolve => {
        gsap.to(videoFrame.material, {
          onComplete: () => {
            videoEl.src = videoSources[randomInteger(0, videoSources.length - 1)]
            setTimeout(resolve, 100)
          },
          opacity: 0,
          duration: 1,
          ease: 'none',
          overwrite: 'auto'
        })
      })

      p1.then(() => {
        gsap.to(videoFrame.material, {
          opacity: 1,
          duration: 1,
          ease: 'none',
          overwrite: 'auto'
        })

        videoFrame.material.needsUpdate

        setTimeout(addVideo, 3000)
      })
    }
  }
  addVideo()

  const textConfig = {
    color: tickerInitColor
  }
  function addText () {
    userDataObj = JSON.parse(localStorage.getItem('userObj'))

    userName = userDataObj && userDataObj.name
      ? userDataObj.name
      : 'неопознанный лепрекон'

    bd = userDataObj && userDataObj.date
      ? userDataObj.date
      : null
    bd = new Date(bd)
    td = new Date()
    bdEnabled = bd.getDate() === td.getDate() && bd.getMonth() === td.getMonth()

    gsap.to(videoFrame.material, {
      opacity: 0,
      duration: 1,
      overwrite: 'auto'
    })

    const myText = new Text()
    root.add(myText)

    dataTexts = userDataObj && userDataObj.language === '1' ? ticker_rus : ticker_eng
    document.querySelector('.lang').addEventListener('change', e => {
      dataTexts = e.target.value === '1' ? ticker_rus : ticker_eng
    })


    let text = ballMode === 'deftext'
      ? dataTexts[0].texts[randomInteger(0, dataTexts[0].texts.length - 1)]
      : dataTexts[1].texts[randomInteger(0, dataTexts[1].texts.length - 1)]

    if (bdEnabled && ballMode === 'deftext') {
      const percent = randomInteger(1, 10)
      percent <= 7 ? text = dataTexts[2].texts[randomInteger(0, dataTexts[2].texts.length - 1)] : ''
    }

    text = text.replace('#name#', userName)

    // Set properties to configure:
    myText.font = './fonts/pangolin-v11-latin_cyrillic-regular.woff'
    myText.text = text
    myText.fontSize = 5
    myText.position.z = 0
    myText.position.y = 0
    myText.anchorX = '-10%'
    myText.anchorY = 'middle'
    myText.textAlign = 'center'

    myText.clipRect = modelsPathId === '4' ? [-11, -10, 11, 10] : [-14, -10, 14, 10]
    myText.textIndent = 15
    myText.curveRadius = modelsPathId === '0'
      ? -26.5
      : modelsPathId === '1'
        ? -30
        : modelsPathId === '2'
          ? -60
          : modelsPathId === '3'
            ? -30
            : modelsPathId === '4' ? -30 : ''

    const textTL = gsap.timeline({
      onComplete: () => {
        setTimeout(addVideo, 1200)
        root.remove(myText)
        myText.dispose()
        const t10 = gsap.timeline({
          onComplete: () => {
            // desktop ? controls.reset() : ''
            // !controls.enabled ? controls.enabled = true : ''
            controls.reset()
            controls = new OrbitControls(camera, renderer.domElement)
            controls.enablePan = false
            controls.enableZoom = false
            controls.minDistance = 50
            controls.maxDistance = 300
            controls.addEventListener('change', controlOnChange)
            MAEnabled = 0
            setTimeout(initT1, 100)
          }
        })
        t10.to(root.rotation, {
          x: Math.PI / 2,
          z: 0,
          y: 0,
          duration: 1,
          overwrite: 'auto'
        })
        t10.to(camera.position, {
          x: 47,
          y: -64,
          z: 126,
          duration: 1,
          overwrite: 'auto'
        }, '<')
      }
    })
    textTL.to(myText, {
      anchorX: `${100 + ((14 / text.length).toFixed(3) * 100)}%`,
      duration: ((text.length + 15) / 10).toFixed(3),
      ease: 'none',
      overwrite: 'auto'
    })

    myText.material = new T.MeshBasicMaterial({
      transparent: true,
      opacity: 1,
      color: textConfig.color
    })

    myText.rotation.set(
      T.MathUtils.degToRad(-90),
      T.MathUtils.degToRad(0),
      T.MathUtils.degToRad(0)
    )

    myText.position.y = 31
  }

  //= ========================screen end

  let returnAnimation = 0

  function mouseUpHandler () {
    if (returnAnimation) return
    t2 = gsap.timeline({
      onStart: () => {
        window.removeEventListener('mouseup', mouseUpHandler)
        window.removeEventListener('touchend', mouseUpHandler)
        returnAnimation = 1
        controls.enabled ? controls.enabled = false : ''
      },
      onComplete: () => {
        !controls.enabled ? controls.enabled = true : ''
        returnAnimation = 0
        setTimeout(initT1, 100)
      }
    })
    t2.to(root.position, {
      x: 0,
      y: 0,
      z: 0,
      duration: 1,
      ease: 'power2.inOut',
      overwrite: 'auto'
    })
    t2.to(root.rotation, {
      x: Math.PI / 2,
      y: 0,
      z: 0
    })
    t2.to(camera.position, {
      x: 47,
      y: -64,
      z: 126,
      duration: 1,
      ease: 'power2.inOut',
      overwrite: 'auto'
    }, '<')
  }

  function controlOnChange () {
    t1 ? t1.kill() : ''

    !MAEnabled && !returnAnimation ? window.addEventListener('mouseup', mouseUpHandler) : ''
    !MAEnabled && !returnAnimation ? window.addEventListener('touchend', mouseUpHandler) : ''
  }

  controls.addEventListener('change', controlOnChange)

  // ++++++++++++++++++++++++postprocessing
  const composer = new EffectComposer(
    renderer, {
      frameBufferType: T.HalfFloatType
    }
  )

  const smaaEffect = new SMAAEffect(
    assets.get('smaa-search'),
    assets.get('smaa-area')
  )

  const renderPass = new RenderPass(scene, camera)
  const smaaPass = new EffectPass(camera, smaaEffect)
  const effectPass = new EffectPass(
    camera
  )

  effectPass.renderToScreen = true

  composer.addPass(renderPass)
  composer.addPass(smaaPass)
  composer.addPass(effectPass)


  window.addEventListener('resize', (function () {
    let id = 0

    function handleResize () {
      const width = container3d.clientWidth
      const height = container3d.clientHeight

      camera.aspect = width / height
      camera.updateProjectionMatrix()
      composer.setSize(width, height)

      setCameraAspect()
      camera.fov = fov

      const canvasAspect = container3d.clientWidth / container3d.clientHeight
      const imageAspect = scene.background.image ? scene.background.image.width / scene.background.image.height : 1
      const aspectBg = imageAspect / canvasAspect

      scene.background.offset.x = aspectBg > 1 ? (1 - 1 / aspectBg) / 2 : 0
      scene.background.repeat.x = aspectBg > 1 ? 1 / aspectBg : 1

      scene.background.offset.y = aspectBg > 1 ? 0 : (1 - aspectBg) / 2
      scene.background.repeat.y = aspectBg > 1 ? 1 : aspectBg

      scroll()
      TokenFs()

      id = 0
    }

    return function onResize (event) {
      if (id === 0) {
        id = setTimeout(handleResize, 66, event)
      }
    }
  })())

  changeBodyColor(ball.material, bodySettings, materialData, customInput, images)
  changeBackground(scene, bgTexture, customInput, images)
  changeTickerColor(textConfig, tickerInitColor)

  Screenshot(renderer.domElement, composer, camera, bgTexture, scene, renderer)
  Warnings()


  let cl = controls.getAzimuthalAngle()
  let counter = 0
  let trueCounter = 0
  let distCam = camera.position.x
  let cls = 0

  ball.material.needsUpdate

  function render () {
    cls = controls.getAzimuthalAngle() - cl;
    (cls > 0.1 || cls < -0.1) ? trueCounter++ : ''
    cl = controls.getAzimuthalAngle()

    counter++
    if (counter === 30) { // 100
      counter = 0
      distCam = 0
      const criticalNumber = desktop ? 22 : 18
      if (trueCounter > criticalNumber && !MAEnabled) { // 50
        mainAnimation()
        MAEnabled = 1
      }
      trueCounter = 0
    }

    controls.update()

    requestAnimationFrame(render)
    composer.render(clock.getDelta())
  }
  render()

  const fullscreen = document.querySelector('.full-screen')
  const ftl = gsap.timeline({
    paused: true
  })
    .to(['.menu', '.main-description', '.instructions', '.mint', '.referral', '.footer'], {
      y: 50,
      opacity: 0,
      duration: 1,
      ease: "power2.inOut"
    })
    .to('.container3d', {
      onUpdate: () => {
        const width = container3d.clientWidth
        const height = container3d.clientHeight

        camera.aspect = width / height
        camera.updateProjectionMatrix()
        // globalUniforms.aspect.value = camera.aspect;
        composer.setSize(width, height)

        setCameraAspect()
        camera.fov = fov
        camera.updateProjectionMatrix()

        const canvasAspect = container3d.clientWidth / container3d.clientHeight
        const imageAspect = scene.background.image ? scene.background.image.width / scene.background.image.height : 1
        const aspectBg = imageAspect / canvasAspect

        scene.background.offset.x = aspectBg > 1 ? (1 - 1 / aspectBg) / 2 : 0
        scene.background.repeat.x = aspectBg > 1 ? 1 / aspectBg : 1

        scene.background.offset.y = aspectBg > 1 ? 0 : (1 - aspectBg) / 2
        scene.background.repeat.y = aspectBg > 1 ? 1 : aspectBg
      },
      onComplete: () => {
        fullscreen.style.background = `url("https://arweave.net/GxxozpkT684Ye5OGL4oaKU6TZ7vZxnyKUC68bRR3i5c") no-repeat center/cover`
      },
      onReverseComplete: () => {
        fullscreen.style.background = `url("https://arweave.net/r1xZBYdXC7aarwtqqbgl6eAuVjsHs6TTyQmBsh9ne4Y") no-repeat center/cover`
      },
      width: `${window.innerWidth - 80}px`,
      height: '80vh',
      left: '40px',
      duration: 1
    })


  let direction = 1

  fullscreen.addEventListener('click', () => {
    // if (desktop) {
    direction === 1 ? ftl.play() : ftl.reverse()
    direction === 1 ? direction = 0 : direction = 1
    // }
  })

  TokenFs()

  // openModal('.warning-RoadMap', '#RoadMap');
  slider();


  const timer = {
    date: (new Date(1672002000000)), //UTC+0 25 в 21:00 это 26 число по москве 
    start: function () {
      const self = this;
      const mint = document.querySelector('#mint_start');
      self.setTimeToSelector(mint)

      setTimeout(() => {
        self.setTimeToSelector(mint)
      }, 1000);
    },
    timeToString: function (day = 0, hour = 0, min = 0) {
      return `Mint through: ${day} day ${hour} h. ${min} min.`;
    },
    setTimeToSelector: function(mint) {
      let timeMintStart = this.date - (new Date());
      if (!mint) {

        return false;
      }

      if (timeMintStart <= 0) {
        mint.value = 'Mint';
        return;
      }
      
      let sec = Math.trunc(timeMintStart/1000);
      let min = (sec/60) % 60;
      let hours = ((sec/60)/60) % 60;
      let days = ((sec/60)/60/24) % 60;
      mint.value = this.timeToString(Math.trunc(days), Math.trunc(hours), Math.trunc(min));
    }
  };

  timer.start();

  // let iframe = document.querySelector('iframe.mobile-thumb-example-container__item');
  // iframe.contentWindow.document.querySelector('.full-screen').addEventListener('click', () => {
  //   if (iframe.classList.contains('iframeFullScreen')) {
  //     iframe.classList.remove('iframeFullScreen');
  //   } else {
  //     iframe.classList.add('iframeFullScreen');
  //   }
  // });
}
