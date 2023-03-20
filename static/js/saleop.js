var sortProdiuctByCategory = function (category) {
    var products = $('.product');
    var productsByCategory = $('.product').data('p-category', category);

    products.hide();
    productsByCategory.show();
};

$(document).ready(function () {
    $('#sort-Category').change(function () {
        var category = $(this).val();
        sortProdiuctByCategory(category);
    });
});

$(document).ready(function () {
    $('.add-to-cart').click(function () {
        var product_sku = $(this).data('p-id');
        var product_Quantity = $(this).data('p-quantity');
        var csrf_token = $(this).data('csrf-token');

        $.ajax({
            type: 'POST',
            url: $(this).data('url'),
            data: {
                product_sku: product_sku,
                quantity: product_Quantity,
                csrfmiddlewaretoken: csrf_token
            },
            success: function (data) {
                console.log(data);
                if (data.success) {
                    var itemincart = $('.item-in-cart').data('itemincart');
                    $('.item-in-cart').html(itemincart + 1);
                }
            }
        });
    });
});