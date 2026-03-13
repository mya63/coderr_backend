
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders_app', '0002_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('in_progress', 'In progress'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='in_progress', max_length=20),
        ),
    ]
