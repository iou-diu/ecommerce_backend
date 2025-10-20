"use strict";

// Class definition
var KTWidgets = function () {
    // Private properties

    // Advance Tables
    var _initAdvancedTableGroupSelection = function(element) {
        var table = KTUtil.getById(element);

        if (!table) {
            return;
        }

        KTUtil.on(table, 'thead th .checkbox > input', 'change', function (e) {
            var checkboxes = KTUtil.findAll(table, 'tbody td .checkbox > input');

            for (var i = 0, len = checkboxes.length; i < len; i++) {
                checkboxes[i].checked = this.checked;
            }
        });
    }

    var _initPriceSlider = function (element) {
        // init slider
        var slider = document.getElementById(element);
        if (typeof slider === 'undefined') {
            return;
        }

        if (!slider) {
            return;
        }

        noUiSlider.create(slider, {
            start: [20, 60],
            connect: true,
            range: {
                'min': 0,
                'max': 100
            }
        });
    }

    // Education Show More Demo
    var _initEducationShowMoreBtn = function() {
        var el = KTUtil.getById('kt_app_education_more_feeds_btn');

        if (!el) {
            return;
        }

        KTUtil.addEvent(el, 'click', function(e) {
            var elements = document.getElementsByClassName('education-more-feeds');

            if (!elements || elements.length <= 0) {
                return;
            }

            KTUtil.btnWait(el, 'spinner spinner-right spinner-white pr-15', 'Please wait...', true);

            setTimeout(function() {
                KTUtil.btnRelease(el);
                KTUtil.addClass(el, 'd-none');

                var item;

                for (var i = 0, len = elements.length; i < len; i++) {
                    item = elements[0];
                    KTUtil.removeClass(elements[i], 'd-none');

                    var textarea = KTUtil.find(item, 'textarea');
                    if (textarea) {
                        autosize(textarea);
                    }
                }

                KTUtil.scrollTo(item);
            }, 1000);
        });
    }

    // Public methods
    return {
        init: function () {
            // General Control

            // Table Widgets
            _initAdvancedTableGroupSelection('kt_advance_table_widget_1');
            _initAdvancedTableGroupSelection('kt_advance_table_widget_2');
            _initAdvancedTableGroupSelection('kt_advance_table_widget_3');
            _initAdvancedTableGroupSelection('kt_advance_table_widget_4');

            // Form Widgets
            _initPriceSlider('kt_price_slider');

            // Education App
            _initEducationShowMoreBtn();
        }
    }
}();

// Webpack support
if (typeof module !== 'undefined') {
    module.exports = KTWidgets;
}

jQuery(document).ready(function () {
    KTWidgets.init();
});
