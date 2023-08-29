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

function carousel() {
  const elements = document.querySelectorAll(".glide");
  elements.forEach((element, i) => {
    const count = element.querySelectorAll(".glide__slide").length;
    if (count > 0) {
      const startIndex = count >= 5 ? 2 : Math.floor(count / 2);
      const glide = new Glide(element, {
        startAt: startIndex,
        perView: 5,
        focusAt: "center",
        rewind: false,
        gap: 0,
        animationDuration: 150,
        breakpoints: {
          600: {
            perView: 3,
          },
        },
      });
      glide.on(["mount.after", "resize"], () => {
        const track = glide.selector.querySelector(".glide__track");
        track.style.aspectRatio = `${glide.settings.perView} / 2`;
      });
      glide.on(["mount.after", "run.after"], () => {
        const items = glide.selector.querySelectorAll(".glide__slide");
        items.forEach((item) => {
          item.classList.remove(
            "glide__slide--active-prev2",
            "glide__slide--active-prev1",
            "glide__slide--active-next1",
            "glide__slide--active-next2"
          );
        });
        items[glide.index - 2]?.classList.add("glide__slide--active-prev2");
        items[glide.index - 1]?.classList.add("glide__slide--active-prev1");
        items[glide.index + 1]?.classList.add("glide__slide--active-next1");
        items[glide.index + 2]?.classList.add("glide__slide--active-next2");
      });
      glide.mount();
    }
  });
}

function scrollingDots(section, container) {
  const eventsSectionDots = document.querySelectorAll(`${section} .scrolling-dots span`);
  const eventsSectionScrollable = document.querySelector(`${section} ${container}`);

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

  carousel();

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
