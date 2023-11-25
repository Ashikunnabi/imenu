// Main script: app.js
import { categoryModule } from "../components/categoryModule.js";
import { menuModule } from "../components/menuModule.js";

// categoryModule.getCategories(1);
menuModule.getMenus();
menuModule.getSearchItems();


// store table number in local storage with 5 hours expiry time
function storeTableNumber() {
    // Get the URL parameters
    const urlParams = new URLSearchParams(window.location.search);

    // Check if the 'table' parameter exists
    if (urlParams.has('table')) {
        // Get the value of the 'table' parameter
        const tableValue = urlParams.get('table');
        setLocalWithExpiry("table_uuid", tableValue, 5*60)
    } else {
        console.log('Table parameter not found.');
    }
}
storeTableNumber()
