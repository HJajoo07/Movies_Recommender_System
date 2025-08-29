const backendUrl = "http://127.0.0.1:5000";
let allMovies = [];

// Load all movies
fetch(`${backendUrl}/movies`)
  .then(res => res.json())
  .then(data => {
    allMovies = data.movies.sort(); // keep sorted alphabetically
  })
  .catch(err => console.error("Error loading movies:", err));

const searchInput = document.getElementById("movieInput");
const dropdown = document.getElementById("movieList");

// Show sorted list on focus (click)
searchInput.addEventListener("focus", () => {
  renderDropdown(allMovies);
});

// Filter list while typing
searchInput.addEventListener("input", () => {
  const query = searchInput.value.toLowerCase();
  const filtered = allMovies.filter(movie =>
    movie.toLowerCase().includes(query)
  );
  renderDropdown(filtered);
});

// Render dropdown list
function renderDropdown(list) {
  dropdown.innerHTML = "";
  if (list.length === 0) {
    dropdown.style.display = "none";
    return;
  }
  list.forEach(movie => {
    let li = document.createElement("li");
    li.textContent = movie;
    li.addEventListener("click", () => selectMovie(movie));
    dropdown.appendChild(li);
  });
  dropdown.style.display = "block";
}

// Select a movie from dropdown
function selectMovie(movie) {
  searchInput.value = movie;
  dropdown.style.display = "none";
}

// Hide dropdown if click happens outside input or dropdown
document.addEventListener("click", function(event) {
  if (!searchInput.contains(event.target) && !dropdown.contains(event.target)) {
    dropdown.style.display = "none";
  }
});

// Recommend button handler
// Recommend button handler
document.getElementById("recommendBtn").addEventListener("click", () => {
  const movie = searchInput.value.trim();
  const resultsDiv = document.getElementById("results");

  // 🧹 Always clear old recommendations first
  resultsDiv.innerHTML = "";

  if (!movie) {
    // if input is empty, just stop
    return;
  }

  fetch(`${backendUrl}/recommend`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ movie })
  })
    .then(res => res.json())
    .then(data => {
      if (!data.recommendations || data.recommendations.length === 0) {
        resultsDiv.innerHTML = "<p>No recommendations found.</p>";
        return;
      }

      resultsDiv.innerHTML =
        "<h3>Recommended Movies:</h3><div class='movie-grid'>" +
        data.recommendations
          .map(m => `<div class="movie-card">${m}</div>`)
          .join("") +
        "</div>";
    })
    .catch(err => {
      console.error("Error fetching recommendations:", err);
      resultsDiv.innerHTML = "<p style='color:red'>Error fetching recommendations.</p>";
    });
});

