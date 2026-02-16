import csv
from decimal import Decimal, InvalidOperation

from django.core.management.base import BaseCommand

from landing.models import Product, Condition, Location


class Command(BaseCommand):
    help = 'Imports data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the csv file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        valid_conditions = {c.value for c in Condition}
        valid_locations = {l.value for l in Location}

        required_cols = {
            'title', 'price', 'category', 'condition', 'location',
            'available', 'seller', 'image', 'description'
        }

        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                if not reader.fieldnames:
                    self.stdout.write(self.style.ERROR("Error: CSV has no header row."))
                    return

                missing = required_cols - set(h.strip() for h in reader.fieldnames)
                if missing:
                    self.stdout.write(self.style.ERROR(
                        f"Error: Missing required column(s): {sorted(missing)}. "
                        f"Found: {reader.fieldnames}"
                    ))
                    return

                for row in reader:
                    row = {k: (v.strip() if isinstance(v, str) else v) for k, v in row.items()}

                    title = row.get('title', '').strip()
                    if not title:
                        self.stdout.write(self.style.ERROR("Error: Missing title in a row; skipping."))
                        continue

                    # boolean field handling
                    available_bool = row['available'].strip().lower() == 'true'

                    # decimal field handling
                    try:
                        price_decimal = Decimal(row['price'].strip())
                    except (InvalidOperation, KeyError):
                        self.stdout.write(self.style.ERROR(
                            f"Invalid price for title='{row.get('title', '?')}'. value='{row.get('price', '')}'"
                        ))
                        continue

                    # condition / location handling
                    condition_val = row['condition'].strip().lower()
                    if condition_val not in valid_conditions:
                        self.stdout.write(self.style.ERROR(
                            f"Invalid condition for title='{row.get('title', '?')}'. "
                            f"value='{row.get('condition', '')}'. "
                            f"Expected one of: {sorted(valid_conditions)}"
                        ))
                        continue

                    location_val = row['location'].strip()
                    if location_val not in valid_locations:
                        self.stdout.write(self.style.ERROR(
                            f"Invalid location for title='{row.get('title', '?')}'. "
                            f"value='{row.get('location', '')}'. "
                            f"Expected one of: {sorted(valid_locations)}"
                        ))
                        continue

                    obj, created = Product.objects.get_or_create(
                        title=title,
                        defaults={
                            'price': price_decimal,
                            'category': row.get('category', ''),
                            'condition': condition_val,
                            'location': location_val,
                            'available': available_bool,
                            'seller': row.get('seller', ''),
                            'image': row.get('image', ''),
                            'description': row.get('description', '').strip() or None,
                        }
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Imported: {title}"))
                    else:
                        self.stdout.write(self.style.WARNING(f"Skipped: {title}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
