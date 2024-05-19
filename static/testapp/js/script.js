$(document).on("submit", "#my-form", function (e) {
  e.preventDefault();
  $.ajax({
    type: "POST",
    url: "/ajax/post/url",
    data: $(this).serialize(), // serializes the form's elements.
    success: function (response) {
      botMessage = response.message;
      userMessages = response.userMessage;
      $("#chatbot-messages").append(
        "<p class='user-message'>" + userMessages + "</p>",
      );
      $("#chatbot-messages").append(
        "<p class='chatbot-message'>" + botMessage + "</p>",
      );
      $("#my-form")[0].reset();
    },
    error: function (response) {},
  });
});

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

const nav = document.querySelector(".navbar");

window.addEventListener("scroll", () => {
  if (window.scrollY > 50) {
    nav.classList.add("navbar-scrolled");
  } else {
    nav.classList.remove("navbar-scrolled");
  }
});

const authAlertsDiv = document.querySelector(".auth-alerts");
const alertDiv = authAlertsDiv.querySelector(".alert");

alertDiv.addEventListener("closed.bs.alert", () => {
  authAlertsDiv.remove(); // Remove the entire auth-alerts div
});
