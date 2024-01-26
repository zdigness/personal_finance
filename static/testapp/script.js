function calculate() {
    var category_list = document.querySelectorAll(".category")

    for (var i = 0; i < category_list.length; i++) {
        var x = category_list[i].querySelector("#current").innerHTML.slice(1)
        var y = category_list[i].querySelector("#spent").innerHTML.slice(1)
        var z = parseFloat(x - y).toFixed(2)
        category_list[i].querySelector("#result").innerHTML = "$" + z;
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const track = document.querySelector(".carousel-track");
    const slides = document.querySelectorAll(".carousel-slide");
    const prevButton = document.querySelector(".carousel-prev");
    const nextButton = document.querySelector(".carousel-next");

    let currentIndex = 0;

    // Set initial position of the track
    function setInitialPosition() {
        track.style.transform = `translateX(-${currentIndex * 100}%)`;
    }

    // Update the track position based on the current index
    function updateTrack() {
        track.style.transform = `translateX(-${currentIndex * 100}%)`;
    }

    // Move to the next slide
    function nextSlide() {
        if (currentIndex < slides.length - 1) {
            currentIndex++;
        } else {
            currentIndex = 0;
        }
        updateTrack();
    }

    // Move to the previous slide
    function prevSlide() {
        if (currentIndex > 0) {
            currentIndex--;
        } else {
            currentIndex = slides.length - 1;
        }
        updateTrack();
    }

    // Event listeners for next and previous buttons
    nextButton.addEventListener("click", nextSlide);
    prevButton.addEventListener("click", prevSlide);

    // Set initial position
    setInitialPosition();
});