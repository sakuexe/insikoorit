/** @type {HTMLFormElement | null} */
const evaluationForm = document.querySelector('form[action="/evaluate"]');
/** @type {HTMLInputElement | null | undefined} */
const fileInput = evaluationForm?.querySelector('input[name="file"]');

if (!fileInput) throw new Error("no fileinput field was found");

// by default, hide the results
hideResults()

fileInput?.addEventListener("change", () => {
/** @type {HTMLImageElement | null} */
  const imagePreview = document.querySelector("#image-preview > img");
  if (!imagePreview) throw new Error("No image preview was found")
  if (!fileInput.files) return

  const file = fileInput.files[0];
  const reader = new FileReader();

  /** @param {ProgressEvent<FileReader>} e */
  reader.onload = (e) => {
    imagePreview.src = e.target?.result?.toString() ?? "";
  };
  reader.readAsDataURL(file || new Blob());

  // hide the scores when the image changes
  hideResults();
});

evaluationForm?.addEventListener("submit", async (e) => {
  e.preventDefault();
  const formData = new FormData(evaluationForm)
  try {
    const response = await fetch(evaluationForm.action, {
      method: "POST",
      body: formData
    });

    if (!response.ok) throw new Error("not okay response")

    const data = await response.json();
    //console.log(data);
    displayData(data)

  } catch (error) {
    console.error(error)
    throw new Error("something fucked up");
  }
})

/** 
 * @typedef {Object} EvaluationData
 * @property {string} type
 * @property {number} score
 */

/** @param {EvaluationData} data */
function displayData(data) {
  /** @type {HTMLParagraphElement | null }*/
  const typeElement = document.querySelector("#type > .value");
  /** @type {HTMLParagraphElement | null }*/
  const scoreElement = document.querySelector("#score > .value");

  if (!typeElement) throw new Error("No element for type was found");
  if (!scoreElement) throw new Error("No element for score was found");

  typeElement.innerText = data.type;
  scoreElement.innerText = data.score.toString();
  showResults();
}

function hideResults() {
  /** @type {HTMLDivElement | null }*/
  const results = document.querySelector("output#result");
  if (!results) throw new Error("No output#result element was found");

  results.style.setProperty("opacity", "0");
}

function showResults() {
  /** @type {HTMLDivElement | null }*/
  const results = document.querySelector("output#result");
  if (!results) throw new Error("No output#result element was found");

  results.style.setProperty("opacity", "100");
}
