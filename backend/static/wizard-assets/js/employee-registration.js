// this file will be used to add styling and dynamic interactions to the services 
// selection section in the employee registration form
document.addEventListener('DOMContentLoaded', function() {
    const categoryDropdown = document.querySelector('.category-dropdown');
    const serviceContainers = document.querySelectorAll('.category-services');

    categoryDropdown.addEventListener('change', function() {
        const selectedCategory = this.value;

        // this will hide all service containers
        serviceContainers.forEach(container => {
            container.style.display = 'none';
        });

        // this will show the selected category's service container
        if (selectedCategory) {
            const selectedContainer = document.querySelector(
                `.category-services[data-category="${selectedCategory}"]`
            );

            if (selectedContainer) {
                selectedContainer.style.display = 'block';
            }
        }

    })
});