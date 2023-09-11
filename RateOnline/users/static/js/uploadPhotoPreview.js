preview = (input, image) => {
    document.querySelector(input).addEventListener('change', () => resize())
    function resize(){
      const resize_width = 110;
      const item = document.querySelector(input).files[0];
      const reader = new FileReader();

      reader.readAsDataURL(item);
      reader.name = item.name;
      reader.size = item.size;
      reader.onload = function(event) {
        const img = new Image();
        img.src = event.target.result;
        img.name = event.target.name;
        img.size = event.target.size;
        img.onload = function(el) {
          const elem = document.createElement('canvas');

          elem.width = resize_width;
          elem.height = resize_width;

          const ctx = elem.getContext('2d');
          ctx.drawImage(el.target, 0, 0, elem.width, elem.height);

          const srcEncoded = ctx.canvas.toDataURL('image/jpeg', 1);

          document.querySelector(image).src = srcEncoded;
        }
      }
    }
    }
    preview('#photo_1', '#image_1')
    preview('#photo_2', '#image_2')
    preview('#photo_3', '#image_3')
    preview('#photo_4', '#image_4')