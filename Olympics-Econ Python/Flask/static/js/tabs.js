document.addEventListener("DOMContentLoaded", function() {
  const tabButtons = document.querySelectorAll(".tab-button");
  const tabContents = document.querySelectorAll(".tab-content");
  let activeTabButton = null; // To track the last clicked tab button

  // Function to show a tab content
  function showTabContent(tabButton) {
      tabContents.forEach(content => content.classList.remove("active"));
      tabButtons.forEach(button => button.classList.remove("active"));

      const targetContent = document.querySelector(tabButton.dataset.target);
      targetContent.classList.add("active");
      tabButton.classList.add("active");
  }

  // Click event listener
  tabButtons.forEach(button => {
      button.addEventListener("click", function() {
          activeTabButton = button; // Update the active tab button
          showTabContent(button);
      });
  });

  // Hover event listeners
  tabButtons.forEach(button => {
      button.addEventListener("mouseenter", function() {
          showTabContent(button);
      });

      button.addEventListener("mouseleave", function() {
          if (activeTabButton) {
              showTabContent(activeTabButton); // Revert to the last clicked tab
          }
      });
  });

  // Activate the first tab by default
  if (tabButtons.length > 0) {
      tabButtons[0].click();
  }
});
