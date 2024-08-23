function toggleImage(tabContent) {
    const img = tabContent.querySelector('img');
    const currentSrc = img.src;
    const altSrc = img.getAttribute('data-alt-image');

    // Swap the current src with the alternative src
    img.src = altSrc;
    img.setAttribute('data-alt-image', currentSrc);

    // Optionally update the tooltip text
    const tooltip = tabContent.querySelector('.tooltip-text');
    if (tooltip.innerText.includes('GDP per Capita')) {
        tooltip.innerText = 'Click to change to Overall GDP';
    } else {
        tooltip.innerText = 'Click to change to GDP per Capita';
    }

    const activeTabButton = document.querySelector('.tab-button.active');
    if (activeTabButton) {
        const currentText = activeTabButton.innerText;
        const altText = activeTabButton.getAttribute('data-alt-text');
        activeTabButton.innerText = altText;
        activeTabButton.setAttribute('data-alt-text', currentText);
    }
}
