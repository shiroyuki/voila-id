function main() {
    form = new Form($('form'));
    $avatar = $('.avatar');
    $button = form.context.find('button');
    $inputs = form.context.find('input');

    form.context.on('submit', function (e) {
        e.preventDefault();

        if (!form.valid()) {
            return;
        }

        $inputs.parent().hide();
        $button.attr('disabled', true);
        $button.html($button.attr('data-progress'));

        onSuccess = function (response) {
            if (!response.authenticated) {
                return onFailure();
            }

            $avatar.find('img').attr('src', response.pass.avatar_url);
            $button.html($button.attr('data-done'));

            setTimeout(function () {
                window.location = relay_url;
            }, 3000);
        };

        onFailure = function () {
            alert('Either email or password is invalid. Please try again.');
            $inputs.parent().show();
            $button.attr('disabled', false);
            $button.html($button.attr('data-stdby'));
        };

        onError = function () {
            $('body').append([
                '<div style="z-index: 10; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: #000; padding: 60px; color: #cc0000; font-size: 24px; font-weight: 200;">',
                    'We are not ready to log you in at the moment. Please try again later.',
                '</div>'
            ].join(''))
        };

        form.submit({
            success: onSuccess,
            statusCode: {
                400: onFailure,
                403: onSuccess,
                405: onFailure,
                500: onError
            }
        });
    });
}

$(document).ready(main);