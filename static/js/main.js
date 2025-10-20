toastr.options = {
    "closeButton": false,
    "debug": false,
    "newestOnTop": false,
    "progressBar": false,
    "positionClass": "toast-top-center",
    "preventDuplicates": false,
    "onclick": null,
    "showDuration": "300",
    "hideDuration": "1000",
    "timeOut": "2000",
    "extendedTimeOut": "1000",
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut"
};

var arrows;
if (KTUtil.isRTL()) {
    arrows = {
        leftArrow: '<i class="la la-angle-right"></i>',
        rightArrow: '<i class="la la-angle-left"></i>'
    }
} else {
    arrows = {
        leftArrow: '<i class="la la-angle-left"></i>',
        rightArrow: '<i class="la la-angle-right"></i>'
    }
}
$('.dateinput').datepicker({
    format: 'yyyy-mm-dd',
    autoclose: true,
    rtl: KTUtil.isRTL(),
    orientation: "bottom left",
    templates: arrows
});

$('.timeinput').timepicker({
    minuteStep: 1,
    defaultTime: '',
    showSeconds: false,
    showMeridian: false,
    snapToStep: true,
});

$('.select').select2({width: '100%'});
$('.selectmultiple').select2({
    placeholder: "Please select from list",
    width: '100%',
});
$('.selectmultiple_tag').select2({
    placeholder: "Please select from list",
    width: '100%',
    tags:true
});

// quilljs_textarea('textarea', {
//     modules: {
//         toolbar: [
//             [{'header': 1}],
//             [{'header': 2}],
//             ['bold', 'italic', 'underline'],
//             ['image', 'link'],
//             [{'list': 'ordered'}, {'list': 'bullet'}],
//             [{'align': []}],
//         ]
//     },
//     theme: 'snow',
// });

// quilljs_textarea('textarea', {
//     modules: {
//         toolbar: [
//             [{'header': 1}],
//             [{'header': 2}],
//             ['bold', 'italic', 'underline'],
//             ['link'],
//             [{'list': 'bullet'}],
//         ]
//     },
//     theme: 'snow',
// });