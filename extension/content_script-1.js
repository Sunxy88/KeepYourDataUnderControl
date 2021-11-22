$( document ).ready(function() {

    var qrcode = {};
    $("e-img").each(function() {
        const source = $(this).attr("src");

        $(this).replaceWith(`<img src="${source}" ${getAttributes(this)}>`);
    });

    $("e-vid").each(function() {
        const source = $(this).attr("src");

        $(this).replaceWith(`<video ${getAttributes(this)}><source src="${source}"></video>`);
    });

    $("e-txt").each(function() {
        const source = $(this).attr("src");
        const alternativeText =  $(this).attr("alt");
        const element = this;

        $.get(source, function (data) {
            element.replaceWith(data);
          })
            .fail(function () {
                element.replaceWith(alternativeText);
            });
    });

    $("img").filter(':not([analyzed])').each(async function() {
        const source = $(this).attr("src");

        let qrCode = new QrCode(undefined, source);

        try {
            //Check If Image URL exists
            $(this).fadeTo( "fast" , 0, () => {

                qrCode.decode();
                setTimeout(() => {
                    const newSource = qrCode.getLink();
                    if(newSource)
                            $(this).attr("src", newSource);
                            $(this).attr("analyzed", '');
                            $(this).fadeTo("fast" , 1);
                },50);
            });
        }catch (exception) {
            if (exception.message !== "Not a qrCode") throw exception;
        }
    });
});

function getAttributes ( element ) {
    const attributes = element.attributes;
    let string = "";

    for (const attr of attributes) {
        if (attr.value) string += `${attr.name}=${attr.value} `;
        else string += `${attr.name} `;
    }
    return string;
}