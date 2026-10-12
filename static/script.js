document.addEventListener("DOMContentLoaded", () => {
  const buttons = document.querySelectorAll("button");

  buttons.forEach((button) => {
    button.addEventListener("click", async (event) => {
      // Only target buttons related to assignments or actions
      if (button.textContent.includes("Open assignment") || button.classList.contains("theme-btn") == false) {
        try {
          const response = await fetch("http://127.0.0.1:8000/assignments");
          const data = await response.json();
          console.log("Backend Assignments Data:", data);
          alert(`Successfully fetched ${data.length} assignments from FastAPI backend!`);
        } catch (error) {
          console.error("Failed to connect to backend:", error);
          alert("Could not reach backend API.");
        }
      }
    });
  });
});