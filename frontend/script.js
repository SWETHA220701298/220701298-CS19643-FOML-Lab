const imageUpload = document.getElementById("imageUpload");
const imagePreview = document.getElementById("imagePreview");
const resultContainer = document.getElementById("resultContainer");

imageUpload.addEventListener("change", () => {
  const file = imageUpload.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = () => {
      imagePreview.src = reader.result;
      imagePreview.style.display = "block";
    };
    reader.readAsDataURL(file);
  }
});

function submitImage() {
  const file = imageUpload.files[0];
  if (!file) {
    alert("Please select an image first.");
    return;
  }

  const formData = new FormData();
  formData.append("image", file);

  fetch("http://localhost:5000/analyze-face", {
    method: "POST",
    body: formData
  })
    .then(response => response.json())
    .then(data => {
      resultContainer.classList.remove("hidden");
      document.getElementById("toneResult").textContent = data.tone || "Not available";
      document.getElementById("textureResult").textContent = data.texture || "Not available";
      document.getElementById("tipResult").textContent = data.tip || "No tip available";
    
      const productList = document.getElementById("productList");
      productList.innerHTML = "";
      
      if (Array.isArray(data.products) && data.products.length > 0) {
        data.products.forEach(product => {
          const li = document.createElement("li");
          li.textContent = product; // since each item is a string from Gemini
          productList.appendChild(li);
        });
      } else {
        const li = document.createElement("li");
        li.textContent = "No products recommended.";
        productList.appendChild(li);
      }
    })
    
    
    .catch(error => {
      console.error("Error:", error);
      alert("Something went wrong. Please try again.");
    });
}
