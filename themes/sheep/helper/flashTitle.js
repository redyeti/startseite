/// based on answer by Matt from http://stackoverflow.com/questions/3381462/how-to-create-flashing-page-title-effect-like-facebook

(function () {

var original = document.title;
var timeout;

window.flashTitle = function (newMsg, howManyTimes) {
    function step() {
        document.title = (document.title == original) ? newMsg : original;

        if (isNaN(howManyTimes) || --howManyTimes > 0) {
            timeout = setTimeout(step, 1000);
        };
    };

    howManyTimes = parseInt(howManyTimes);

    cancelFlashTitle(timeout);
    step();
};

window.cancelFlashTitle = function () {
    clearTimeout(timeout);
    document.title = original;
};

}());
