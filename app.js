const task = document.querySelector("#task");
const level = document.querySelector("#level");
const hoursWrap = document.querySelector("#hours-wrap");
const hours = document.querySelector("#hours");
const input = document.querySelector("#input-text");
const inputLabel = document.querySelector("#input-label");
const submitBtn = document.querySelector("#submit-btn");
const statusEl = document.querySelector("#status");
const resultCard = document.querySelector("#result-card");
const result = document.querySelector("#result");
const quizResult = document.querySelector("#quiz-result");
const copyBtn = document.querySelector("#copy-btn");

const taskMeta = {
  qa: { label: "Your question", placeholder: "Example: Why does the sky look blue?", button: "Ask EduGenie" },
  explain: { label: "Concept", placeholder: "Example: Explain recursion in Python.", button: "Explain concept" },
  quiz: { label: "Passage", placeholder: "Paste at least a short educational passage here...", button: "Generate 3-question quiz" },
  summarize: { label: "Text to summarize", placeholder: "Paste the educational text you want summarized...", button: "Summarize" },
  learn: { label: "Topic", placeholder: "Example: SQL from beginner to advanced", button: "Build learning path" }
};

function updateTaskUI() {
  const meta = taskMeta[task.value];
  inputLabel.textContent = meta.label;
  input.placeholder = meta.placeholder;
  submitBtn.textContent = meta.button;
  hoursWrap.classList.toggle("hidden", task.value !== "learn");
  resultCard.classList.add("hidden");
  quizResult.innerHTML = "";
  result.textContent = "";
}
task.addEventListener("change", updateTaskUI);
updateTaskUI();

async function request(path, body) {
  const response = await fetch(path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.detail || "Request failed");
  return data;
}

function renderQuiz(quiz) {
  result.textContent = "";
  quizResult.innerHTML = "";
  quiz.questions.forEach((q, index) => {
    const box = document.createElement("div");
    box.className = "quiz-question";
    const title = document.createElement("h3");
    title.textContent = `${index + 1}. ${q.question}`;
    box.appendChild(title);

    q.options.forEach(option => {
      const button = document.createElement("button");
      button.className = "quiz-option";
      button.textContent = option;
      button.addEventListener("click", () => {
        [...box.querySelectorAll(".quiz-option")].forEach(b => b.disabled = true);
        if (option === q.answer) {
          button.classList.add("correct");
          feedback.textContent = "Correct!";
        } else {
          button.classList.add("wrong");
          feedback.textContent = `Not quite. Correct answer: ${q.answer}`;
        }
        explanation.textContent = q.explanation || "";
      });
      box.appendChild(button);
    });

    const feedback = document.createElement("p");
    feedback.className = "status";
    box.appendChild(feedback);
    const explanation = document.createElement("p");
    explanation.className = "status";
    box.appendChild(explanation);
    quizResult.appendChild(box);
  });
}

submitBtn.addEventListener("click", async () => {
  const text = input.value.trim();
  if (!text) {
    statusEl.textContent = "Please enter something first.";
    return;
  }

  submitBtn.disabled = true;
  statusEl.textContent = "EduGenie is thinking...";
  resultCard.classList.remove("hidden");
  result.textContent = "";
  quizResult.innerHTML = "";

  try {
    let data;
    if (task.value === "qa") {
      data = await request("/qa", { question: text, level: level.value });
      result.textContent = data.answer;
    } else if (task.value === "explain") {
      data = await request("/explain", { topic: text, level: level.value });
      result.textContent = data.explanation;
    } else if (task.value === "quiz") {
      data = await request("/quiz", { text, level: level.value });
      renderQuiz(data.quiz);
    } else if (task.value === "summarize") {
      data = await request("/summarize", { text, level: level.value });
      result.textContent = data.summary;
    } else {
      data = await request("/learn/recommendations", {
        topic: text, level: level.value, hours_per_week: Number(hours.value)
      });
      result.textContent = data.recommendations;
    }
    statusEl.textContent = "Done.";
  } catch (error) {
    result.textContent = `Error: ${error.message}`;
    statusEl.textContent = "The request could not be completed.";
  } finally {
    submitBtn.disabled = false;
  }
});

copyBtn.addEventListener("click", async () => {
  const text = result.textContent || quizResult.innerText;
  if (!text) return;
  await navigator.clipboard.writeText(text);
  statusEl.textContent = "Copied.";
});
