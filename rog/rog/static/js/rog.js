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
  }
  if (header_marquee) {
    header_marquee.style.transform = `rotate(${angle}deg)`;
    header_marquee.style.top = secondary_navigation
      ? `${secondary_navigation.offsetHeight + nav_bg_left_height - 4}px`
      : `${nav_bg_left_height - 2}px`;
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

    function resizeImages() {
      const maxWidth = gallery.offsetWidth * 0.66;
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

        if (imageRatio > containerRatio) {
          image.style.width = `${maxWidth}px`;
          image.style.height = "auto";
        } else {
          image.style.width = "auto";
          image.style.height = `${maxHeight}px`;
        }

        image.style.top = `${(maxHeight - image.offsetHeight) / 2}px`;
        image.style.bottom = "auto";
        if (i === activeIndex && item.classList.contains("active")) {
          image.setAttribute("tabindex", "0");
          image.style.transformOrigin = "center center";
          image.style.left = `${(gallery.offsetWidth - image.offsetWidth) / 2}px`;
          image.style.right = "auto";
        } else if (i < activeIndex) {
          image.removeAttribute("tabindex");
          image.style.transformOrigin = "center left";
          if (item.classList.contains("prev1")) {
            image.style.left = "8.25%";
            image.style.right = "auto";
          } else if (item.classList.contains("prev2")) {
            image.style.left = "0";
            image.style.right = "auto";
          } else {
            image.style.left = `${-gallery.offsetWidth}px`;
            image.style.right = "auto";
          }
        } else if (i > activeIndex) {
          image.removeAttribute("tabindex");
          image.style.transformOrigin = "center right";
          if (item.classList.contains("next1")) {
            image.style.left = "auto";
            image.style.right = "8.25%";
          } else if (item.classList.contains("next2")) {
            image.style.left = "auto";
            image.style.right = "0";
          } else {
            image.style.left = "auto";
            image.style.right = `${-gallery.offsetWidth}px`;
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
      const scrollbarWidth = eventsSectionScrollable.offsetHeight - eventsSectionScrollable.clientHeight;
      scrollbarHider.style.height = `${eventsSectionScrollable.offsetHeight - scrollbarWidth}px`;
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

document.addEventListener("DOMContentLoaded", () => {
  rotateNavbar();

  gallery();

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
});
