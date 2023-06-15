async function start() {
  console.log("rog.js");

  const labs = document.querySelectorAll(".labs-section .lab");
  labs.forEach((lab) => {
    lab.addEventListener("mouseenter", onLabEnter);
  });
}

function onLabEnter(event) {
  const img = event.currentTarget.querySelector("img");
  const video = event.currentTarget.querySelector("video");

  if (!video) {
    return;
  }

  video.currentTime = 0;
  video.play();
  video.addEventListener("ended", () => onVideoEnded(img, video));

  img.style.opacity = "0";
}

function onVideoEnded(img, video) {
  img.style.opacity = "1";

  video.pause();
  video.currentTime = 0;
}

document.addEventListener("DOMContentLoaded", () => {
  start();
});
