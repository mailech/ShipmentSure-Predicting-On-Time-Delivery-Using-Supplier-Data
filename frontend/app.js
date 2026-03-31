const endpoints = {
  health: "/api/health",
  schema: "/api/schema",
  predict: "/api/predict",
};

const form = document.getElementById("prediction-form");
const formState = document.getElementById("form-state");
const fillDefaultsButton = document.getElementById("fill-defaults");
const resultEmpty = document.getElementById("result-empty");
const resultContent = document.getElementById("result-content");
const confidenceValue = document.getElementById("confidence-value");
const scoreRing = document.getElementById("score-ring");
const predictionLabel = document.getElementById("prediction-label");
const predictionClass = document.getElementById("prediction-class");
const predictionMessage = document.getElementById("prediction-message");
const probabilityBars = document.getElementById("probability-bars");
const apiStatus = document.getElementById("api-status");

let schemaResponse = null;

function prettifyFieldName(name) {
  return name
    .replaceAll("_", " ")
    .replaceAll(".", " ")
    .replace(/\b\w/g, (char) => char.toUpperCase());
}

function setApiStatus(text, tone) {
  apiStatus.textContent = text;
  apiStatus.className = `pill ${tone}`;
}

function setFormState(text) {
  formState.textContent = text;
}

function setLoading(isLoading) {
  const controls = form.querySelectorAll("input, select, button");
  controls.forEach((control) => {
    control.disabled = isLoading;
  });
}

async function fetchJson(url, options = {}) {
  const response = await fetch(url, options);
  if (!response.ok) {
    let detail = `Request failed with status ${response.status}`;
    try {
      const body = await response.json();
      if (typeof body.detail === "string") {
        detail = body.detail;
      } else if (Array.isArray(body.detail)) {
        detail = body.detail.map((item) => item.msg || JSON.stringify(item)).join("; ");
      }
    } catch (_error) {
      // Keep fallback error message if body is not JSON.
    }
    throw new Error(detail);
  }
  return response.json();
}

function buildField(field) {
  const wrapper = document.createElement("label");
  wrapper.className = "field";

  const titleRow = document.createElement("div");
  titleRow.className = "field-title";

  const title = document.createElement("span");
  title.textContent = prettifyFieldName(field.name);
  titleRow.appendChild(title);

  if (field.type === "number") {
    const range = document.createElement("span");
    range.className = "field-range";
    range.textContent = `${field.min} to ${field.max}`;
    titleRow.appendChild(range);
  }

  wrapper.appendChild(titleRow);

  let control;
  if (field.type === "select") {
    control = document.createElement("select");
    field.options.forEach((optionValue) => {
      const option = document.createElement("option");
      option.value = optionValue;
      option.textContent = optionValue;
      if (optionValue === field.default) {
        option.selected = true;
      }
      control.appendChild(option);
    });
  } else {
    control = document.createElement("input");
    control.type = "number";
    control.min = String(field.min);
    control.max = String(field.max);
    control.step = String(field.step || 1);
    control.value = String(field.default);
    control.required = true;
  }

  control.name = field.name;
  control.id = field.name;
  wrapper.appendChild(control);

  return wrapper;
}

function renderForm(fields) {
  form.innerHTML = "";

  fields.forEach((field) => {
    form.appendChild(buildField(field));
  });

  const actions = document.createElement("div");
  actions.className = "form-actions";

  const submitButton = document.createElement("button");
  submitButton.type = "submit";
  submitButton.className = "primary-btn";
  submitButton.textContent = "Predict Outcome";

  actions.appendChild(submitButton);
  form.appendChild(actions);
}

function applyDefaults() {
  if (!schemaResponse) {
    return;
  }

  schemaResponse.raw_fields.forEach((field) => {
    const control = form.elements.namedItem(field.name);
    if (!control) {
      return;
    }

    control.value = String(field.default);
  });
}

function collectPayload() {
  if (!schemaResponse) {
    throw new Error("Schema is not ready yet");
  }

  const payload = {};

  schemaResponse.raw_fields.forEach((field) => {
    const control = form.elements.namedItem(field.name);
    if (!control) {
      return;
    }

    if (field.type === "number") {
      payload[field.name] = Number(control.value);
    } else {
      payload[field.name] = String(control.value).trim();
    }
  });

  return payload;
}

function renderProbabilityBars(probabilities) {
  probabilityBars.innerHTML = "";

  const entries = Object.entries(probabilities || {}).sort((a, b) => Number(b[1]) - Number(a[1]));

  if (!entries.length) {
    const fallback = document.createElement("p");
    fallback.textContent = "This model output does not expose class probabilities.";
    fallback.style.margin = "0";
    fallback.style.color = "var(--text-soft)";
    probabilityBars.appendChild(fallback);
    return;
  }

  entries.forEach(([label, value]) => {
    const pct = Math.max(0, Math.min(100, Math.round(Number(value) * 100)));

    const item = document.createElement("div");
    item.className = "prob-item";

    const head = document.createElement("div");
    head.className = "prob-head";

    const labelText = document.createElement("span");
    labelText.textContent = `Class ${label}`;

    const pctText = document.createElement("span");
    pctText.textContent = `${pct}%`;

    head.appendChild(labelText);
    head.appendChild(pctText);

    const track = document.createElement("div");
    track.className = "prob-track";

    const fill = document.createElement("span");
    fill.className = "prob-fill";
    fill.style.width = `${pct}%`;

    track.appendChild(fill);
    item.appendChild(head);
    item.appendChild(track);
    probabilityBars.appendChild(item);
  });
}

function renderResult(result) {
  const confidencePct = Math.max(0, Math.min(100, Math.round(Number(result.confidence || 0) * 100)));

  confidenceValue.textContent = `${confidencePct}%`;
  scoreRing.style.setProperty("--score", `${confidencePct}%`);

  predictionLabel.textContent = result.prediction_label || "Prediction";
  predictionClass.textContent = String(result.prediction);
  predictionMessage.textContent = `${result.message || "Prediction generated."} ${
    result.target_hint || ""
  }`.trim();

  renderProbabilityBars(result.class_probabilities);

  resultEmpty.classList.add("hidden");
  resultContent.classList.remove("hidden");
}

async function checkHealth() {
  try {
    const health = await fetchJson(endpoints.health);
    setApiStatus("API Live", "ok");
    return health;
  } catch (error) {
    setApiStatus("API Unreachable", "error");
    throw error;
  }
}

async function initialize() {
  try {
    setFormState("Checking backend and loading model schema...");
    await checkHealth();

    schemaResponse = await fetchJson(endpoints.schema);
    renderForm(schemaResponse.raw_fields);
    applyDefaults();

    setFormState("Schema loaded. Enter shipment details and run prediction.");
  } catch (error) {
    setFormState(`Startup error: ${error.message}`);
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  try {
    setLoading(true);
    setFormState("Running prediction...");

    const payload = collectPayload();
    const result = await fetchJson(endpoints.predict, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    renderResult(result);
    setFormState("Prediction completed successfully.");
  } catch (error) {
    setFormState(`Prediction failed: ${error.message}`);
  } finally {
    setLoading(false);
  }
});

fillDefaultsButton.addEventListener("click", () => {
  applyDefaults();
  setFormState("Default sample values loaded.");
});

initialize();
