const infoOutput = document.querySelector("#info-output");
const mathOutput = document.querySelector("#math-output");
const refreshBtn = document.querySelector("#refresh-info");
const form = document.querySelector("#math-form");

const endpoints = {
  root: "/api/",
  health: "/api/health",
  info: "/api/info",
  env: "/api/env",
  math: (operation, a, b) => `/api/${operation}/${a}/${b}`,
};

async function fetchJson(url, options) {
  const response = await fetch(url, options);
  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({}));
    throw new Error(
      errorBody.error || `Запрос завершился с ошибкой ${response.status}`
    );
  }
  return response.json();
}

async function refreshInfo() {
  infoOutput.textContent = "Загрузка...";
  try {
    const [rootData, healthData, envData] = await Promise.all([
      fetchJson(endpoints.root),
      fetchJson(endpoints.health),
      fetchJson(endpoints.env),
    ]);
    infoOutput.textContent = JSON.stringify(
      {
        message: rootData.message,
        endpoints: rootData.endpoints,
        health: healthData,
        env: envData.env,
      },
      null,
      2
    );
  } catch (error) {
    infoOutput.textContent = error.message;
  }
}

refreshBtn.addEventListener("click", (event) => {
  event.preventDefault();
  refreshInfo();
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  mathOutput.textContent = "Выполняю операцию...";
  const formData = new FormData(form);
  const operation = formData.get("operation");
  const a = formData.get("a");
  const b = formData.get("b");

  try {
    const result = await fetchJson(endpoints.math(operation, a, b));
    mathOutput.textContent = JSON.stringify(result, null, 2);
  } catch (error) {
    mathOutput.textContent = error.message;
  }
});

refreshInfo();

