$(function () {
    /* Price Range Slider */
    // if ($('#steps-slider').length) {
    //     var slider = document.getElementById('steps-slider');
    //
    //     // Retrieve the min and max prices from the view
    //     var minPrice = parseInt(document.getElementById('min-price').innerText, 10);
    //     var maxPrice = parseInt(document.getElementById('max-price').innerText, 10);
    //
    //     // Initialize the slider with dynamic min and max
    //     noUiSlider.create(slider, {
    //         direction: 'rtl',
    //         start: [minPrice, maxPrice],
    //         connect: true,
    //         step: 50000,
    //         range: {
    //             'min': minPrice,
    //             'max': maxPrice
    //         }
    //     });
    //
    //     // Update the view with the selected price range
    //     slider.noUiSlider.on('update', function (values) {
    //         var selectedMinPrice = Math.round(values[0]);
    //         var selectedMaxPrice = Math.round(values[1]);
    //
    //         // Update the view elements with the user-set prices
    //         $('#price-range-from').text(numFormat(selectedMinPrice));
    //         $('#price-range-to').text(numFormat(selectedMaxPrice));
    //
    //         // Optionally, update hidden inputs or other elements if needed
    //         document.getElementById('selected-min-price').value = selectedMinPrice;
    //         document.getElementById('selected-max-price').value = selectedMaxPrice;
    //     });
    //
    // }

    if ($('#steps-slider').length) {
        var slider = document.getElementById('steps-slider');

        // Retrieve the min and max prices from the view
        var minPrice = parseInt(document.getElementById('min-price').innerText, 10);
        var maxPrice = parseInt(document.getElementById('max-price').innerText, 10);

        // Retrieve the stored price range or use the default min and max
        var storedMinPrice = localStorage.getItem('selectedMinPrice') || minPrice;
        var storedMaxPrice = localStorage.getItem('selectedMaxPrice') || maxPrice;

        // Initialize the slider with dynamic min and max
        noUiSlider.create(slider, {
            direction: 'rtl',
            start: [storedMinPrice, storedMaxPrice],
            connect: true,
            step: 50000,
            range: {
                'min': minPrice,
                'max': maxPrice
            }
        });

        // Update the view with the selected price range
        slider.noUiSlider.on('update', function (values) {
            var selectedMinPrice = Math.round(values[0]);
            var selectedMaxPrice = Math.round(values[1]);

            // Update the view elements with the user-set prices
            $('#price-range-from').text(numFormat(selectedMinPrice));
            $('#price-range-to').text(numFormat(selectedMaxPrice));

            // Store the selected prices in localStorage
            localStorage.setItem('selectedMinPrice', selectedMinPrice);
            localStorage.setItem('selectedMaxPrice', selectedMaxPrice);

            // Optionally, update hidden inputs or other elements if needed
            document.getElementById('selected-min-price').value = selectedMinPrice;
            document.getElementById('selected-max-price').value = selectedMaxPrice;
        });
    }

    /* Price Range Slider */

    /* On Sale Counter */
    function countDown() {
        var today = new Date();
        var eventDate = new Date("November 30,2025 00:00:00"); /* Change This Date To Update Counter */
        var currentTime = today.getTime();
        var eventTime = eventDate.getTime();
        var remTime = eventTime - currentTime;

        var sec = Math.floor(remTime / 1000);
        var min = Math.floor(sec / 60);
        var hrs = Math.floor(min / 60);
        var days = Math.floor(hrs / 24);

        hrs %= 24;
        min %= 60;
        sec %= 60;

        days = (days < 10) ? "0" + days : days;
        hrs = (hrs < 10) ? "0" + hrs : hrs;
        min = (min < 10) ? "0" + min : min;
        sec = (sec < 10) ? "0" + sec : sec;

        var elTimeCounter = $('.time-counter');
        var elDays = $('.days', elTimeCounter);
        var elHours = $('.hours', elTimeCounter);
        var elMinutes = $('.minutes', elTimeCounter);
        var elSeconds = $('.seconds', elTimeCounter);

        $('.num', elDays).html(days);
        $('.num', elHours).html(hrs);
        $('.num', elMinutes).html(min);
        $('.num', elSeconds).html(sec);

        setTimeout(countDown, 1000);
    }

    countDown();
    /* /On Sale Counter */

    /* Initialize menu */
    $('.droopmenu-navbar').droopmenu({
        dmArrow: true,
        dmArrowDirection: 'dmarrowdown'
    });
    /* /Initialize menu */

    /* Featured Products Filter */
    if ($('.featured-categories').length) {
        $('.featured-categories').click(function () {
            var category = $(this).data('val');
            $('.featured-product').each(function () {
                if ($(this).hasClass(category))
                    $(this).fadeIn();
                else
                    $(this).fadeOut(0);
            })

            /* Update Active Menu */
            $('.featured-categories').each(function () {
                $(this).removeClass('active');
                if ($(this).data('val') == category)
                    $(this).addClass('active');
            })
        })
        $('.featured-categories').eq(0).trigger('click');
    }
    /* /Featured Products Filter */

    /* Most Sold Products Filter */
    if ($('.most-sales-categories').length) {
        $('.most-sales-categories').click(function () {
            var category = $(this).data('val');
            $('.most-sales-product').each(function () {
                if ($(this).hasClass(category))
                    $(this).fadeIn();
                else
                    $(this).fadeOut(0);
            })

            /* Update Active Menu */
            $('.most-sales-categories').each(function () {
                $(this).removeClass('active');
                if ($(this).data('val') == category)
                    $(this).addClass('active');
            })
        })
        $('.most-sales-categories').eq(0).trigger('click');
    }
    /* /Most Sold Products Filter */

    /* Collapse In Mobile */
    if ($('.collapse').length) {
        if (($(window).width()) < 992) {
            $('.collapse').removeClass('show');
        }
    }
    /* /Collapse In Mobile */

    /* Num Format Functions */
    function intFormat(number) {
        var regex = /(\d)((\d{3},?)+)$/;
        number = number + '';
        number = number.split(',').join('');

        while (regex.test(number)) {
            number = number.replace(regex, '$1,$2');
        }
        return number;
    }

    function numFormat(number) {
        var pointReg = /([\d,\.]*)\.(\d*)$/, f;
        if (pointReg.test(number)) {
            f = RegExp.$2;
            return intFormat(RegExp.$1) + '.' + f;
        }
        return intFormat(number);
    }

    /* /Num Format Functions */

    /* Products Carousel */
    if ($('.products-carousel').length > 0) {
        var owl = $('.products-carousel');
        owl.owlCarousel({
            rtl: true,
            autoplay: true,
            autoplayHoverPause: true,
            margin: 25,
            nav: false,
            dots: false,
            loop: true,
            responsive: {
                0: {
                    items: 1
                },
                768: {
                    items: 3
                },
                1000: {
                    items: 4
                }
            }
        })
    }
    /* /Products Carousel */

    /* Product Order Number */
    if ($('.btn-plus').length > 0) {
        $('.btn-plus').click(function () {
            var index = $(this).index('.btn-plus');
            var orderNumber = Number($('input.quantity').eq(index).val());
            $('input.quantity').eq(index).val(orderNumber + 1);
        })

        $('.btn-minus').click(function () {
            var index = $(this).index('.btn-minus');
            var orderNumber = Number($('input.quantity').eq(index).val());
            if (orderNumber > 1)
                $('input.quantity').eq(index).val(orderNumber - 1);
        })
    }
    /* /Product Order Number */

    AOS.init();
});
