const BASE_URL = "http://localhost:8000/products/";
const CATEGORY_URL = "http://localhost:8000/products/categories/";

const productsContainer = document.getElementById("productsContainer");
const categoryFilter = document.getElementById("categoryFilter");
const searchInput = document.getElementById("searchInput");
const searchButton = document.getElementById("searchButton");

const productTemplate = document.getElementById("productTemplate");
const errorTemplate = document.getElementById("errorTemplate");

if (
  !productsContainer ||
  !categoryFilter ||
  !searchInput ||
  !searchButton ||
  !productTemplate ||
  !errorTemplate
) {
  console.error("One or more required DOM elements are missing.");
} else {
  async function fetchProducts(category = "") {
    try {
      let url = BASE_URL;
      if (category) {
        url += `?category=${encodeURIComponent(category)}`;
      }

      const response = await fetch(url);
      const products = await response.json();

      if (products.error) {
        renderError(products.error);
      } else {
        renderProducts(products);
      }
    } catch (error) {
      console.error("Error fetching products:", error);
      renderError("Unable to fetch products. Please try again later.");
    }
  }

  function renderProducts(products) {
    if (!productsContainer || !(productTemplate instanceof HTMLTemplateElement))
      return;

    productsContainer.innerHTML = "";
    const fragment = document.createDocumentFragment();

    products.forEach((product) => {
      const clone = productTemplate.content.cloneNode(true);

      const nameEl = clone.querySelector('[data-field="name"]');
      const descEl = clone.querySelector('[data-field="description"]');
      const priceEl = clone.querySelector('[data-field="price"]');
      const manuDateEl = clone.querySelector('[data-field="manufacture_date"]');
      const expDateEl = clone.querySelector('[data-field="expiry_date"]');
      const weightEl = clone.querySelector('[data-field="weight"]');
      const categoryEl = clone.querySelector('[data-field="category"]');

      if (nameEl) nameEl.textContent = product.name || "N/A";
      if (descEl) descEl.textContent = product.description || "N/A";
      if (priceEl) priceEl.textContent = product.price_in_RS || "N/A";
      if (manuDateEl)
        manuDateEl.textContent = product.manufacture_date || "N/A";
      if (expDateEl) expDateEl.textContent = product.expiry_date || "N/A";
      if (weightEl) weightEl.textContent = product.weight_in_KG || "N/A";
      if (categoryEl) categoryEl.textContent = product.category || "N/A";

      fragment.appendChild(clone);
    });

    productsContainer.appendChild(fragment);
  }

  function renderError(message) {
    productsContainer.innerHTML = "";
    const errorElement = errorTemplate.content.cloneNode(true);
    const msgEl = errorElement.querySelector(".error-message");
    if (msgEl) msgEl.textContent = message;
    productsContainer.appendChild(errorElement);
  }

  function searchProducts() {
    const keyword = searchInput.value.trim().toLowerCase();

    if (!keyword) {
      fetchProducts(categoryFilter.value);
      return;
    }

    fetch(BASE_URL)
      .then((res) => res.json())
      .then((data) => {
        const filtered = data.filter((product) => {
          return (
            product.name.toLowerCase().includes(keyword) ||
            (product.description &&
              product.description.toLowerCase().includes(keyword))
          );
        });

        renderProducts(filtered);
      })
      .catch((err) => {
        console.error("Search error:", err);
        renderError("Error searching products.");
      });
  }

  async function loadCategories() {
    try {
      const res = await fetch(CATEGORY_URL);
      const categories = await res.json();

      categories.forEach((cat) => {
        const option = document.createElement("option");
        option.value = cat.category_name;
        option.textContent = cat.category_name;
        categoryFilter.appendChild(option);
      });
    } catch (err) {
      console.error("Category fetch error:", err);
    }
  }

  function initEvents() {
    categoryFilter.addEventListener("change", () =>
      fetchProducts(categoryFilter.value),
    );
    searchButton.addEventListener("click", searchProducts);
    searchInput.addEventListener("keypress", (event) => {
      if (event.key === "Enter") {
        searchProducts();
      }
    });
  }

  window.onload = () => {
    loadCategories();
    fetchProducts();
    initEvents();
  };
}
