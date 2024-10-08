const result = document.querySelector("#result");
const errorSound = new Audio("/static/audio/error.mp3");

// play an error sound if the result has an error
result?.addEventListener('htmx:afterSwap', async (_) => {
  if (!result.querySelector("#error")) return
  errorSound.volume = 0.65;
  errorSound.play()
});
