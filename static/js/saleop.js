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

    $('.add-to-cart').click(function () {
        var product_sku = $(this).data('p-id');
        var product_Quantity = $(this).data('p-quantity');
        const csrftoken = Cookies.get('csrftoken');

        $.ajax({
            type: 'POST',
            url: $(this).data('url'),
            data: {
                product_sku: product_sku,
                quantity: product_Quantity,
                csrfmiddlewaretoken: csrftoken
            },
            success: function (data) {
                location.reload();
            }
        });
    });
    $('.alert-message').delay(3000).fadeOut();
});

function category_filter() {
    var category = '';
    $.each($('.category_checkbox:checked'), function () {
        category += $(this).data('slug') + '+';
    });
    if (category == '') {
        return '';
    }
    return '&category=' + category;
}
function brand_filter() {
    var brand = '';
    $.each($('.brand-checkbox:checked'), function () {
        brand += $(this).data('slug') + '+';
    });
    if (brand == '') {
        return '';
    }
    return '&brand=' + brand;
}
function price_filter() {
    var min_price = $('.price#min').val();
    var max_price = $('.price#max').val();
    if (min_price == '' && max_price == '') {
        return '';
    }
    return '&price=' + min_price + '-' + max_price;
}
function sort_filter() {
    var sort = $('.sort-Category').val();
    if (sort == '') {
        return '';
    }
    return '&sort=' + sort;
}


// redirect to filter url
$('.category_checkbox').change(function () {
    document.location.href = '?' + category_filter() + brand_filter() + price_filter() + sort_filter();
});
$('.brand-checkbox').change(function () {
    document.location.href = '?' + category_filter() + brand_filter() + price_filter() + sort_filter();
});
$('.price').change(function () {
    document.location.href = '?' + category_filter() + brand_filter() + price_filter() + sort_filter();
});

$('.sort-Category').change(function () {
    document.location.href = '?' + category_filter() + brand_filter() + price_filter() + sort_filter();
});

$('.address_list_chosen input').change(function () {
    $('.addr').find('.u_ship_info.hidden').removeClass('hidden');
    $('.addr').find('.text-base.r_noti').addClass('hidden');
    $('#r_name').val('Người nhận: '+$(this).data('name'));
    $('#r_phone').val('Số điện thoại: '+$(this).data('phone'));
    $('#r_address').val('Địa chỉ: '+$(this).data('address'));
});
    