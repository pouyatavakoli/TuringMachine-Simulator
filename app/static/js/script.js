const TMSimulator = (() => {
    function init() {
        $('#initBtn').on('click', handleInit);
    }

    function handleInit() {
        console.log("Initialize button clicked");
        // TODO: initialization logic
    }

    return { init };
})();

$(document).ready(TMSimulator.init);