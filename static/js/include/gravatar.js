function GravatarService(apiUrlPattern) {
    this.urlPattern = apiUrlPattern;
}

GravatarService.prototype.resolveUrl = function (email, size, handler) {
    $.ajax(
        this.urlPattern,
        {
            method: 'get',
            data: {
                email:   email,
                size:    size
            },
            success: handler
        }
    )
};