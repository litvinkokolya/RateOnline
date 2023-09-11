const closeBtn = document.querySelector('.close-judge-modal');
const modal = document.querySelector('.judge-modal');
const form = document.querySelector('.evaluations-form');
const blur = document.querySelector('.blur');

const radio = document.querySelectorAll('.evulation-radio')
const balls = document.getElementById('balls')
const ballsModal = document.getElementById('ballsModal')
let numberBalls = 0;
let modalBtn = document.querySelector('.open-modal')

window.onload=function(){
  window.scrollBy(0, 30);
}

let radioNames = Array.from(radio).map(i => i.name).filter((value, index, self) => self.indexOf(value) === index);

modalBtn.addEventListener('click', function() {
  let checkRadio = Array.from(radio).filter(i => i.checked);

  checkRadio.forEach(el => {
    if (radioNames.includes(el.name)) {
      radioNames = radioNames.filter(f => f !== el.name)
    }
  });

  for (const i of radio) {
    if (radioNames.includes(i.name)) {
      i.closest('div').style.outline = "1px solid red";
    }
  }

  if (radioNames.length === 0) {
    modal.classList.remove('visually-hidden');
    blur.classList.remove('visually-hidden')
    form.style.background = 'transparent';
  }
});

closeBtn.addEventListener('click', function() {
  modal.classList.add('visually-hidden');
  blur.classList.add('visually-hidden')
});

let calc = {
  summ: 0,
  valueArray: $(".evaluations-item").map(function() {
    return parseInt($(this).find("input:checked").attr("value")) || 0;
  }).get(),
  summation: function () {
    this.summ = this.valueArray.reduce((total, value) => total + value, 0);
    $("#balls").html(calc.summ);
    $("#ballsModal").html(calc.summ);
  },
  changeEvent: function () {
    $("input[type='radio']").change(function () {
      const element = event.target;
      const elementValue = parseInt(element.value);
      const elementId = $(element).parents(".evaluations-item").index();
      calc.valueArray[elementId] = elementValue;
      calc.summation ();
    });
  },
  init: function () {
    calc.summation ();
    calc.changeEvent ();
  }
};

calc.init ();