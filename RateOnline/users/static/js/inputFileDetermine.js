const fileInputs = document.querySelectorAll('input[type=file]');
const submitButton = document.querySelector('button');

fileInputs.forEach(input => {
  input.addEventListener('change', () => {
    const allFilesSelected = Array.from(fileInputs).every(input => input.files.length > 0);
    submitButton.disabled = !allFilesSelected;
  });
});