document.addEventListener("DOMContentLoaded", function () {

    const price = document.getElementById("id_price");
    const discountPercentage = document.getElementById("id_discount_percentage");
    const discountAmount = document.getElementById("id_discount_amount");
    const sellingPrice = document.getElementById("id_selling_price");

    function updateSellingPrice(price, discountAmount) {
        if (sellingPrice) {
            sellingPrice.value = (price - discountAmount).toFixed(2);
        }
    }

    if (!price || !discountPercentage || !discountAmount) {
        return;
    }

    function calculateFromPercentage() {
        const p = parseFloat(price.value) || 0;
        const percent = parseFloat(discountPercentage.value) || 0;

        const amount = (p * percent) / 100;
        discountAmount.value = amount.toFixed(2);
    updateSellingPrice(p, amount);
    
    }

    function calculateFromAmount() {
        const p = parseFloat(price.value) || 0;
        const amount = parseFloat(discountAmount.value) || 0;

        let percent = 0;

        if (p > 0) {
            percent = (amount * 100) / p;
        }

        discountPercentage.value = percent.toFixed(2);

        updateSellingPrice(p, amount);
    }

    discountPercentage.addEventListener("input", calculateFromPercentage);
    discountAmount.addEventListener("input", calculateFromAmount);
    price.addEventListener("input", calculateFromPercentage);


    calculateFromPercentage();
    calculateFromAmount();

});