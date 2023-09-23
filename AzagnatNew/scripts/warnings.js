export function Warnings () {
  const warnings = document.querySelectorAll('.warning')
  warnings.forEach(i => {
    let button = i.querySelectorAll('.warning__button')
    button[0] ? button[0].addEventListener('click', e => {
      if (e.currentTarget.classList.contains('disabled')) {
        return;
      }
      i.classList.add('hide')
      document.body.style.overflow = ''
    }) : ''
    button[1] ? button[1].addEventListener('click', e => {
      if (e.currentTarget.classList.contains('disabled')) {
        return;
      }
      i.classList.add('hide')
      document.body.style.overflow = ''
    }) : ''
    i.addEventListener('click', e => {
      if (e.target === i && i.classList.contains("warning-ref-redeemed")) {
        document.location.href = "https://azagnat.top/"
      } else {
        i.classList.add('hide')
        document.body.style.overflow = ''
      }
    })
  })
}



