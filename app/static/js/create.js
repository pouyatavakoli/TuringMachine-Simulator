$(document).ready(function () {
  let transitionCount = 0;

  // Add transition
  $("#addTransitionBtn").click(function () {
    const template = $("#transitionTemplate").html();
    const newTransition = $(template);

    // Add remove functionality
    newTransition.find(".remove-transition").click(function () {
      $(this).closest(".transition-row").remove();
      updatePreview();
      checkTransitions();
    });

    // Add input change handlers
    newTransition.find("input, select").on("input change", updatePreview);

    $("#transitionsContainer").append(newTransition);
    $("#noTransitionsMessage").hide();
    transitionCount++;
    updatePreview();
  });

  // Check if there are any transitions
  function checkTransitions() {
    if ($(".transition-row").length === 0) {
      $("#noTransitionsMessage").show();
    }
  }

  // Update preview
  function updatePreview() {
    const name = $("#machineName").val() || "Untitled Machine";
    const states = $("#machineStates").val() || "";
    const inputAlphabet = $("#inputAlphabet").val() || "";
    const tapeAlphabet = $("#tapeAlphabet").val() || "";
    const blank = $("#blankSymbol").val() || "□";
    const initialState = $("#initialState").val() || "";
    const finalStates = $("#finalStates").val() || "";

    let preview = `# Turing Machine: ${name}\n`;
    preview += `states: ${states}\n`;
    preview += `input_alphabet: ${inputAlphabet}\n`;
    preview += `tape_alphabet: ${tapeAlphabet}\n`;
    preview += `blank: ${blank}\n`;
    preview += `initial_state: ${initialState}\n`;
    preview += `final_states: ${finalStates}\n`;
    preview += "transitions:\n";

    // Add transitions
    $(".transition-row").each(function () {
      const currentState =
        $(this).find(".transition-current-state").val() || "";
      const readSymbol = $(this).find(".transition-read").val() || "";
      const nextState = $(this).find(".transition-next-state").val() || "";
      const writeSymbol = $(this).find(".transition-write").val() || "";
      const move = $(this).find(".transition-move").val() || "R";

      if (currentState && readSymbol && nextState && writeSymbol) {
        preview += `${currentState},${readSymbol} -> ${nextState},${writeSymbol},${move}\n`;
      }
    });

    $("#previewPanel").text(preview);
  }

  // Set up input change handlers for form fields
  $(
    "#machineName, #machineStates, #inputAlphabet, #tapeAlphabet, #blankSymbol, #initialState, #finalStates"
  ).on("input", updatePreview);

  // Preview button
  $("#previewBtn").click(updatePreview);

  // Reset form
  $("#resetBtn").click(function () {
    if (
      confirm("Are you sure you want to reset the form? All data will be lost.")
    ) {
      $("input, select").val("");
      $("#blankSymbol").val("□");
      $(".transition-row").remove();
      $("#noTransitionsMessage").show();
      updatePreview();
    }
  });

  // Create machine
  $("#createBtn").click(function () {
    // Validate required fields
    const requiredFields = [
      $("#machineName"),
      $("#machineStates"),
      $("#inputAlphabet"),
      $("#tapeAlphabet"),
      $("#blankSymbol"),
      $("#initialState"),
      $("#finalStates"),
    ];

    let isValid = true;
    requiredFields.forEach((field) => {
      if (!field.val().trim()) {
        field.addClass("is-invalid");
        isValid = false;
      } else {
        field.removeClass("is-invalid");
      }
    });

    // Check transitions
    if ($(".transition-row").length === 0) {
      showAlert("Please add at least one transition", "danger");
      isValid = false;
    }

    if (!isValid) {
      showAlert("Please fill in all required fields", "danger");
      return;
    }

    // Collect transitions
    const transitions = [];
    $(".transition-row").each(function () {
      const currentState = $(this)
        .find(".transition-current-state")
        .val()
        .trim();
      const readSymbol = $(this).find(".transition-read").val().trim();
      const nextState = $(this).find(".transition-next-state").val().trim();
      const writeSymbol = $(this).find(".transition-write").val().trim();
      const move = $(this).find(".transition-move").val();

      if (currentState && readSymbol && nextState && writeSymbol) {
        transitions.push({
          current_state: currentState,
          read_symbol: readSymbol,
          next_state: nextState,
          write_symbol: writeSymbol,
          move: move,
        });
      }
    });

    if (transitions.length === 0) {
      showAlert("Please add valid transitions", "danger");
      return;
    }

    // Prepare data
    const machineData = {
      name: $("#machineName").val().trim(),
      states: $("#machineStates").val().trim(),
      input_alphabet: $("#inputAlphabet").val().trim(),
      tape_alphabet: $("#tapeAlphabet").val().trim(),
      blank: $("#blankSymbol").val().trim(),
      initial_state: $("#initialState").val().trim(),
      final_states: $("#finalStates").val().trim(),
      transitions: transitions,
    };

    // Send request
    $.ajax({
      url: "/api/machines/create",
      method: "POST",
      contentType: "application/json",
      data: JSON.stringify(machineData),
      success: function (response) {
        showAlert(response.message, "success");
        // Reset form after successful creation
        setTimeout(() => {
          $("#resetBtn").click();
        }, 2000);
      },
      error: function (xhr) {
        const error = xhr.responseJSON
          ? xhr.responseJSON.error
          : "Unknown error occurred";
        showAlert("Error: " + error, "danger");
      },
    });
  });

  // Show alert function
  function showAlert(message, type) {
    const alert = $(`
      <div class="alert alert-${type} alert-dismissible fade show" role="alert">
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      </div>
    `);

    $(".alert-area").append(alert);

    // Auto dismiss after 5 seconds
    setTimeout(() => {
      alert.alert("close");
    }, 5000);
  }

  // Initialize
  updatePreview();
});
