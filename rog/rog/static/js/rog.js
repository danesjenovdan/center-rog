function labsHoverAnimations() {
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

function carousel() {
  const slider = tns({
    container: ".tiny-slider-carousel",
    items: 5,
    slideBy: 1,
    // autoplay: true,
    loop: false,
    center: true,
    mouseDrag: true,
    nav: false,
    // controls: false,
    autoplayButtonOutput: false,
    onInit(info) {
      const h = getComputedStyle(info.container)["height"];
      info.container.style.height = `${parseInt(h) * 2}px`;
      onSliderIndexChanged(info);
    },
  });

  slider.events.on("indexChanged", (info) => {
    onSliderIndexChanged(info);
  });
}

function onSliderIndexChanged(info) {
  [...info.slideItems].forEach((item) => {
    item.classList.remove(
      "active-prev2",
      "active-prev1",
      "active",
      "active-next1",
      "active-next2"
    );
  });

  info.slideItems[info.index - 2]?.classList.add("active-prev2");
  info.slideItems[info.index - 1]?.classList.add("active-prev1");
  info.slideItems[info.index].classList.add("active");
  info.slideItems[info.index + 1]?.classList.add("active-next1");
  info.slideItems[info.index + 2]?.classList.add("active-next2");
}

function scrollingDots(section, container) {
  const eventsSectionDots = document.querySelectorAll(`.${section} .scrolling-dots span`);
  const eventsSectionScrollable = document.querySelector(`.${section} .${container}`);

  eventsSectionDots[0].addEventListener("click", () => {
    eventsSectionScrollable.scrollTo({
      left: 0,
      behavior: "smooth",
    })
  });

  eventsSectionDots[1].addEventListener("click", () => {
    console.log(eventsSectionScrollable.scrollWidth)
    console.log(eventsSectionScrollable.offsetWidth)
    eventsSectionScrollable.scrollTo({
      left: (eventsSectionScrollable.scrollWidth - eventsSectionScrollable.offsetWidth) / 2,
      behavior: "smooth",
    })
  });

  eventsSectionDots[2].addEventListener("click", () => {
    eventsSectionScrollable.scrollTo({
      left: eventsSectionScrollable.scrollWidth,
      behavior: "smooth",
    })
  });
}

document.addEventListener("DOMContentLoaded", () => {
  labsHoverAnimations();
  //carousel();
  scrollingDots("events-section", "events-container");
  scrollingDots("studios-section", "studios-container");
  scrollingDots("news-section", "news-container");
});
