export function TokenFs () {
  const container3dWidth = document.querySelector('.container3d').clientWidth
  const titleContainer = document.querySelector('.title-container')
  const container3dFooter = document.querySelector('.container3d-footer')
  const mainTitle = document.querySelector('.main-title')
  const userName = document.querySelector('.user-name')
  const avatar = document.querySelector('.avatar')
  const switchModeContainer = document.querySelector('.switch-mode__container')
  const switchMode = document.querySelector('.switch-mode')
  const fullScreen__container = document.querySelector('.full-screen__container')
  const fullScreen = document.querySelector('.full-screen')

  titleContainer.style.padding = `${ ( container3dWidth / 100 ) * 4 }px`
  container3dFooter.style.padding = `${ ( container3dWidth / 100 ) * 4 }px`

  mainTitle.style.fontSize = `${ ( container3dWidth / 100 ) * 7 }px`
  userName.style.fontSize = `${ ( container3dWidth / 100 ) * 6 }px`

  avatar.style.top = `${ ( container3dWidth / 100 ) * 4 }px`
  avatar.style.right = `${ ( container3dWidth / 100 ) * 4 }px`
  avatar.style.width = `${ ( container3dWidth / 100 ) * 20 }px`
  avatar.style.height = `${ ( container3dWidth / 100 ) * 20 }px`

  switchModeContainer.style.width = `${ ( container3dWidth / 100 ) * 15 }px`
  switchModeContainer.style.height = `${ ( container3dWidth / 100 ) * 15 }px`
  switchMode.style.width = `${ ( container3dWidth / 100 ) * 15 }px`
  switchMode.style.height = `${ ( container3dWidth / 100 ) * 15 }px`

  fullScreen__container.style.width = `${ ( container3dWidth / 100 ) * 15 }px`
  fullScreen__container.style.height = `${ ( container3dWidth / 100 ) * 15 }px`
  fullScreen.style.width = `${ ( container3dWidth / 100 ) * 15 }px`
  fullScreen.style.height = `${ ( container3dWidth / 100 ) * 15 }px`

}