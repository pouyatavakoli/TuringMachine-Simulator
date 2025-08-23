const TMSimulator = (() => {
    function init() {
        $('#initBtn').on('click', handleInit);
        $('#resetBtn').on('click', handleReset);
    }

    function handleInit() {
        console.log("Initialize button clicked");
        // TODO: initialization logic
    }
    function handleReset(){
        console.log("Reset btn clicked");
        // TODO: reset logic
    }

    return { init };
})();

$(document).ready(TMSimulator.init);