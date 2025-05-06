from product.models.prod_model import Product

def seed_products(category_id):
    """Seed some products into test DB linked to given category."""
    product1 = Product(
        name="Bread",
        description="Fresh Bread",
        price=50.0,
        category_id=category_id
    )
    product2 = Product(
        name="Knife Set",
        description="Stainless Steel Kitchen Knives",
        price=500.0,
        category_id=category_id
    )
    
    product1.save()
    product2.save()
    
    return [product1, product2]
