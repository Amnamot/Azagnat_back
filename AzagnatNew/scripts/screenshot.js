import html2canvas from 'html2canvas';
import {TokenFs} from "./token-fs";

let screenTarget = document.querySelector('.container3d')
let warningMintButton = document.querySelector('.warning-mint .warning__button')
const checksInfo = document.querySelectorAll('.warning-mint .warning__info input');
let warningMintImg = document.querySelector('.warning-mint img')
let warningMint = document.querySelector('.warning-mint')
let switchMode = document.querySelector('.switch-mode')
let fullScreen = document.querySelector('.full-screen')
let avatar = document.querySelector('.avatar')

export function Screenshot (canvas, composer, camera, bgTexture, scene, renderer) {
  document.querySelector('.mint__submit').addEventListener('click', () => {
    if (null == localStorage.getItem("userObj") || 5 > Object.keys(JSON.parse(localStorage.getItem("userObj"))).length) {
      document.querySelector(".warning-req-param").classList.remove("hide");
      return;
    }
    screenTarget.style.width = '512px'
    screenTarget.style.height = '512px'
    screenTarget.style.borderRadius = '0'
    screenTarget.style.border = 'none'
    screenTarget.style.minHeight = 'unset'
    switchMode.style.background = ' url("./img/question.png") no-repeat center/cover'
    fullScreen.style.background = ' url("./img/flower.png") no-repeat center/cover'

    bgTexture = scene.background
    const canvasAspect = screenTarget.clientWidth / screenTarget.clientHeight
    const imageAspect = bgTexture.image ? bgTexture.image.width / bgTexture.image.height : 1
    const aspectBg = imageAspect / canvasAspect

    bgTexture.offset.x = aspectBg > 1 ? (1 - 1 / aspectBg) / 2 : 0
    bgTexture.repeat.x = aspectBg > 1 ? 1 / aspectBg : 1

    bgTexture.offset.y = aspectBg > 1 ? 0 : (1 - aspectBg) / 2
    bgTexture.repeat.y = aspectBg > 1 ? 1 : aspectBg

    scene.background = bgTexture

    camera.aspect = 1
    let initialFov = camera.fov
    camera.fov -= 17
    camera.updateProjectionMatrix()
    composer.setSize(512, 512)
    renderer.setPixelRatio(2)
    renderer.antialias = true
    setTimeout(() => {
      TokenFs()
      html2canvas(screenTarget, {
          scale: 1
      }).then(function (canvas) {

        const dataURL = canvas.toDataURL()
        setTimeout(() =>{

            warningMintImg.src = dataURL
            warningMint.classList.remove('hide')
            document.body.style.overflow = 'hidden'
            sessionStorage.setItem('screenshot', dataURL.replace(/^data:image\/(png|jpg);base64,/, ''))

            // const link = document.createElement('a')
            // link.innerHTML = 'download screenshot'
            // link.classList.add('dlLink')
            // link.addEventListener('click', function (ev) {
            //   link.href = dataURL
            //   link.download = 'screen.png'
            // }, false)
            // link.click()

        }, 10
        )

        screenTarget.style.width = ''
        screenTarget.style.height = ''
        screenTarget.style.borderRadius = ''
        screenTarget.style.border = ''
        screenTarget.style.minHeight = ''
        switchMode.style.background = ''
        fullScreen.style.background = ''
        avatar.style.width = ''
        avatar.style.height = ''
        avatar.style.objectFit = ''

        bgTexture = scene.background
        const canvasAspect = screenTarget.clientWidth / screenTarget.clientHeight
        const imageAspect = bgTexture.image ? bgTexture.image.width / bgTexture.image.height : 1
        const aspectBg = imageAspect / canvasAspect

        bgTexture.offset.x = aspectBg > 1 ? (1 - 1 / aspectBg) / 2 : 0
        bgTexture.repeat.x = aspectBg > 1 ? 1 / aspectBg : 1

        bgTexture.offset.y = aspectBg > 1 ? 0 : (1 - aspectBg) / 2
        bgTexture.repeat.y = aspectBg > 1 ? 1 : aspectBg

        scene.background = bgTexture

        const width = screenTarget.clientWidth
        const height = screenTarget.clientHeight

        camera.fov = initialFov
        camera.aspect = width / height
        camera.updateProjectionMatrix()
        composer.setSize(width, height)

        window.innerWidth <= 1920 ? renderer.setPixelRatio(Math.min(2, window.devicePixelRatio)) : ''
        renderer.antialias = false

        TokenFs()

      });
    }, 250)


    for (const checkInfo of checksInfo) {
      updateDisplay();
      checkInfo.addEventListener('click', updateDisplay);
    }
    
    function updateDisplay() {
      let checkedCount = 0;
      for (const checkInfo of checksInfo) {
        if (checkInfo.checked) {
          checkedCount++;
        }
      }
    
      if (checkedCount === checksInfo.length) {
        warningMintButton.classList.remove('disabled')
      } else {
        warningMintButton.classList.add('disabled');
      }
    }

  })

}

