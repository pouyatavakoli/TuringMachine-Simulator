const TMSimulator = (() => {
    function init() {
        $('#initBtn').on('click', handleInit);
        $('#resetBtn').on('click', handleReset);
        $('#stepBtn').on('click', handleStep)
        $('#runBtn').on('click', handleRunToggle);
        $('#runFastBtn').on('click', handleFastRun);
        loadMachines();
        $('#clearTape').on('click', () => $('#initialTape').val(''));
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
    function handleRunToggle() {
    console.log("Run button clicked");
    // TODO: for run logic
    }

    function handleFastRun() {
    console.log("Fast run button clicked");
    // TODO: for fast run logic
    }

    function loadMachines() {
    //TODO: loading machines
    console.log("Loading machines");
}

    return { init };
})();

$(document).ready(TMSimulator.init);