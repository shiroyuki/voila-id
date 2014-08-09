function main() {
    gravatar   = new GravatarService(gravatar_service_url);
    form       = new Form($('form'));
    $container = $('.container.main');
    $feedback  = $('.feedback');
    $avatar    = $feedback.find('.avatar');
    $status    = $feedback.find('.status');
    $appForm   = $('application-form');

    function delaySwitchToStandby() {
        setTimeout(function () {
            $container.attr('data-mode', 'stdby');
        }, 3000);
    }

    function onRegistration(e) {
        var data = form.data();

        e.preventDefault();

        if (!form.valid()) {
            return false;
        }

        onAvatarResolved = function (avatar) {
            $avatar.find('img').attr('src', avatar.url);
        };

        onFailure = function () {
            $status.html('Unable to register you to the system.');
            delaySwitchToStandby();
        };

        onSuccess = function (response) {
            if (response.success) {
                $status.html('<a class="btn btn-success" href="' + login_url + '">Log in</a>');

                return;
            }

            $status.html('You seem to be already registered.');
            delaySwitchToStandby();
        };

        $container.attr('data-mode', 'processing');

        gravatar.resolveUrl(data.email, 200, onAvatarResolved);

        form.submit({
            success: onSuccess,
            error:   onFailure,
            statusCode: {
                405: onFailure
            }
        });
    }

    form.context.on('submit', onRegistration);

    form.data({
        name: 'Juti Noppornpitak',
        email: 'juti_n@yahoo.co.jp',
        username: 'shiroyuki',
        plain_password: 'iamgenius'
    });
}

$(document).ready(main);