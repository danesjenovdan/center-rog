(async () => {
  const data = window.__USER_GALLERY_DATA__;
  const containerElement = document.querySelector(".user-gallery");
  const templateElement = containerElement.querySelector("template");

  data.forEach((image) => {
    const clone = templateElement.content.cloneNode(true);
    const img = clone.querySelector("img");
    const button = clone.querySelector("button");

    img.src = image.url;
    img.alt = image.name;
    img.dataset.id = image.image_id;

    button.addEventListener("click", () => {
      alert("TODO" + image.image_id);
    });

    containerElement.appendChild(clone);
  });
})();
