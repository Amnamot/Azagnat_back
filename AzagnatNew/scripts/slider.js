import Swiper from 'swiper';

//BildSlider
let sliders = document.querySelectorAll("._swiper");
if (sliders) {
  for (let index = 0; index < sliders.length; index++) {
    let slider = sliders[index];
    if (!slider.classList.contains("swiper-bild")) {
      let slider_items = slider.children;
      if (slider_items) {
        for (let index = 0; index < slider_items.length; index++) {
          let el = slider_items[index];
          el.classList.add("swiper-slide");
        }
      }
      let slider_content = slider.innerHTML;
      let slider_wrapper = document.createElement("div");
      slider_wrapper.classList.add("swiper-wrapper");
      slider_wrapper.innerHTML = slider_content;
      slider.innerHTML = "";
      slider.appendChild(slider_wrapper);
      slider.classList.add("swiper-bild");

      if (slider.classList.contains("_swiper_scroll")) {
        let sliderScroll = document.createElement("div");
        sliderScroll.classList.add("swiper-scrollbar");
        slider.appendChild(sliderScroll);
      }
    }
  }
}

const slider = () => {

  const dottsF = () => {
    return `<span class="swiper-pagination-bullet" >●</span>`;
  }
  
  let slider_clients = new Swiper(".NFT__slider", {
    autoplay: {
      delay: 9000,
      disableOnInteraction: false,
    },
    
    observer: true,
    observeParents: true,
    autoHeight: true,
    speed: 800,
    loop: true,
    loopAdditionalSlides: 5,
    preloadImages: true,
    lazy: true,
    slidesPerView: 1,
    width: 130,
    spaceBetween: 30,
    centeredSlides: true,
    centerInsufficientSlides: true,
    touch: true,
    pagination: {
      el: '.NFT__dotts',
      clickable: true,
      renderBullet: dottsF,
    },
    breakpoints: {
      300: {
        width: 200,
        slidesPerView: 1,
        spaceBetween: 30,
      },
      768: {
        width: 280,
        slidesPerView: 1,
        spaceBetween: 40,
      },
    },
    
  });
}
export default slider;