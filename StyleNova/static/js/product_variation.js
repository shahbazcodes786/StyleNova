document.addEventListener("DOMContentLoaded", function () {

    function updateVariationDropdowns() {

        // Right side (Chosen variation categories)
        const chosenBox = document.getElementById("id_variation_categories_to");

        if (!chosenBox) return;

        // Selected categories
        let categories = [];

        Array.from(chosenBox.options).forEach(function (option) {
            categories.push({
                value: option.value,
                text: option.text
            });
        });

        // Update every variation category dropdown
        document.querySelectorAll("select[id$='variation_category']").forEach(function (dropdown) {

            const currentValue = dropdown.value;

            dropdown.innerHTML = "";

            // Empty option
            dropdown.appendChild(new Option("---------", ""));

            categories.forEach(function (cat) {
                dropdown.appendChild(new Option(cat.text, cat.value));
            });

            dropdown.value = currentValue;
        });

    }

    // First load
    updateVariationDropdowns();

    // Every 300ms check changes
    setInterval(updateVariationDropdowns, 300);

});