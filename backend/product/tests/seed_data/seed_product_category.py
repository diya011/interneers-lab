from product.models.prod_category_model import ProductCategory

def seed_product_categories():
    """Seed some product categories into test DB."""
    category1 = ProductCategory(title="Food", description="All food items")
    category2 = ProductCategory(title="Kitchen Essentials", description="Items needed in kitchen")
    
    category1.save()
    category2.save()
    
    return [category1, category2]  # Return for linking products if needed
