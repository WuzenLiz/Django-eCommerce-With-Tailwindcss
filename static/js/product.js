$('.variant-selector').click(function() {
    $(this).addClass('active').siblings().removeClass('active');
    $(this).addClass('bg-primary').siblings().removeClass('bg-primary');
    var input = $(this).find('input');
    var product_sku = input.data('sku');
    var product_max_Quantity = input.data('quantity');
    var product_price = input.data('price');
    var product_sale_price = input.data('sale-price');
    var img_variant = $('.image-catalogue img#img-' + product_sku).attr('src');
    $('img.image-main-lg').attr('src', img_variant);
    $('.p-sku').html(product_sku);
    $('.p-quantity').attr('max', product_max_Quantity);
    if (product_sale_price) {
        $('.p-sale-price').html(product_sale_price);
        $('.p-price').html(product_price);
    }
    else {
        $('.p-sale-price').html(product_price);
        $('.p-price').html('');
    }
    $('.add-to-cart').attr('data-p-id', product_sku);
});
$('.p_add-q').click(function() {
    var quantity = $('.input_p-quantity').val();
    quantity++;
    $('.input_p-quantity').val(quantity);
    $('.add-to-cart').attr('data-p-quantity', quantity);
});
$('.p_sub-q').click(function() {
    var quantity = $('.input_p-quantity').val();
    if (quantity > 1) {
        quantity--;
        $('.input_p-quantity').val(quantity);
        $('.add-to-cart').attr('data-p-quantity', quantity);
    }
}); 

$('.image-catalogue img').click(function() {
    var src = $(this).attr('src');
    $('img.image-main-lg').attr('src', src);
});