(() => {
  const userDataObj = JSON.parse(localStorage.getItem('userObj')) ?? {}
  const userLabels = document.querySelectorAll('.user-data label')
  const userInputs = document.querySelectorAll('.user-data input')
  const userSelects = document.querySelectorAll('.user-data select')
  //= ============name

  const nameField = document.querySelector('.user-name')
  const nameInput = userInputs[0]

  nameInput.value = userDataObj.name ?? ''
  nameField.innerText = userDataObj.name ?? 'leprechaun'
  userDataObj.name ? userLabels[0].classList.add('active') : ''

  userInputs[0].addEventListener('input', () => {
    if (nameInput.value.length >= 5) {
      userLabels[0].classList.add('active')
      nameField.innerText = nameInput.value
      userDataObj.name = nameInput.value
      localStorage.setItem('userObj', JSON.stringify(userDataObj))
    } else {
      userLabels[0].classList.remove('active')
      nameField.innerText = 'leprechaun'
      userDataObj.name = null
      localStorage.setItem('userObj', JSON.stringify(userDataObj))
    }
  })

  //  ====================date
  const dateField = document.querySelector('.user-date')
  const dateInput = userInputs[1]

  dateInput.value = userDataObj.date ?? ''
  // dateField.innerText = userDataObj.date ?? '*****'
  userDataObj.date ? userLabels[1].classList.add('active') : ''

  userInputs[1].addEventListener('change', () => {
    userLabels[1].classList.add('active')
    // dateField.innerText = dateInput.value
    userDataObj.date = dateInput.value
    localStorage.setItem('userObj', JSON.stringify(userDataObj))
  })

  //  =========gender

  const genderInput = userSelects[0]
  const gOptions = genderInput.querySelectorAll('option')

  if (userDataObj.gender) {
    gOptions.forEach(i => i.removeAttribute('selected'))
    gOptions[Number(userDataObj.gender)].setAttribute('selected', 'selected')
    document.querySelector('.f-select-container__gender .placeholder').innerHTML = userDataObj.gender === '0' ? 'Man' : 'Woman'
    userLabels[2].classList.add('active')
  }

  genderInput.addEventListener('change', () => {
    userLabels[2].classList.add('active')
    userDataObj.gender = genderInput.value
    console.log(genderInput.value)
    localStorage.setItem('userObj', JSON.stringify(userDataObj))
  })

  //  ================avatar

  const avatar = document.querySelector('.avatar')

  userDataObj.imgData ? avatar.src = 'data:image/png;base64,' + userDataObj.imgData : ''
  userDataObj.imgData ? userLabels[3].classList.add('active') : ''

  userInputs[2].onchange = () => readURL(userInputs[2])

  function readURL (input) {

      avatar.style.display = 'block'

      input.nextElementSibling.innerText = input.files[0].name.split(".")[0].slice(0, 16)

      localStorage.setItem('avatar_name', input.files[0].name)

      if (input.files && input.files[0]) {
        const reader = new FileReader()

        reader.onload = function (e) {


          let dataURL = e.target.result.toString()
          dataURL = dataURL.replace(/^data:image\/(png|jpg|jpeg);base64,/, '')


          if (dataURL.length > 450000) {
            document.querySelector('.warning-avatar-exceed').classList.remove('hide')
            return
          }

          avatar.src = e.target.result
          userLabels[3].classList.add('active')

          userDataObj.imgData = dataURL
          localStorage.setItem('userObj', JSON.stringify(userDataObj))
        }

        reader.readAsDataURL(input.files[0])
      }

  }

  //  =========language

  const languageInput = userSelects[1]
  const lOptions = languageInput.querySelectorAll('option')

  if (userDataObj.language) {
    lOptions.forEach(i => i.removeAttribute('selected'))
    lOptions[Number(userDataObj.language)].setAttribute('selected', 'selected')
    document.querySelector('.f-select-container__language .placeholder').innerHTML = userDataObj.language === '0' ? 'English' : 'Russian'
    userLabels[4].classList.add('active')
  }

  languageInput.addEventListener('change', () => {
    userLabels[4].classList.add('active')
    userDataObj.language = languageInput.value
    localStorage.setItem('userObj', JSON.stringify(userDataObj))
  })
})()
