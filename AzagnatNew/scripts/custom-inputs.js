export function customInput () {
  document.querySelector('form').onsubmit = e => e.preventDefault()

  const allInputElements = document.querySelectorAll('.input, input, select, option, label')
  allInputElements.forEach(i => i.classList.add('text-input'))

// input type range

  const es = document.querySelectorAll('input[type="range"].slider-progress')
  window.addEventListener('load', () => {
    es.forEach(e => e.style.setProperty('--value', e.value))
  })

  for (const e of es) {
    e.style.setProperty('--value', e.value)
    e.style.setProperty('--min', e.min == '' ? '0' : e.min)
    e.style.setProperty('--max', e.max == '' ? '100' : e.max)
    e.addEventListener('input', () => e.style.setProperty('--value', e.value))
  }

// input type range end

// input fake select

  const fakeSelects = document.querySelectorAll('.f-select-container')
  const trueSelects = document.querySelectorAll('select')
  const labels = document.querySelectorAll('label')

  labels.forEach((i, id) => {
    i.style.zIndex = `${(20 - id) * 2}`
  })

  fakeSelects.forEach((i, id) => {
    const options = i.querySelectorAll('.f-select-option:not(.placeholder)')
    const placeholder = i.querySelector('.placeholder')
    i.addEventListener('mouseenter', () => {
      i.classList.add('active')
      options.forEach(i => i.classList.add('active'))
    })

    i.addEventListener('click', () => {
      i.classList.add('active')
      options.forEach(i => i.classList.add('active'))
    })

    i.addEventListener('mouseleave', () => {
      i.classList.remove('active')
      options.forEach(i => i.classList.remove('active'))
    })

    options.forEach((i, id2) => {
      i.addEventListener('click', () => {
        options.forEach(i => i.classList.remove('active'))
        placeholder ? placeholder.innerHTML = i.innerText : ''
        const trueOptions = trueSelects[id].querySelectorAll('option')
        trueOptions.forEach(i => i.removeAttribute('selected'))
        trueOptions[id2].setAttribute('selected', 'selected')
        trueSelects[id].dispatchEvent(new InputEvent('change'))
      })
    })
  })

// new AirDatepicker('.air-picker',{
//   locale: localeEn,
//   dateFormat: 'yyyy-MM-dd',
//   onSelect(date) {
//     dateInput.value = date.formattedDate
//     dateInput.dispatchEvent(new InputEvent('change'))
//   }
// })

// dateInput.addEventListener('mouseenter', () => {
//   airPicker.classList.add('active')
//   dateInput.classList.add('active')
// })
//
// datelabel.addEventListener('mouseleave', () => {
//   airPicker.classList.remove('active')
//   dateInput.classList.remove('active')
// })

// input fake select end

  // const sol = document.querySelectorAll('.sol span')
  // const solSum = document.querySelector('.mint__sum span')
  //
  // let sum = 0
  // sol.forEach(i => {
  //   sum += Number(i.innerText)
  // })
  //
  // solSum.innerText = sum

}

