from django.core.management.base import BaseCommand
from scanner.models import User

class Command(BaseCommand):
    help = 'Generate barcodes for users who do not have one'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without making changes',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        # Find users without barcodes
        users_without_barcodes = User.objects.filter(barcode__isnull=True) | User.objects.filter(barcode='')
        
        if not users_without_barcodes.exists():
            self.stdout.write(
                self.style.SUCCESS('All users already have barcodes!')
            )
            return
        
        self.stdout.write(
            f'Found {users_without_barcodes.count()} users without barcodes'
        )
        
        if dry_run:
            self.stdout.write('DRY RUN - No changes will be made')
            for user in users_without_barcodes:
                self.stdout.write(
                    f'Would generate barcode for: {user.get_full_name()} ({user.username})'
                )
        else:
            generated_count = 0
            for user in users_without_barcodes:
                try:
                    barcode = user.generate_barcode()
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Generated barcode {barcode} for {user.get_full_name()} ({user.username})'
                        )
                    )
                    generated_count += 1
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f'Failed to generate barcode for {user.get_full_name()}: {str(e)}'
                        )
                    )
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully generated {generated_count} barcodes')
            ) 