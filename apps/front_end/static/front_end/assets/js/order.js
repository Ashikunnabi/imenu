var currentURL = window.location.href;


class Order {
	list_url = "/api/v1/orders/"
	add_url = "/api/v1/orders/"

	get(order_uuid = '') {
		let order = getLocalWithExpiry("order") || null
		let order_already_exists = order || false

		if (!order_already_exists) {
			console.log("Order not found. Maybe expired.")
			return
		} else {
			this.order_uuid = order.uuid
			this.list_url = `${this.list_url}${order.uuid}/`
		}

		new AjaxRequest(this.list_url, "GET").makeRequest()
			.done(function (response) {
				setLocalWithExpiry("order", response.data, 60)
			})
			.fail(function (error) {
				console.error('Error in POST Request:', error);
			});
		return getLocalWithExpiry("order") || {}
	}

	add(cart_uuid) {
		let data = {
			"cart_uuid": cart_uuid
		}

		new AjaxRequest(this.add_url, "POST").makeRequest(data)
			.done(function (response) {
				setLocalWithExpiry("order", response.data, 60)
				notify("success", "Order created successfully.")
			})
			.fail(function (error) {
				console.error('Error in POST Request:', error);
			});

	}
	edit(order_uuid) {

	}
	delete(order_uuid) {

	}
}

