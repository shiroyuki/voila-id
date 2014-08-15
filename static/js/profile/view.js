function main() {
    var $body = $('body'),
        $dt   = $('.profile.view'),
        $form = $('.profile.edit form'),
        form  = new Form($form)
    ;

    $('.editor-trigger').on('click', function (e) {
        e.preventDefault();

        $body.toggleClass('editor-enabled');
    });

    onOk = function () {};

    $form.on('submit', function (e) {
        e.preventDefault();

        form.submit({
            success: function (data) {
                var data = form.data();

                $.each(data, function (k, v) {
                    $dt.find('[data-property=' + k + '] .inner-value').html(v);
                });
                
                $body.removeClass('editor-enabled');
            },
            statusCode: {
                500: function () {
                    alert('Ops!');
                }
            }
        })
    });
}

$(document).ready(main);