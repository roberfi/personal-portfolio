const container = document.getElementById("container");
const progressBar = document.getElementById("progress-bar");

export function initProgressBar() {
  // Event on scroll
  container.addEventListener("scroll", () => {
    // Set the progress of the progress bar
    progressBar.value =
      (container.scrollTop /
        (container.scrollHeight - container.clientHeight)) *
      100;
  });
}
