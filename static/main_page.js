window.addEventListener('load', function() {
    var recommended_products = document.getElementsByClassName('recommended-product');
    for (var i = 0; i < recommended_products.length; i++) {
        var product_name = recommended_products[i].getElementsByClassName('name')[0];
        var product_description = recommended_products[i].getElementsByClassName('description')[0];

        //get product_name with httpGet from http://127.0.0.1:5500/get_product/{i}/name
        product_name.textContent = httpGet('http://127.0.0.1:5500/get_product/' + i + '/name');
        product_description.textContent = httpGet('http://127.0.0.1:5500/get_product/' + i + '/description');
    }
});
