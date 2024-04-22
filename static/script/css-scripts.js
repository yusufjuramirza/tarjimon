$(document).ready(() => {
    let engTextArea = $('#text-field');
    let engTextAreaBox = $('.eng-text-field-box')

    // Outline Effect
    engTextArea.on('focus', function() {
        engTextAreaBox.addClass('active');
    });
    engTextArea.on('blur', function() {
        engTextAreaBox.removeClass('active');
    });

    // Character Counter
    // ∞
    engTextArea.on('input paste', function() {
        setTimeout(() => {
            $('.counter').text(`${engTextArea.text().length}`);
        }, 100);
    });

    // Placeholder Handle
    engTextArea.on('focus', function() {
        // handle placeholder show
        $(this).removeAttr('placeholder');
    });

    engTextArea.on('blur', function() {
        // handle placeholder show
        if (engTextArea.text() === '') {
            $(this).attr('placeholder', 'Yozing...');
        }
    });

    // Announcement Banner Handle
    $('#ann-close-btn').on('click', function() {
        const annBanner = $('#announcement-banner');
        const translateBody = $('.translator-body');

        let newHeight = annBanner.prop('height') - translateBody.prop('margin-top')
        // shrink margin bottom accordingly
        translateBody.css('margin-top', `${newHeight}px`);
        // remove announcement banner
        annBanner.css('display', 'none');
    });

});
