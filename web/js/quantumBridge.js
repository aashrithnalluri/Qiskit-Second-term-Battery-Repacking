/**
 * Platform-neutral interface for RePack-Q's quantum Python functions.
 *
 * A Qollab-specific bootstrap must register the adapter only after its exact
 * Python invocation mechanism has been verified. No Qollab globals or API
 * names are assumed here.
 */

const ADAPTER_KEY = "__REPACKQ_RUNTIME_ADAPTER__";

function getAdapter() {
  return globalThis[ADAPTER_KEY] ?? null;
}

export function registerRuntimeAdapter(adapter) {
  if (!adapter || typeof adapter.getCapabilities !== "function" || typeof adapter.runSmokeTest !== "function") {
    throw new TypeError("Runtime adapter must implement getCapabilities() and runSmokeTest().");
  }
  globalThis[ADAPTER_KEY] = adapter;
}

export async function getCapabilities() {
  const adapter = getAdapter();
  if (!adapter) {
    return {
      available: false,
      bridge: "repackq-runtime-adapter-v1",
      message: "No verified Qollab or local Python adapter is registered in this host.",
    };
  }
  return await adapter.getCapabilities();
}

export async function runSmokeTest() {
  const adapter = getAdapter();
  if (!adapter) {
    throw new Error("No verified Python runtime adapter is registered in this host.");
  }
  return await adapter.runSmokeTest();
}
