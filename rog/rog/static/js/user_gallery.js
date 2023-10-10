// Function to get the CSRF token from a cookie
function getCookie(name) {
  const cookieValue = document.cookie.match("(^|;)\\s*" + name + "\\s*=\\s*([^;]+)");
  return cookieValue ? cookieValue.pop() : "";
}

async function galleryAPI(url, method, formData) {
  // Fetch the CSRF token from a cookie
  const csrfToken = getCookie("csrftoken");

  // Create headers with the CSRF token
  const headers = {
    "X-CSRFToken": csrfToken,
    Accept: "application/json",
  };

  return fetch(url, {
    method: method,
    body: formData,
    headers: headers,
  }).then((response) => {
    // Check if the response status is OK (200)
    if (response.status === 200) {
      return response;
    } else {
      // Handle other response statuses (e.g., 404, 500)
      throw new Error("Request failed");
    }
  });
}

(async () => {
  const data = window.__USER_GALLERY_DATA__;
  const containerElement = document.querySelector(".user-gallery");
  const templateElement = containerElement.querySelector("template");

  function deleteImage(e) {
    // Define the API endpoint URL
    const apiUrl = "/users/delete-gallery/";

    const imgElement = e.target.parentNode.querySelector("img");
    const imgId = imgElement.dataset.id;

    const formData = new FormData();
    formData.append("id", imgId);

    // Make a request using the fetch API
    galleryAPI(apiUrl, "POST", formData)
      .then((data) => {
        e.target.parentNode.remove();
      })
      .catch((error) => {
        // Handle errors
        const errorfield = document.querySelector(".error");
        errorfield.innerHTML = "Prišlo je do napake.";
        console.error(error);
      });
  }

  // show initial user images
  data.forEach((image) => {
    const clone = templateElement.content.cloneNode(true);
    const img = clone.querySelector("img");
    const button = clone.querySelector("button");

    img.src = image.url;
    img.alt = image.name;
    img.dataset.id = image.image_id;

    button.addEventListener("click", deleteImage);
    containerElement.appendChild(clone);
  });

  // handle image uploads
  const imageInput = document.getElementById("id_custom_gallery");

  // Event listener for the file input change event
  imageInput.addEventListener("change", (event) => {
    const apiUrl = "/users/edit-gallery/";

    new_files = event.target.files;

    if ((containerElement.querySelectorAll(".user-image").length + new_files.length) > 10) {
      document.querySelector(".error").innerHTML = "Preveliko število slik. // Too many images.";
      return;
    }

    const formData = new FormData();
    for (const file of event.target.files) {
      if (file.type.startsWith("image/")) {
        formData.append("image", file);
      }
    }

    galleryAPI(apiUrl, "POST", formData)
      .then((response) => {
        return response.json()
      })
      .then((response) => {
        console.log("response", response);
        for (const image of response.images) {
          
          const clone = templateElement.content.cloneNode(true);
          const img = clone.querySelector("img");
          const button = clone.querySelector("button");

          img.src = image.src;
          img.dataset.id = image.id;

          button.addEventListener("click", deleteImage);
          containerElement.appendChild(clone);
        }
      })
      .catch((error) => {
        // Handle errors
        console.error("Error:", error);
      });
  });
})();


