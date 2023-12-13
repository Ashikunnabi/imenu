var currentURL = window.location.href;


class Cart {
	list_url = "/api/v1/carts/"
	add_url = "/api/v1/carts/"

	get(cart_uuid='') {
		let cart = getLocalWithExpiry("cart") || null
		let cart_already_exists = cart || false

		if (!cart_already_exists) {
			console.log("Cart not found. Maybe expired.")
			return
		} else {
			this.cart_uuid = cart.uuid
			this.list_url = `${this.list_url}${cart.uuid}/`
		}

		new AjaxRequest(this.list_url, "GET").makeRequest()
			.done(function (response) {
				setLocalWithExpiry("cart", response.data, 60)
			})
			.fail(function (error) {
				console.error('Error in POST Request:', error);
			});
		return getLocalWithExpiry("cart") || {}
	}
	add(product_uuid) {
		let data = {
			"lines": [
				{
					"product_uuid": product_uuid,
					"quantity": 1
				}
			]

		}

		new AjaxRequest(this.add_url, "POST").makeRequest(data)
			.done(function (response) {
				setLocalWithExpiry("cart", response.data, 60)
			})
			.fail(function (error) {
				console.error('Error in POST Request:', error);
			});

	}
	edit(cart_uuid) {

	}
	delete(cart_uuid) {

	}
}

class CartLine {
	list_url = "/api/v1/carts/cart_uuid/lines/"
	add_url = "/api/v1/carts/cart_uuid/lines/"
	delete_url = "/api/v1/carts/cart_uuid/lines/cart_line_uuid/"

	constructor(cart_uuid) {
		this.cart_uuid = cart_uuid
	}
	get(cart_line_uuid) {

	}
	add(product_uuid) {
		let cart = getLocalWithExpiry("cart") || null
		let cart_already_exists = cart || false

		if (!cart_already_exists) {
			new Cart().add(product_uuid)
			return
		} else {
			this.cart_uuid = cart.uuid
			this.list_url = this.list_url.replace("cart_uuid", cart.uuid)
			this.add_url = this.add_url.replace("cart_uuid", cart.uuid)
		}

		let data = {
			"product_uuid": product_uuid,
			"quantity": 1,
		}

		new AjaxRequest(this.add_url, "POST").makeRequest(data)
			.done(function (response) {
				setLocalWithExpiry("cart", response.data, 60)
			})
			.fail(function (error) {
				console.error('Error in POST Request:', error);
			});
	}
	edit(cart_line_uuid) {

	}
	delete(product_uuid) {
		let cart = getLocalWithExpiry("cart") || null
		let cart_already_exists = cart || false

		if (!cart_already_exists) {
			console.log("Cart not found. Maybe expired.")
			return
		} else {
			this.cart_uuid = cart.uuid
			this.list_url = this.list_url.replace("cart_uuid", cart.uuid)
			this.add_url = this.add_url.replace("cart_uuid", cart.uuid)
			this.delete_url = this.delete_url.replace("cart_uuid", cart.uuid)
			let cart_line_uuid = this.findLineUuidByProductUuid(cart, product_uuid)
			if (!cart_line_uuid) {
				console.log("CartLine not found. Maybe expired.")
				return
			}
			this.delete_url = this.delete_url.replace("cart_line_uuid", cart_line_uuid)
			console.log(this.delete_url)
		}


		let data = {}
		new AjaxRequest(this.delete_url, "DELETE").makeRequest(data)
			.done(function (response) {
				setLocalWithExpiry("cart", response.data, 60)
			})
			.fail(function (error) {
				console.error('Error in POST Request:', error);
			});
	}

	findLineUuidByProductUuid(data, product_uuid) {
		var lines = data.lines;

		for (var i = 0; i < lines.length; i++) {
			var line = lines[i];

			// Check if product uuid matches
			if (line.product.uuid === product_uuid) {
				return line.uuid;
			}
		}

		// Return null if no match found
		return null;
	}

}
