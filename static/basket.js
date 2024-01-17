// Define a product
function Product(name, price, quantity) {
    this.name = name;
    this.price = price;
    this.quantity = quantity;
}

// Define a basket
function Basket() {
    this.products = [];
    this.total = 0;
}

// Add a product to the basket
Basket.prototype.addProduct = function (product) {
    this.products.push(product);
    this.total += product.price * product.quantity;
};

// Create a new basket
var basket = new Basket();

// Add some products to the basket
basket.addProduct(new Product("Product 1", 10, 2));
basket.addProduct(new Product("Product 2", 20, 1));

// Log the total price of the basket
console.log(basket.total);
