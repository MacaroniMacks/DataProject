document.addEventListener('DOMContentLoaded', () => {
  const tabContents = document.querySelectorAll('.tab-content');
  
  tabContents.forEach(tabContent => {
      tabContent.addEventListener('mousemove', (event) => {
          const tooltip = tabContent.querySelector('.tooltip-text');
          if (tooltip) {
              tooltip.style.left = `${event.pageX - tabContent.offsetLeft}px`;
              tooltip.style.top = `${event.pageY - tabContent.offsetTop - 120}px`;
              tooltip.style.visibility = 'visible';
              tooltip.style.opacity = '1';
          }
      });

      tabContent.addEventListener('mouseleave', () => {
          const tooltip = tabContent.querySelector('.tooltip-text');
          if (tooltip) {
              tooltip.style.visibility = 'hidden';
              tooltip.style.opacity = '0';
          }
      });
  });
});
