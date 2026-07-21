from store.models import Variation, VariationCategory

color = VariationCategory.objects.get(name="Color")
size = VariationCategory.objects.get(name="Size")

count = 0

for variation in Variation.objects.all():
    if variation.variation_category == "color":
        variation.variation_category_new = color
    elif variation.variation_category == "size":
        variation.variation_category_new = size

    variation.save()
    count += 1

print(f"{count} variations updated successfully!")