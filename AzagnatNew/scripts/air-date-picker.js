import AirDatepicker from 'air-datepicker'
import '../styles/air-datepicker.scss'

import localeEn from 'air-datepicker/locale/en'

const airPicker = document.querySelector('.air-picker')
const dateInput = document.querySelector('.date-label-pic')
const datelabel = document.querySelector('.date-label')

// var _default = {
//   days: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
//   daysShort: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
//   daysMin: ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'],
//   months: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
//   monthsShort: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
//   today: 'Today',
//   clear: 'Clear',
//   dateFormat: 'yyyy/MM/dd',
//   timeFormat: 'hh:mm aa',
//   firstDay: 0
// };

new AirDatepicker('.air-picker', {
  locale: localeEn,
  dateFormat: 'yyyy-MM-dd',
  onSelect (date) {
    dateInput.value = date.formattedDate
    dateInput.dispatchEvent(new InputEvent('change'))
  }
})

dateInput.addEventListener('mouseenter', () => {
  airPicker.classList.add('active')
  dateInput.classList.add('active')
})

datelabel.addEventListener('mouseleave', () => {
  airPicker.classList.remove('active')
  dateInput.classList.remove('active')
})

dateInput.addEventListener('click', (e) => {
  e.preventDefault()
})


