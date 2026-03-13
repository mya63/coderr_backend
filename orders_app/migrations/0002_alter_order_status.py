
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('in progress', 'In progress'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='in progress', max_length=20),
        ),
    ]
