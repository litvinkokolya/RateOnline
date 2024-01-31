function resize(input, image) {
  input.addEventListener('change', function() {
    var file = this.files[0];
    var reader = new FileReader();
    reader.onloadend = function() {
      image.src = reader.result;
    }
    reader.readAsDataURL(file);
  });
}

function preview(inputSelector, imageSelector) {
  const input = document.querySelector(inputSelector);
  const image = document.querySelector(imageSelector);
  resize(input, image);
}

preview('#photo_1', '#image_1');
preview('#photo_2', '#image_2');
preview('#photo_3', '#image_3');
preview('#photo_4', '#image_4');
