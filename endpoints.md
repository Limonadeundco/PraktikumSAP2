@app.route("/get_product/<product_id>/<column>", methods=["GET"])
@app.route("/get_product/<product_id>", methods=["GET"])

@app.route("/get_all_products", defaults={'limit': None}, methods=["GET"])
@app.route("/get_all_products/<limit>", methods=["GET"])

@app.route("/update_product/<product_id>/<parameters>", methods=["PUT"])
@app.route("/add_product/<path:parameters>", methods=["POST"])
@app.route("/remove_product/<product_id>", methods=["DELETE"])

@app.route("/get_recommended_products/<limit>", methods=["GET"])
@app.route("/get_recommended_products", defaults={'limit': 5}, methods=["GET"])
@app.route("/get_all_recommended_products", methods=["GET"])

@app.route("/get_image/<product_id>", methods=["GET"])
@app.route("/get_image/<product_id>/<image_id>", methods=["GET"])
@app.route("/get_image/utility/<name>", methods=["GET"])

@app.route("/get_basket_for_user/<user_id>", methods=["GET"])
@app.route("/remove_product_from_basket/<user_id>/<product_id>", methods=["DELETE"])
@app.route("/clear_basket/<user_id>", methods=["DELETE"])

@app.route("/get_cookie", methods=["GET"])

@app.route("/", methods=["GET"])
@app.route("/basket", methods=["GET"])
@app.route("/products", methods=["GET"])
@app.route("/contact", methods=["GET"])
