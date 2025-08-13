const button = document.getElementById('boardSettings');
const contextMenu = document.getElementById('contextMenu');
let menuVisible = false;

document.addEventListener('DOMContentLoaded', function () {
    // Prevent the browser's default context menu on the button
    button.addEventListener('contextmenu', function (event) {
        event.preventDefault();
    });

    // Function to show the context menu
    function showContextMenu(x, y) {
        contextMenu.style.left = x + 'px';
        contextMenu.style.top = y + 'px';
        contextMenu.classList.add('show');
        menuVisible = !menuVisible;
    }

    // Event listener for the button click
    button.addEventListener('click', function (event) {
        event.preventDefault(); // Prevent default button behavior

        // Position the context menu relative to the button
        const buttonRect = button.getBoundingClientRect();
        const x = buttonRect.left;
        const y = buttonRect.bottom; // Place menu below the button

        showContextMenu(x, y);
    });

    // Function to hide the context menu
    function hideContextMenu() {
        contextMenu.classList.remove('show');
        menuVisible = !menuVisible;
    }

    // Event listener to hide the context menu when clicking anywhere else
    document.addEventListener('click', function (event) {
        if (menuVisible && !contextMenu.contains(event.target) && event.target !== button) {
            hideContextMenu();
        }
    });
});

