const eventKey = "revenue_os_events";
const langKey = "revenue_os_lang";

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

document.addEventListener("click", async (event) => {
  const target = event.target.closest("[data-copy-email]");
  if (!target) return;
  const email = target.dataset.copyEmail;
  const status = document.querySelector("[data-copy-status]");
  try {
    await navigator.clipboard.writeText(email);
    if (status) status.textContent = "Email copied.";
  } catch {
    if (status) status.textContent = email;
  }
});

document.addEventListener("submit", (event) => {
  const form = event.target.closest("form[data-lead-form]");
  if (!form) return;
  event.preventDefault();
  const data = Object.fromEntries(new FormData(form).entries());
  recordEvent("lead_form_submit", data);
  const status = form.querySelector("[data-form-status]");
  const endpoint = form.dataset.formEndpoint;
  if (endpoint) {
    fetch(endpoint, {
      method: "POST",
      headers: { "Accept": "application/json" },
      body: new FormData(form)
    })
      .then((response) => {
        if (!response.ok) throw new Error("Form endpoint error");
        form.reset();
        if (status) status.textContent = currentLang() === "ru" ? "Запрос отправлен." : "Request sent.";
      })
      .catch(() => {
        if (status) status.textContent = currentLang() === "ru" ? "Не удалось отправить форму. Скопируйте email ниже." : "Form submit failed. Please copy the email below.";
      });
    return;
  }
  const recipient = form.dataset.recipientEmail || "tech.it.rooster@yandex.ru";
  const subject = currentLang() === "ru" ? "Технический запрос" : "Technical assessment request";
  const body = [
    `Name: ${data.name || ""}`,
    `Email: ${data.email || ""}`,
    `Company: ${data.company || ""}`,
    "",
    data.message || ""
  ].join("\n");
  window.location.href = `mailto:${recipient}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
  if (status) {
    status.textContent = currentLang() === "ru" ? "Открываю подготовленное письмо." : "Opening a prepared email.";
  }
});

function setText(id, text) {
  const element = document.getElementById(id);
  if (element) element.textContent = text;
}

function currentLang() {
  return localStorage.getItem(langKey) || "en";
}

function applyLang(lang) {
  localStorage.setItem(langKey, lang);
  document.documentElement.lang = lang;
  document.querySelectorAll("[data-en][data-ru]").forEach((element) => {
    element.innerHTML = element.dataset[lang];
  });
  const toggle = document.querySelector("[data-lang-switch]");
  if (toggle) toggle.textContent = lang === "ru" ? "EN" : "RU";
}

document.addEventListener("click", (event) => {
  const target = event.target.closest("[data-lang-switch]");
  if (!target) return;
  applyLang(currentLang() === "ru" ? "en" : "ru");
});

applyLang(currentLang());

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
