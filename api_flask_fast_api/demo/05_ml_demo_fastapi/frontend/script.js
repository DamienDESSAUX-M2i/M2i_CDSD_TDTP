const API_BASE_URL = "http://127.0.0.1:8000";
const PREDICT_URL = `${API_BASE_URL}/predict-intent`;
const HISTORY_URL = `${API_BASE_URL}/predictions`;

const form = document.getElementById("prediction-form");
const resultCard = document.getElementById("result-card");
const resultContainer = document.getElementById("result");
const historyContainer = document.getElementById("history");
const refreshHistoryButton = document.getElementById("refresh-history");

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const firstName = document.getElementById("firstName").value.trim();
  const message = document.getElementById("message").value.trim();
  const submitButton = form.querySelector("button[type='submit']");

  if (!firstName || !message) {
    return;
  }

  submitButton.disabled = true;
  submitButton.textContent = "Envoi en cours...";

  try {
    const response = await fetch(PREDICT_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        first_name: firstName,
        text: message
      })
    });

    if (!response.ok) {
      throw new Error("Erreur lors de l'appel à l'API");
    }

    const data = await response.json();
    renderResult(data);
    await loadHistory();
  } catch (error) {
    resultCard.classList.remove("hidden");
    resultContainer.innerHTML = `<div class="result-item">Erreur : ${error.message}</div>`;
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = "Envoyer à l'API";
  }
});

refreshHistoryButton.addEventListener("click", loadHistory);

function renderResult(data) {
  resultCard.classList.remove("hidden");

  const scoresHtml = Object.entries(data.all_scores)
    .sort((a, b) => b[1] - a[1])
    .map(([label, score]) => `
      <div class="score-item">
        <strong>${label}</strong> : ${(score * 100).toFixed(2)} %
      </div>
    `)
    .join("");

  resultContainer.innerHTML = `
    <div class="result-grid">
      <div class="result-item"><strong>ID en base :</strong> ${data.id}</div>
      <div class="result-item"><strong>Prénom :</strong> ${escapeHtml(data.first_name)}</div>
      <div class="result-item"><strong>Texte :</strong> ${escapeHtml(data.text)}</div>
      <div class="result-item"><strong>Classement :</strong> <span class="label-badge">${data.predicted_label}</span></div>
      <div class="result-item"><strong>Confiance :</strong> ${(data.confidence * 100).toFixed(2)} %</div>
      <div class="result-item"><strong>Créé le :</strong> ${new Date(data.created_at).toLocaleString()}</div>
    </div>
    <h3>Scores détaillés</h3>
    <div class="score-list">${scoresHtml}</div>
  `;
}

async function loadHistory() {
  try {
    const response = await fetch(HISTORY_URL);

    if (!response.ok) {
      throw new Error("Impossible de charger l'historique");
    }

    const items = await response.json();

    if (!items.length) {
      historyContainer.innerHTML = '<div class="history-empty">Aucune prédiction enregistrée pour le moment.</div>';
      return;
    }

    historyContainer.innerHTML = `
      <div class="history-list">
        ${items.map((item) => `
          <div class="history-item">
            <div><strong>#${item.id}</strong> - <strong>${escapeHtml(item.first_name)}</strong></div>
            <div class="small">${new Date(item.created_at).toLocaleString()}</div>
            <div>${escapeHtml(item.message)}</div>
            <div><strong>Catégorie :</strong> ${item.predicted_label}</div>
            <div><strong>Confiance :</strong> ${(item.confidence * 100).toFixed(2)} %</div>
          </div>
        `).join("")}
      </div>
    `;
  } catch (error) {
    historyContainer.innerHTML = `<div class="history-empty">Erreur : ${error.message}</div>`;
  }
}

function escapeHtml(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

loadHistory();
