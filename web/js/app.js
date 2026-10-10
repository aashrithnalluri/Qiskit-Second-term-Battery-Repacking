import * as quantumBridge from "./quantumBridge.js";

const state = document.querySelector("#runtime-state");
const copy = document.querySelector("#runtime-copy");
const result = document.querySelector("#runtime-result");
const button = document.querySelector("#smoke-button");

function showJson(value) {
  result.textContent = JSON.stringify(value, null, 2);
}

async function initialize() {
  try {
    const capabilities = await quantumBridge.getCapabilities();
    showJson(capabilities);
    if (capabilities.available && capabilities.qiskit_available) {
      state.textContent = "Runtime ready";
      copy.textContent = "The registered Python runtime reports Qiskit support. Run the deterministic circuit check.";
      button.disabled = false;
    } else {
      state.textContent = "Adapter needed";
      copy.textContent = "The page loaded, but this browser has no verified Qollab Python adapter yet.";
    }
  } catch (error) {
    state.textContent = "Check failed";
    copy.textContent = "The runtime capability check returned an error.";
    showJson({ error: String(error?.message ?? error) });
  }
}

button.addEventListener("click", async () => {
  button.disabled = true;
  state.textContent = "Running";
  copy.textContent = "Waiting for the Python Qiskit smoke test.";
  try {
    showJson(await quantumBridge.runSmokeTest());
    state.textContent = "Passed";
    copy.textContent = "The deterministic circuit returned the expected result.";
  } catch (error) {
    state.textContent = "Failed";
    copy.textContent = "The smoke test could not complete.";
    showJson({ error: String(error?.message ?? error) });
  } finally {
    button.disabled = false;
  }
});

await initialize();
