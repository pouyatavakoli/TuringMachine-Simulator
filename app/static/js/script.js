const TMSimulator = (() => {
  let machineId = null;
  let runInterval = null;
  const simulationSpeed = 300; // ms per step

  function init() {
    $("#initBtn").on("click", handleInit);
    $("#resetBtn").on("click", handleReset);
    $("#stepBtn").on("click", handleStep);
    $("#runBtn").on("click", handleRunToggle);
    $("#runFastBtn").on("click", handleFastRun);
    $("#clearTape").on("click", () => $("#initialTape").val(""));
    loadMachines();
    toggleControls(false);
  }

  function handleInit() {
    const initialTape = $("#initialTape").val();
    const machineName = $("#machineSelect").val();
    if (!machineName) return updateStatus("Please select a machine");

    $.postJSON(
      "/api/init",
      { tape: initialTape, machine: machineName },
      (response) => {
        machineId = response.machine_id;
        updateMachineState(response.state);
        updateMachineInfo(response.machine_info);
        toggleControls(true);
        updateStatus("Machine initialized and ready");
      },
      (xhr) => updateStatus("Error initializing machine: " + xhr.responseText)
    );
  }

  function handleReset() {
    if (!machineId) return;
    const tapeStr = $("#initialTape").val();

    $.postJSON(
      "/api/reset",
      { machine_id: machineId, tape: tapeStr },
      (response) => {
        updateMachineState(response.state);
        updateStatus("Machine reset");
      },
      (xhr) => updateStatus("Error resetting machine: " + xhr.responseText)
    );
  }

  function handleStep() {
    if (!machineId) return;

    $.postJSON(
      "/api/step",
      { machine_id: machineId },
      (response) => {
        updateMachineState(response.state);
        if (response.state.halted) updateStatus("Computation halted");
      },
      (xhr) => updateStatus("Error stepping machine: " + xhr.responseText)
    );
  }

  function handleRunToggle() {
    if (!machineId) return;
    const $btn = $("#runBtn");

    if (runInterval) {
      stopRun();
      updateStatus("Computation paused");
    } else {
      $btn
        .html('<i class="fas fa-stop me-2"></i>Stop')
        .removeClass("btn-info")
        .addClass("btn-danger");
      startRun();
    }
  }

  function handleFastRun() {
    if (!machineId) return;

    $.postJSON(
      "/api/run",
      { machine_id: machineId, max_steps: 1000 },
      (response) => {
        updateMachineState(response.state);
        updateStatus(
          response.state.halted
            ? "Computation completed"
            : "Computation stopped"
        );
      },
      (xhr) => updateStatus("Error running machine: " + xhr.responseText)
    );
  }

  function loadMachines() {
    $.get("/api/machines", (machines) => {
      const $select = $("#machineSelect").empty();
      machines.forEach((m) => {
        $select.append(`<option value="${m.id}">${m.name}</option>`);
      });
    });
  }

  function toggleControls(enabled) {
    $("#stepBtn, #runBtn, #runFastBtn, #resetBtn").prop("disabled", !enabled);
  }

  function startRun() {
    if (runInterval) return;

    runInterval = setInterval(() => {
      if (!machineId) return stopRun();

      $.postJSON(
        "/api/step",
        { machine_id: machineId },
        (response) => {
          updateMachineState(response.state);
          if (response.state.halted) {
            stopRun();
            updateStatus("Computation halted");
          }
        },
        (xhr) => {
          stopRun();
          updateStatus("Error during computation: " + xhr.responseText);
        }
      );
    }, simulationSpeed);
  }

  function stopRun() {
    clearInterval(runInterval);
    runInterval = null;
    $("#runBtn")
      .html('<i class="fas fa-play-circle me-2"></i>Run')
      .removeClass("btn-danger")
      .addClass("btn-info");
  }

  // AJAX helper
  $.postJSON = function (url, data, success, error) {
    $.ajax({
      url,
      method: "POST",
      contentType: "application/json",
      data: JSON.stringify(data),
      success,
      error: error || ((xhr) => console.error("Error:", xhr.responseText)),
    });
  };

  return { init };
})();

$(document).ready(TMSimulator.init);

// ------------------------
// UI Update Functions
// ------------------------
function updateStatus(message) {
  $("#statusInfo").text(message);
}

function updateMachineState(state) {
  $("#currentState").text(state.current_state || "-");
  $("#stepCount").text(state.steps || 0);

  const $tapeContainer = $("#tapeContainer").empty();
  if (state.tape?.length) {
    state.tape.forEach((symbol, index) => {
      const position = (state.min_index || 0) + index;
      const isHead = position === (state.head_position || 0);
      const $cell = $("<div>").addClass("tape-cell").text(symbol);
      $cell.append($("<div>").addClass("cell-index").text(position));
      if (isHead)
        $cell
          .addClass("cell-head")
          .append($("<div>").addClass("head-indicator").text("HEAD"));
      $tapeContainer.append($cell);
    });
  } else {
    $tapeContainer.append(
      $("<div>").addClass("text-center text-muted").text("Tape is empty")
    );
  }

  if (state.halted) {
    $("#statusInfo").html(
      `<span class="badge bg-success">HALTED</span> Computation completed after ${state.steps} steps`
    );
  }
}

function updateMachineInfo(info) {
  $("#statesInfo").text(info.states?.length ? info.states.join(", ") : "-");
  $("#inputAlphabet").text(
    info.input_alphabet?.length ? info.input_alphabet.join(", ") : "-"
  );
  $("#tapeAlphabet").text(
    info.tape_alphabet?.length ? info.tape_alphabet.join(", ") : "-"
  );
  $("#blankSymbol").text(info.blank || "-");
  $("#initialState").text(info.initial_state || "-");
  $("#finalStates").text(
    info.final_states?.length ? info.final_states.join(", ") : "-"
  );

  const $transitionsList = $("#transitionsList").empty();
  if (!info.transitions?.length) {
    $transitionsList.append(
      $("<div>")
        .addClass("text-center text-muted")
        .text("No transitions defined")
    );
    return;
  }

  info.transitions.forEach((t) => {
    const text = `δ(${t.current_state}, ${t.current_symbol}) = (${t.next_state}, ${t.write_symbol}, ${t.move})`;
    $transitionsList.append(
      $("<div>").addClass("list-group-item transition-card").text(text)
    );
  });
}
