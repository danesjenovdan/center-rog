function debounce(func, wait = 50) {
  let timeout;
  return function debounced() {
    const context = this;
    const args = arguments;
    const later = function () {
      timeout = null;
      func.apply(context, args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
    return timeout;
  };
}

function rotateNavbar() {
  const collapsable_menu = document.getElementById("navbar-collapsable-menu");
  const logo = document.getElementById("logo-navigation");
  const primary_navigation = document.getElementById("primary-navigation");

  collapsable_menu.addEventListener("show.bs.collapse", (event) => {
    collapsable_menu.style.opacity = "";
    logo.classList.add("custom-navigation-show");
    primary_navigation.classList.add("custom-navigation-show");
    updateNavBarAngle();
  });

  collapsable_menu.addEventListener("hide.bs.collapse", (event) => {
    logo.classList.remove("custom-navigation-show");
    primary_navigation.classList.remove("custom-navigation-show");
    updateNavBarAngle();
  });

  window.addEventListener("resize", debounce(updateNavBarAngle));
  updateNavBarAngle();
}

function updateNavBarAngle() {
  const nav_bg = document.getElementById("primary-navigation-background");
  const menu_open = nav_bg.parentElement.classList.contains("custom-navigation-show");

  let left_height = 0;
  let right_height = 0;
  if (menu_open) {
    left_height = 1;
    right_height = 0.9;
    if (window.innerWidth < 768) {
      left_height = 1;
      right_height = 1;
    }
  } else {
    left_height = 0;
    right_height = 0.5;
    if (window.innerWidth < 768) {
      left_height = 0.85;
    }
  }

  const nav_bg_left_height = left_height * nav_bg.offsetHeight;
  const nav_bg_right_height = right_height * nav_bg.offsetHeight;

  const x1 = 0;
  const y1 = nav_bg_left_height;
  const x2 = nav_bg.offsetWidth;
  const y2 = nav_bg_right_height;
  const angle = (Math.atan2(y2 - y1, x2 - x1) * 180) / Math.PI;

  const secondary_navigation = document.getElementById("secondary-navigation");
  const header_marquee = document.querySelector(".header-marquee");
  if (secondary_navigation) {
    secondary_navigation.style.transform = `rotate(${angle}deg)`;
    secondary_navigation.style.top = `${nav_bg_left_height - 2}px`;
    secondary_navigation.offsetWidth; // force layout before adding class to prevent animation
    secondary_navigation.classList.add("shown");
    document.body.classList.add("has-secondary-navigation");
  }
  if (header_marquee) {
    header_marquee.style.transform = `rotate(${angle}deg)`;
    header_marquee.style.top = secondary_navigation
      ? `${secondary_navigation.offsetHeight + nav_bg_left_height - 4}px`
      : `${nav_bg_left_height - 2}px`;
    header_marquee.offsetWidth; // force layout before adding class to prevent animation
    header_marquee.classList.add("shown");
    document.body.classList.add("has-header-marquee");
  }
}

function gallery() {
  const galleries = document.querySelectorAll(".custom-gallery");

  galleries.forEach((gallery) => {
    const items = Array.from(gallery.querySelectorAll(".custom-gallery-item"));
    const navArrows = Array.from(gallery.querySelectorAll(".custom-gallery-navigation"));
    const count = items.length;
    const startIndex = count >= 5 ? 2 : Math.floor(count / 2);
    let activeIndex = startIndex;

    items.forEach((item) => {
      const mc = new Hammer.Manager(item, {
        recognizers: [[Hammer.Swipe, { direction: Hammer.DIRECTION_HORIZONTAL }]],
      });

      mc.on("swipe", (event) => {
        if (event.direction === Hammer.DIRECTION_LEFT) {
          setActiveItem(activeIndex + 1);
        } else if (event.direction === Hammer.DIRECTION_RIGHT) {
          setActiveItem(activeIndex - 1);
        }
      });
    });

    function resizeImages() {
      const isMobile = gallery.offsetWidth < 600;
      const maxWidth = gallery.offsetWidth * (isMobile ? 0.85 : 0.66);
      const maxHeight = gallery.querySelector(".custom-gallery-image").offsetHeight;

      navArrows.forEach((nav) => {
        nav.style.top = `${maxHeight / 2}px`;
      });

      items.forEach((item, i) => {
        const image = item.querySelector(".custom-gallery-image img");
        const imageWidth = image.naturalWidth;
        const imageHeight = image.naturalHeight;
        const imageRatio = imageWidth / imageHeight;
        const containerRatio = maxWidth / maxHeight;

        item.style.zIndex = `${count + Math.abs(i - activeIndex) * -1}`;

        if (imageRatio > containerRatio) {
          image.style.width = `${maxWidth}px`;
          image.style.height = "auto";
        } else {
          image.style.width = "auto";
          image.style.height = `${maxHeight}px`;
        }

        const sideOffsetMult = isMobile ? 0.04125 : 0.0825;
        image.style.top = `${(maxHeight - image.offsetHeight) / 2}px`;
        image.style.bottom = "auto";
        image.style.right = "auto";
        if (i === activeIndex && item.classList.contains("active")) {
          image.setAttribute("tabindex", "0");
          image.style.transformOrigin = "center center";
          image.style.left = `${(gallery.offsetWidth - image.offsetWidth) / 2}px`;
        } else if (i < activeIndex) {
          image.removeAttribute("tabindex");
          image.style.transformOrigin = "center left";
          if (item.classList.contains("prev1")) {
            image.style.left = `${gallery.offsetWidth * sideOffsetMult}px`;
          } else if (item.classList.contains("prev2")) {
            image.style.left = "0";
          } else {
            image.style.left = "0";
          }
        } else if (i > activeIndex) {
          image.removeAttribute("tabindex");
          image.style.transformOrigin = "center right";
          if (item.classList.contains("next1")) {
            image.style.left = `${gallery.offsetWidth - image.offsetWidth - gallery.offsetWidth * sideOffsetMult}px`;
          } else if (item.classList.contains("next2")) {
            image.style.left = `${gallery.offsetWidth - image.offsetWidth}px`;
          } else {
            image.style.left = `${gallery.offsetWidth - image.offsetWidth}px`;
          }
        }
      });
    }

    function setActiveItem(index, focus = true) {
      if (index < 0 || index >= count) {
        return;
      }

      items.forEach((item) => {
        item.classList.remove("prev2", "prev1", "active", "next1", "next2");
      });
      items[index].classList.add("active");
      items[index - 2]?.classList.add("prev2");
      items[index - 1]?.classList.add("prev1");
      items[index + 1]?.classList.add("next1");
      items[index + 2]?.classList.add("next2");

      activeIndex = index;
      resizeImages();

      if (focus) {
        items[index].querySelector(".custom-gallery-image img").focus();
      }
    }

    window.addEventListener("resize", debounce(resizeImages));
    setActiveItem(startIndex, false);

    items.forEach((item) => {
      const image = item.querySelector(".custom-gallery-image img");
      image.addEventListener("click", () => {
        setActiveItem(items.indexOf(item));
      });
    });

    navArrows.forEach((nav) => {
      nav.addEventListener("click", (event) => {
        event.preventDefault();
        if (nav.classList.contains("prev")) {
          setActiveItem(activeIndex - 1);
        } else if (nav.classList.contains("next")) {
          setActiveItem(activeIndex + 1);
        }
      });
    });

    document.addEventListener("keydown", (event) => {
      if (!gallery.contains(document.activeElement)) {
        return;
      }
      if (event.key === "ArrowLeft") {
        event.preventDefault();
        setActiveItem(activeIndex - 1);
      } else if (event.key === "ArrowRight") {
        event.preventDefault();
        setActiveItem(activeIndex + 1);
      }
    });
  });
}

function scrollingDots(section, container) {
  const eventsSectionDots = document.querySelectorAll(`${section} .scrolling-dots span`);
  const eventsSectionScrollable = document.querySelector(`${section} ${container}`);

  const scrollbarHider = document.querySelector(`${section} .scrollbar-hider`);
  if (scrollbarHider) {
    function fixHiddenScrollbars() {
      eventsSectionScrollable.style.paddingBottom = "";
      const detectedScrollbarWidth = eventsSectionScrollable.offsetHeight - eventsSectionScrollable.clientHeight;
      const scrollbarWidth = Math.max(detectedScrollbarWidth, 24); // account for macOS overlay scrollbars
      scrollbarHider.style.height = `${eventsSectionScrollable.offsetHeight - detectedScrollbarWidth}px`;
      const scrollablePadding = parseFloat(getComputedStyle(eventsSectionScrollable).paddingBottom);
      eventsSectionScrollable.style.paddingBottom = `${scrollablePadding + scrollbarWidth}px`;
    }

    window.addEventListener("resize", debounce(fixHiddenScrollbars));
    fixHiddenScrollbars();
  }

  eventsSectionDots[0].addEventListener("click", () => {
    eventsSectionScrollable.scrollTo({
      left: 0,
      behavior: "smooth",
    });
  });

  eventsSectionDots[1].addEventListener("click", () => {
    eventsSectionScrollable.scrollTo({
      left: (eventsSectionScrollable.scrollWidth - eventsSectionScrollable.offsetWidth) / 2,
      behavior: "smooth",
    });
  });

  eventsSectionDots[2].addEventListener("click", () => {
    eventsSectionScrollable.scrollTo({
      left: eventsSectionScrollable.scrollWidth,
      behavior: "smooth",
    });
  });
}

function copyEmailButton() {
  const copyEmailButton = document.querySelectorAll(".copy-email-button");
  copyEmailButton.forEach((button) => {
    const confirmation = button.parentElement.querySelector(".copy-email-confirmation");

    button.addEventListener("click", async () => {
      button.disabled = true;

      const email = button.dataset.email;
      await navigator.clipboard.writeText(email);

      confirmation.classList.remove("d-none");
      setTimeout(() => {
        confirmation.classList.add("d-none");
        button.disabled = false;
      }, 2000);
    });
  });
}

function studioCardButtons() {
  const cards = document.querySelectorAll(".studio-card");
  cards.forEach((card) => {
    card.addEventListener("click", (e) => {
      const href = card.querySelector("a").getAttribute("href");
      window.location = href;
    });
  });
}

function preventDoubleSubmission() {
  const form = document.querySelector(".register-container form");
  if (form) {
    form.addEventListener("submit", function(event) {
      const submitButton = form.querySelector("button[type=submit]");
      setTimeout(function () {
        submitButton.disabled = true;
      }, 0);
    })
  }
}

document.addEventListener("DOMContentLoaded", () => {
  rotateNavbar();
  gallery();
  preventDoubleSubmission();

  if (document.querySelector(".events-section")) {
    scrollingDots(".events-section", ".events-container .row");
  }

  if (document.querySelector(".studios-section")) {
    scrollingDots(".studios-section", ".studios-container .row");
  }

  if (document.querySelector(".news-section")) {
    scrollingDots(".news-section", ".news-container .row");
  }

  copyEmailButton();

  const screenWidth = screen.width;
  if (screenWidth < 768 && document.querySelector(".template-studio-list")) {
    studioCardButtons();
  }
});

window.addEventListener("message", function (event) {
  if (event.origin === "https://oembed.jotform.com") {
    if (typeof event.data === "string") {
      if (event.data.startsWith("setHeight:")) {
        const [, height, jotformId] = event.data.split(":");
        const iframe = document.querySelector(`iframe[src*="jotform.com"][src*="${jotformId}"]`);
        if (iframe) {
          iframe.style.height = `${height}px`;
          return;
        }
      }
    }
    console.log("Message from jotform:", event.data);
  }
});

// Detect Safari
if (navigator.userAgent.includes("AppleWebKit") && !navigator.userAgent.includes("Chrome")) {
  document.body.classList.add("safari");
}

// Handle tab focus on input elements
(function () {
  let tabDown = false;
  window.addEventListener("keydown", (event) => {
    if (event.key === "Tab") {
      tabDown = true;
    }
  });

  window.addEventListener("keyup", (event) => {
    if (event.key === "Tab") {
      tabDown = false;
    }
  });

  window.addEventListener("blur", (event) => {
    tabDown = false;
  });

  document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === "hidden") {
      tabDown = false;
    }
  });

  document.addEventListener("focusin", (event) => {
    if (tabDown) {
      event.target.classList.add("tab-focused");
      event.target.addEventListener(
        "blur",
        (event) => {
          event.target.classList.remove("tab-focused");
        },
        { once: true }
      );
    }
  });
})();
