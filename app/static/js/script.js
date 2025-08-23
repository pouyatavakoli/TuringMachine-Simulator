const TMSimulator = (() => {
    function init() {
        $('#initBtn').on('click', handleInit);
        $('#resetBtn').on('click', handleReset);
        $('#stepBtn').on('click', handleStep)
    }

    function handleInit() {
        console.log("Initialize button clicked");
        // TODO: initialization logic
    }
    function handleReset(){
        console.log("Reset btn clicked");
        // TODO: reset logic
    }
    function handleStep(){
        console.log("reset button clicked");
    }

    return { init };
})();

$(document).ready(TMSimulator.init);