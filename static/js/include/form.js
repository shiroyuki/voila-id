function Form($context) {
    this.context = $context;
}

Form.prototype.data = function (new_data) {
    var $inputs = this.context.find('input'),
        data   = {}
    ;

    if (new_data !== undefined) {
        $.each(new_data, function (k, v) {
            $inputs.filter('[name=' + k + ']').val(v);
        });
    }

    $inputs.each(function () {
        var $input = $(this);
        data[$input.attr('name')] = $input.val();
    });

    return data;
};

Form.prototype.submit = function (options) {
    var
        url    = this.context.attr('action'),
        method = this.context.attr('method') || 'post',
        data   = this.data()
    ;

    options.method = method;
    options.data   = data;

    $.ajax(url, options);
};

Form.prototype.valid = function () {
    var inputs = this.context.find('input'),
        validFields = 0
    ;

    inputs.each(function () {
        validFields += $(this).is(':valid') ? 1 : 0;
    });

    return validFields === inputs.length;
};