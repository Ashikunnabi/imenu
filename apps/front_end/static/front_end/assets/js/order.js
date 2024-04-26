var currentURL = window.location.href;


class Order {
	list_url = "/api/v1/orders/"
	add_url = "/api/v1/orders/"

	get(order_uuid = '') {
		let self = this
		let orders = getLocalWithExpiry("orders") || []
		let order_already_exists = orders || false

		if (!order_already_exists) {
			console.log("Order not found. Maybe expired.")
			return
		}

		// loop through the orders and get the order with the order_uuid
		$.each(orders, function (index, order) {
			let list_url = `${self.list_url}${order.uuid}/`

			new AjaxRequest(list_url, "GET").makeRequest()
				.done(function (response) {
					$.each(orders, function (index, existing_order) {
						if (existing_order.uuid == response.data.uuid) {
							orders[index] = response.data
							setLocalWithExpiry("orders", orders, 60)
						}
					})
				})
				.fail(function (error) {
					console.error('Error in POST Request:', error);
				});
		})
		return getLocalWithExpiry("orders") || []
	}

	add(cart_uuid) {
		let data = {
			"cart_uuid": cart_uuid
		}

		new AjaxRequest(this.add_url, "POST").makeRequest(data)
			.done(function (response) {
				let existing_orders = getLocalWithExpiry("orders") || []
				existing_orders.push(response.data)
				setLocalWithExpiry("orders", existing_orders, 60)
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

