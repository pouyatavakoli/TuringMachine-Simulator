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
    let machineId = null;

    function handleInit() {
        //console.log("Initialize button clicked");
        const initialTape = $('#initialTape').val();
        const machineName = $('#machineSelect').val();

        $.postJSON(
            '/api/init',
            { tape: initialTape, machine: machineName },
            (response) => {
                machineId = response.machine_id;
                updateMachineState(response.state);
                updateMachineInfo(response.machine_info);
                
                // Enable controls
                toggleControls(true);
                updateStatus('Machine initialized and ready');
            },
            (xhr) => updateStatus('Error initializing machine: ' + xhr.responseText)
        );
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

    function toggleControls(enabled) {
    $('#stepBtn, #runBtn, #runFastBtn').prop('disabled', !enabled);
    }
    // AJAX helper
    $.postJSON = function (url, data, success, error) {
        $.ajax({
            url: url,
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success,
            error: error || ((xhr) => console.error('Error:', xhr.responseText)),
        });
    };


    return { init };
})();

$(document).ready(TMSimulator.init);


function updateStatus(message) {
    $('#statusInfo').text(message);
}

function updateMachineState(state) {
    $('#currentState').text(state.current_state || '-');
    $('#stepCount').text(state.steps || 0);
    
    if (state.halted) {
        $('#statusInfo').html(
            `<span class="badge bg-success">HALTED</span> Computation completed after ${state.steps} steps`
        );
    }
    // Update tape display
    const $tapeContainer = $('#tapeContainer').empty();
    
    if (state.tape && state.tape.length > 0) {
        state.tape.forEach((symbol, index) => {
            const position = (state.min_index || 0) + index;
            const isHead = position === (state.head_position || 0);
            
            const $cell = $('<div>').addClass('tape-cell').text(symbol);
            $cell.append($('<div>').addClass('cell-index').text(position));
            
            if (isHead) {
                $cell.addClass('cell-head');
                $cell.append($('<div>').addClass('head-indicator').text('HEAD'));
            }
            
            $tapeContainer.append($cell);
        });
    } else {
        $tapeContainer.append(
            $('<div>').addClass('text-center text-muted').text('Tape is empty')
        );
    }

    // Update history
    if (history && history.length > 0) {
        history.forEach((step) => {
            const tapeStr = step.tape ? step.tape.join(' ') : '';
            const newRow = `
                <tr class="history-step">
                    <td>${step.step}</td>
                    <td><span class="badge bg-primary">${step.state}</span></td>
                    <td><span class="badge bg-secondary">${step.current_symbol}</span></td>
                    <td><code>${tapeStr}</code></td>
                    <td>${step.head}</td>
                </tr>
            `;
            $('#historyTable').prepend(newRow);
        });
    }
}

function updateMachineInfo(info) {
    $('#statesInfo').text(info.states ? info.states.join(', ') : '-');
    $('#inputAlphabet').text(info.input_alphabet ? info.input_alphabet.join(', ') : '-');
    $('#tapeAlphabet').text(info.tape_alphabet ? info.tape_alphabet.join(', ') : '-');
    $('#blankSymbol').text(info.blank || '-');
    $('#initialState').text(info.initial_state || '-');
    $('#finalStates').text(info.final_states ? info.final_states.join(', ') : '-');
    
    const $transitionsList = $('#transitionsList').empty();
    if (!info.transitions || info.transitions.length === 0) {
        $transitionsList.append(
            $('<div>').addClass('text-center text-muted').text('No transitions defined')
        );
        return;
    }
    
    info.transitions.forEach((t) => {
        const text = `δ(${t.current_state}, ${t.current_symbol}) = (${t.next_state}, ${t.write_symbol}, ${t.move})`;
        $transitionsList.append($('<div>').addClass('list-group-item transition-card').text(text));
    });
}