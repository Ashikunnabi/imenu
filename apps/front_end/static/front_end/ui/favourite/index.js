// Main script: app.js
import { productListModule } from "../components/productListModule.js";

productListModule.getSelectedItems();
//  in 5000ms refetch the cart order
productListModule.refetchCartOrder(5000)
