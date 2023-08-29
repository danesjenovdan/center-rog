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
  const collapsable_menu = document.getElementById("navbar-collapsable-menu");
  const secondary_navigation = document.getElementById("secondary-navigation");

  collapsable_menu.addEventListener("hide.bs.collapse", (event) => {
    document.getElementById("primary-navigation").classList.toggle("custom-navigation-show");
    document.getElementById("logo-navigation").classList.toggle("custom-navigation-show");

    if (secondary_navigation) {
      secondary_navigation.classList.toggle("custom-navigation-show");
    }
  });

  collapsable_menu.addEventListener("show.bs.collapse", (event) => {
    document.getElementById("primary-navigation").classList.toggle("custom-navigation-show");
    document.getElementById("logo-navigation").classList.toggle("custom-navigation-show");

    if (secondary_navigation) {
      secondary_navigation.classList.toggle("custom-navigation-show");
    }
  });

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
