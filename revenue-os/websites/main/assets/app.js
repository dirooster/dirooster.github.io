const eventKey = "revenue_os_events";

function recordEvent(type, payload = {}) {
  const event = {
    type,
    payload,
    path: window.location.pathname,
    at: new Date().toISOString()
  };
  const existing = JSON.parse(localStorage.getItem(eventKey) || "[]");
  existing.push(event);
  localStorage.setItem(eventKey, JSON.stringify(existing.slice(-200)));
}

document.addEventListener("click", (event) => {
  const target = event.target.closest("[data-track]");
  if (!target) return;
  recordEvent("cta_click", {
    label: target.dataset.track,
    href: target.getAttribute("href") || ""
  });
});

document.addEventListener("submit", (event) => {
  const form = event.target.closest("form[data-lead-form]");
  if (!form) return;
  event.preventDefault();
  const data = Object.fromEntries(new FormData(form).entries());
  recordEvent("lead_form_submit", data);
  form.reset();
  const status = form.querySelector("[data-form-status]");
  if (status) {
    status.textContent = "Draft captured locally. Connect email/CRM before external submission.";
  }
});

function setText(id, text) {
  const element = document.getElementById(id);
  if (element) element.textContent = text;
}

window.runAiDemo = function runAiDemo() {
  const findings = [
    "No regression dataset attached to release flow.",
    "Tool failure handling is implicit and not measured.",
    "Latency budget is missing for multi-step agent runs.",
    "Human approval boundary is unclear for high-impact actions."
  ];
  const plan = {
    risk_level: "medium-high",
    next_step: "Build a 30-case eval set and trace tool-call failures before expanding usage.",
    audit_items: findings
  };
  setText("ai-demo-output", JSON.stringify(plan, null, 2));
};

window.runLogisticsDemo = function runLogisticsDemo() {
  const extraction = {
    shipment_reference: "SYN-2408-17",
    origin: "Rotterdam",
    destination: "Munich",
    goods: "industrial sensors",
    exception: "missing delivery appointment",
    human_review_required: true
  };
  setText("logistics-demo-output", JSON.stringify(extraction, null, 2));
};

