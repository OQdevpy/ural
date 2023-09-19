from catalog.models import OrderItem  # Import the necessary model
import json

# Open the file for reading
with open('catalog_orderitem.json', 'r') as f:
    # Read the contents of the file and load it as JSON
    data = json.load(f)
    for i in data:
        order = OrderItem.objects.create(
            order_id=i['order_id'],
            offer_id=i['offer_id'],
            price=i['price'],
            quantity=i['quantity']
        )
        order.save()

# Now you can access the loaded JSON data
