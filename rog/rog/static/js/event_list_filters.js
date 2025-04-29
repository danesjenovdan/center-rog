(function () {
  const eventListFilters = document.querySelectorAll(".event-list-filters");
  eventListFilters.forEach((eventListFilter) => {
    // toggle the dropdown when the button is clicked
    eventListFilter.addEventListener("click", (event) => {
      const targetButton = event.target.closest(".dropdown-button");
      if (!targetButton) return;

      const dropdown = targetButton.nextElementSibling;
      if (!dropdown || !dropdown.matches(".dropdown-content")) return;

      const dropdownParent = dropdown.closest(".dropdown");
      if (!dropdownParent) return;

      const dropdownName = dropdownParent.getAttribute("data-name");
      const applyFilterLink = dropdown.querySelector(".apply-filter");

      const isOpen = dropdown.classList.contains("show");
      if (isOpen) {
        // close the dropdown
        dropdown.classList.remove("show");
        targetButton.setAttribute("aria-expanded", "false");
      } else {
        // reset the dropdown to its initial state
        const initialItems = window.__DROPDOWN_DATA__?.[`chosen_${dropdownName}`] || [];
        setInitialCheckedCheckboxes(dropdown, initialItems);
        changeApplyFilterLink(applyFilterLink, initialItems);
        // show the dropdown
        dropdown.classList.add("show");
        targetButton.setAttribute("aria-expanded", "true");
      }
    });

    // close the dropdown when the close button is clicked
    const closeButtons = eventListFilter.querySelectorAll(".dropdown-content .close");
    closeButtons.forEach((closeButton) => {
      closeButton.addEventListener("click", (event) => {
        event.stopPropagation();
        const dropdown = closeButton.closest(".dropdown-content");
        if (dropdown) {
          dropdown.classList.remove("show");
          const button = dropdown.previousElementSibling;
          if (button && button.matches(".dropdown-button")) {
            button.setAttribute("aria-expanded", "false");
          }
        }
      });
    });

    // listen for checkbox changes
    const dropdownContents = eventListFilter.querySelectorAll(".dropdown-content");
    dropdownContents.forEach((dropdownContent) => {
      const applyFilterLink = dropdownContent.querySelector(".apply-filter");
      dropdownContent.addEventListener("change", (event) => {
        const targetCheckbox = event.target.closest("input[type='checkbox']");
        if (!targetCheckbox) return;

        const checkboxes = dropdownContent.querySelectorAll("input[type='checkbox']");
        const checked = Array.from(checkboxes).filter((checkbox) => checkbox.checked);
        const checkedNames = checked.map((checkbox) => checkbox.getAttribute("name"));

        changeApplyFilterLink(applyFilterLink, checkedNames);
      });
    });
  });

  function setInitialCheckedCheckboxes(contentEl, items) {
    const checkboxes = contentEl.querySelectorAll("input[type='checkbox']");
    checkboxes.forEach((checkbox) => {
      const checkboxName = checkbox.getAttribute("name");
      if (items.includes(checkboxName)) {
        checkbox.checked = true;
      } else {
        checkbox.checked = false;
      }
    });
  }

  function changeApplyFilterLink(linkEl, items) {
    const newFilterUrl = new URL(window.location.href);
    const dropdownName = linkEl.closest(".dropdown").getAttribute("data-name");
    newFilterUrl.searchParams.delete(dropdownName);
    if (items.length > 0) {
      newFilterUrl.searchParams.set(dropdownName, items.join(","));
    }
    linkEl.setAttribute("href", newFilterUrl.toString());
  }

  // close the dropdowns when clicking outside of it
  document.addEventListener("click", (event) => {
    const targetButton = event.target.closest(".dropdown-button");
    if (targetButton) return;

    const targetDropdown = event.target.closest(".dropdown-content.show");

    eventListFilters.forEach((eventListFilter) => {
      const dropdowns = eventListFilter.querySelectorAll(".dropdown-content.show");
      dropdowns.forEach((dropdown) => {
        if (dropdown === targetDropdown) return;

        dropdown.classList.remove("show");
        const button = dropdown.previousElementSibling;
        if (button && button.matches(".dropdown-button")) {
          button.setAttribute("aria-expanded", "false");
        }
      });
    });
  });
})();
