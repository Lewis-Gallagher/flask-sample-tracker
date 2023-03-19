const projectNameEl =  document.getElementById('project')
const sampleNameEl = document.getElementById('sample_name')
const dateEl = document.getElementById('date')
const outputEl = document.getElementById('output')

let formElements = document.forms["sample-input"].getElementsByClassName("user-input");

for (const elem of formElements) {
    elem.addEventListener("input", function() {
        inputDate = new Date(dateEl.value)
        newDate = inputDate.toISOString().split('T')[0].split('-').join('')
        outputEl.textContent = (sampleNameEl.value + '_' + projectNameEl.options[projectNameEl.selectedIndex].value + '_' + newDate).split(' ').join('_')
    })
}