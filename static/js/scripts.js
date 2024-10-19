document.addEventListener("DOMContentLoaded", function() {
    window.goToRestaurants = function(city) {
        const selectedCity = city;
        console.log("Selected city:", selectedCity);

        // Add a smooth transition for hiding the city selection buttons
        const cityContainer = document.querySelector('.container');
        cityContainer.style.transition = 'opacity 0.6s ease-out';
        cityContainer.style.opacity = '0';  // Set opacity to 0 for fade-out

        // After the transition ends, hide the container and display the recommendations
        setTimeout(() => {
            cityContainer.style.display = 'none';  // Hide city buttons after transition

            // Make a request to the Flask server to get restaurant recommendations
            fetch(`/recommend?city=${selectedCity}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();  // Parse the response as JSON
            })
            .then(data => {
                console.log("Recommendations received:", data);

                // Clear the existing content inside #recommendations
                const recommendationsContainer = document.getElementById("recommendations");
                recommendationsContainer.innerHTML = "";

                // Dynamically create recommendation cards with a fade-in effect
                const restaurantGrid = document.createElement("div");
                restaurantGrid.className = "restaurant-grid";
                restaurantGrid.style.opacity = "0";  // Start with opacity 0 for fade-in

                data.forEach(restaurant => {
                    const restaurantCard = document.createElement("div");
                    restaurantCard.className = "restaurant-card";

                    // Make the entire restaurant card clickable
                    restaurantCard.onclick = function() {
                        window.open(restaurant.url, '_blank');
                    };

                    restaurantCard.innerHTML = `
                        <img src="/static/images/${restaurant.image}" alt="${restaurant.name}" class="restaurant-img">
                        <h2>${restaurant.name}</h2>
                        <p>${restaurant.description}</p>
                        <div class="price-rating">
                            <span>${restaurant.price}</span>
                            <span>${restaurant.rating}</span>
                        </div>
                    `;
                    
                    restaurantGrid.appendChild(restaurantCard);
                });

                // Append the grid to the recommendations container
                recommendationsContainer.appendChild(restaurantGrid);

                // Fade-in effect for the recommendations
                setTimeout(() => {
                    restaurantGrid.style.transition = 'opacity 0.6s ease-in';
                    restaurantGrid.style.opacity = '1';  // Set opacity to 1 to show the grid
                }, 100);  // Slight delay to ensure it happens after it's added to the DOM
            })
            .catch(error => {
                console.error("Error fetching recommendations:", error);
                document.getElementById("recommendations").innerHTML = "Sorry, something went wrong. Please try again later.";
            });
        }, 600);  // Delay hiding the city buttons until fade-out transition completes
    }
});
