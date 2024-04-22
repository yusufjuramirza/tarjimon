$(document).ready(() => {
  let engTextArea = $('#text-field');
  let translateBtn = $('.translate-btn');
  let clearBtn = $('.text-field-cleaner-btn-wrapper');
  let loader = $('.hide-loader');
  let outputField = $('.output-field');

  // Auto Font Size
  engTextArea.on('input paste', function() {
    console.log(`Screen Height: ${screen.height}`);
    console.log(`Nav Body Height: ${$('.nav-body').css('height')}`);
    console.log(`Translate Body Height: ${$('.translator-body').css('height')}`);
    console.log(`Translate Body Button Box Height: ${$('.translate-btn-box').css('height')}`);

    setTimeout(() => {
      let engTextLength = this.innerText.length;
      let maxFontSize;
      let minFontSize;
      let charLim;
      let reductionFactorDivider;

      // handle font size for different screen sizes
      if (screen.width <= 600) {
        maxFontSize = 20;
        minFontSize = 14;
        charLim = 100;
        reductionFactorDivider = 100;
      } else if (screen.width <= 900) {
        maxFontSize = 22;
        minFontSize = 16;
        charLim = 200;
        reductionFactorDivider = 150
      } else if (screen.width <= 1200) {
        maxFontSize = 24;
        minFontSize = 18;
        charLim = 300;
        reductionFactorDivider = 200;
      }

      let newFontSize = maxFontSize;
      if (engTextLength > charLim) {
        let reductionFactor = (engTextLength - maxFontSize) / reductionFactorDivider;
        newFontSize = Math.max(minFontSize, maxFontSize - reductionFactor);
      }

      // apply new font size
      engTextArea.css('font-size', `${newFontSize}px`);
      $('.output-field').css('font-size', `${newFontSize}px`);
    }, 100); // end of setTimeout
  });

  // Avoid Rich Text
  $('[contenteditable]').on('paste', function (e) {
      e.preventDefault();
      const text = e.originalEvent.clipboardData.getData('text/plain');

      // Alternative using ContentEditable API:
      const editable = $(this);
      const selection = window.getSelection();
      if (selection.rangeCount > 0) {
        const range = selection.getRangeAt(0);
        range.deleteContents();
        range.insertNode(document.createTextNode(text));
      } else {
        editable.append(text);
      }
    });

  // Auto Expand Text Area Height
  engTextArea.on('input paste', function() {
    const scLeft = window.scrollX || (document.documentElement || document.body.parentNode || document.body).scrollLeft;
    const scTop = window.scrollY || (document.documentElement || document.body.parentNode || document.body).scrollTop;

    $(this).css('height', 'auto');
    // Set timeout
    setTimeout(() => {
      // handle translate button effect
      if (engTextArea.text() !== '') {
        translateBtn.removeAttr('disabled');
        translateBtn.css('opacity', '1');
      } else {
        translateBtn.attr('disabled');
        translateBtn.css('opacity', '0.6');
      }

      const newHeight = $(this).prop('scrollHeight');

      $(this).animate({
        height: newHeight + 'px'
      }, 50);

      // window.scrollTo(scLeft, scTop + 200);
    }, 500); // end of setTimeout()
  });

  // Translate
  translateBtn.on('click', function() {
    // hide output field
    outputField.css('display', 'none');
    // show loader
    loader.css('display', 'flex');

    if (engTextArea.text().trim() !== '') {
      // get data
      let textData = engTextArea.text().trim();

      // prepare data to be sent in a format that Flask can understand
      let formData = new FormData();
      formData.append('eng-field', textData);

      // Create an AJAX request to send to the server
      fetch('/translate', {
        method: 'POST',
        body: formData
      })
          .then(response => response.text())
          .then(data => {
            // hide loader
            loader.css('display', 'none');
            // show output field
            outputField.css('display', 'inline-block');
            // use the data from the server
            outputField.text(data);
          })
          .catch(error => {
            console.log(`Error happened in fetch('/translate')... ${error}`);
          });
    }
  }); // on click end

  // Clear English Text Field
  engTextArea.on('input paste', function() {
    // show text field clear button
    clearBtn.css('display', 'inline-block');

    clearBtn.on('click', function() {
      // clear text field
      engTextArea.text("");
      // clear output field
      outputField.text("");
      // reset counter of characters
      $('.counter').text('0');
      // reset field height
      engTextArea.css('height', 'auto');
      // put focus on text field
      engTextArea.focus();
      // hide text field clear button
      $(this).css('display', 'none');
    });
  });

});
