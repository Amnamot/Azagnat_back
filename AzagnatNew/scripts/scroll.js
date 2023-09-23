import {gsap} from "gsap";
import { ScrollTrigger } from './libs/ScrollTrigger'
import { ScrollToPlugin } from './libs/ScrollToPlugin'
gsap.registerPlugin(ScrollTrigger, ScrollToPlugin)

export function scroll () {
  // let dist
  // let menuHeight = document.querySelector('.menu').getBoundingClientRect().height
  // let menuContainerHeight = document.querySelector('.menu-container').getBoundingClientRect().height
  // dist = menuContainerHeight - menuHeight
  //
  // let t1 = gsap.timeline({
  //   scrollTrigger: {
  //     trigger: '.container-webgl',
  //     start: `top top+=${document.querySelector('.header').getBoundingClientRect().height + 20}`,
  //     end: `+${dist}`,
  //     pin: true,
  //     scrub: true
  //   }
  // })
  // t1.to('.menu-container', {
  //   y: `-${dist}px`
  // })

  let mainContainer = document.querySelector('.main')
  let container3d = document.querySelector('.container3d')
  let left = window.innerWidth - mainContainer.getBoundingClientRect().right
  container3d.style.left = `${left}px`
}

