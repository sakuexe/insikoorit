/** @type {HTMLInputElement | null | undefined} */
const fileInput = evaluationForm?.querySelector('input[name="file"]');
if (!fileInput) throw new Error("no fileinput field was found");

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

function hideResults() {
  /** @type {HTMLOutputElement | null }*/
  const results = document.querySelector("output#result");
  if (!results) throw new Error("No output#result element was found");

  results.innerHTML = "";
}
