# Generated by Django 4.1.10 on 2023-08-23 12:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(blank=True, default='', max_length=300)),
                ('number', models.CharField(blank=True, max_length=10)),
                ('stair', models.CharField(blank=True, max_length=10)),
                ('level', models.CharField(blank=True, max_length=10)),
                ('door', models.CharField(blank=True, max_length=10)),
                ('extra', models.CharField(blank=True, max_length=300)),
                ('postal_code', models.CharField(blank=True, max_length=6)),
                ('talk_to', models.CharField(blank=True, default='', max_length=400)),
                ('talk_to_extra', models.CharField(blank=True, default='', max_length=400)),
                ('opening_hours', models.CharField(blank=True, max_length=300)),
                ('lat', models.FloatField(default=48.216618, null=True)),
                ('lon', models.FloatField(default=16.385031, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AddressPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.FloatField(default=48.216618, null=True)),
                ('lon', models.FloatField(default=16.385031, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AddressReapeatedPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.FloatField(default=48.216618, null=True)),
                ('lon', models.FloatField(default=16.385031, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('zone', models.PositiveIntegerField(blank=True, null=True)),
                ('distance', models.FloatField(blank=True, null=True)),
                ('price', models.FloatField(blank=True, null=True)),
                ('extra', models.FloatField(null=True)),
                ('type', models.CharField(default='einzelfahrt', max_length=100)),
                ('fromrepeated', models.BooleanField(blank=True, default=False)),
                ('repeated_id', models.PositiveIntegerField(blank=True, null=True)),
                ('repeated_deleted', models.BooleanField(blank=True, default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('external_id', models.IntegerField(default='-1')),
                ('phone_1', models.CharField(blank=True, max_length=100)),
                ('phone_2', models.CharField(blank=True, max_length=100)),
                ('email', models.CharField(blank=True, max_length=300)),
                ('name', models.CharField(max_length=200)),
                ('payment', models.CharField(default='Bar', max_length=10)),
                ('has_delayed_payment', models.BooleanField(default=False)),
                ('has_delayed_payment_memo', models.TextField(blank=True, default='')),
                ('memo', models.TextField(blank=True)),
                ('is_blacklisted', models.BooleanField(default=False)),
                ('is_blacklisted_memo', models.TextField(blank=True, default='')),
            ],
            options={
                'ordering': ('added',),
            },
        ),
        migrations.CreateModel(
            name='Dispo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('sequence', models.PositiveIntegerField(default=0)),
                ('preliminary', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalStaff',
            fields=[
                ('isDispo', models.BooleanField(default=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical staff',
                'verbose_name_plural': 'historical staffs',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_is_pick_up', models.BooleanField(default=True)),
                ('customer_is_drop_off', models.BooleanField(default=False)),
                ('position', models.PositiveIntegerField(default=0)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('start_time_to', models.DateTimeField(blank=True, null=True)),
                ('end_time_from', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('anon_name', models.CharField(blank=True, default='', max_length=300)),
                ('weight_size_bonus', models.CharField(blank=True, default='', max_length=10)),
                ('is_cargo', models.BooleanField(default=False)),
                ('is_express', models.BooleanField(default=False)),
                ('is_bigbuilding', models.BooleanField(default=False)),
                ('get_there_bonus', models.FloatField(default=0.0)),
                ('waiting_bonus', models.IntegerField(default=0)),
                ('memo', models.TextField(blank=True)),
                ('distance', models.FloatField(default=0.0, null=True)),
                ('price', models.FloatField(default=0.0)),
                ('bonus', models.FloatField(default=0.0)),
                ('storage', models.BooleanField(default=False)),
                ('zone', models.IntegerField(default=1, null=True)),
                ('phone_1', models.CharField(blank=True, default='', max_length=300)),
                ('email', models.CharField(blank=True, default='', max_length=300)),
                ('talk_to', models.CharField(blank=True, default='', max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='Repeated',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField(null=True)),
                ('movable_date', models.DateTimeField(default=None, null=True)),
                ('days_of_the_week', models.CharField(blank=True, max_length=60)),
                ('notes', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='RepeatedContract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('zone', models.PositiveIntegerField(blank=True, null=True)),
                ('distance', models.FloatField(blank=True, null=True)),
                ('price', models.FloatField(blank=True, null=True)),
                ('extra', models.FloatField(null=True)),
                ('type', models.CharField(default='einzelfahrt', max_length=100)),
                ('fromrepeated', models.BooleanField(blank=True, default=False)),
                ('repeated_id', models.PositiveIntegerField(blank=True, null=True)),
                ('repeated_deleted', models.BooleanField(blank=True, default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('basezone_price', models.FloatField(default=8.0)),
                ('addzone_price', models.FloatField(default=4.0)),
                ('express_price', models.FloatField(default=4.0)),
                ('express_price_zone_size', models.IntegerField(default=2)),
                ('zone_size', models.FloatField(default=3.0)),
                ('addzone_size', models.FloatField(default=2.0)),
                ('city', models.CharField(default='Wien', max_length=100)),
                ('gps_lat', models.FloatField(default=48.216618)),
                ('gps_lon', models.FloatField(default=16.385031)),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='disposerv_profile', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('isDispo', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Street',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=400)),
                ('name_street', models.CharField(default='', max_length=400)),
                ('nr_von', models.CharField(max_length=10, null=True)),
                ('nr_bis', models.CharField(max_length=10, null=True)),
                ('postal_code', models.CharField(max_length=4)),
                ('lat', models.FloatField(default=16)),
                ('lon', models.FloatField(default=48)),
            ],
        ),
        migrations.CreateModel(
            name='StreetWithNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=400)),
                ('nr', models.CharField(max_length=10, null=True)),
                ('postal_code', models.CharField(max_length=4)),
                ('lat', models.FloatField(default=16)),
                ('lon', models.FloatField(default=48)),
            ],
        ),
        migrations.CreateModel(
            name='ContractPosition',
            fields=[
                ('position_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='disposerv.position')),
            ],
            bases=('disposerv.position',),
        ),
        migrations.CreateModel(
            name='PositionAddress',
            fields=[
                ('address_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='disposerv.address')),
            ],
            bases=('disposerv.address',),
        ),
        migrations.CreateModel(
            name='RepeatedContractPosition',
            fields=[
                ('position_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='disposerv.position')),
            ],
            bases=('disposerv.position',),
        ),
        migrations.CreateModel(
            name='RepeatedPositionAddress',
            fields=[
                ('address_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='disposerv.address')),
            ],
            bases=('disposerv.address',),
        ),
        migrations.CreateModel(
            name='TimesRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('start_datetime', models.DateTimeField(blank=True, null=True)),
                ('end_datetime', models.DateTimeField(blank=True, null=True)),
                ('mode', models.CharField(default='fahrer', max_length=10)),
                ('staff_member', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='times', to='disposerv.staff')),
            ],
        ),
        migrations.AddIndex(
            model_name='streetwithnumber',
            index=models.Index(fields=['name', 'nr'], name='disposerv_s_name_9def91_idx'),
        ),
        migrations.AddIndex(
            model_name='street',
            index=models.Index(fields=['name', 'name_street', 'nr_von', 'nr_bis'], name='disposerv_s_name_0ad964_idx'),
        ),
        migrations.AddField(
            model_name='repeatedcontract',
            name='customer',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='disposerv.customer'),
        ),
        migrations.AddField(
            model_name='repeated',
            name='contract',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='repeated', to='disposerv.repeatedcontract'),
        ),
        migrations.AddField(
            model_name='position',
            name='customer',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer', to='disposerv.customer'),
        ),
        migrations.AddField(
            model_name='historicalstaff',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalstaff',
            name='user',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='dispo',
            name='contract',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='disposerv.contract'),
        ),
        migrations.AddField(
            model_name='dispo',
            name='dispatched_to',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='disposerv.staff'),
        ),
        migrations.AddField(
            model_name='contract',
            name='customer',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='disposerv.customer'),
        ),
        migrations.AddField(
            model_name='address',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='addresses', to='disposerv.customer'),
        ),
        migrations.AddIndex(
            model_name='timesrecord',
            index=models.Index(fields=['date', 'start_datetime', 'end_datetime', 'mode', 'staff_member'], name='disposerv_t_date_978892_idx'),
        ),
        migrations.AddField(
            model_name='repeatedpositionaddress',
            name='position',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='address', to='disposerv.repeatedcontractposition'),
        ),
        migrations.AddField(
            model_name='repeatedcontractposition',
            name='contract',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='positions', to='disposerv.repeatedcontract'),
        ),
        migrations.AddField(
            model_name='positionaddress',
            name='position',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='address', to='disposerv.contractposition'),
        ),
        migrations.AddIndex(
            model_name='position',
            index=models.Index(fields=['start_time'], name='disposerv_p_start_t_79ea4c_idx'),
        ),
        migrations.AddField(
            model_name='dispo',
            name='position',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='dispo', to='disposerv.contractposition'),
        ),
        migrations.AddField(
            model_name='contractposition',
            name='contract',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='positions', to='disposerv.contract'),
        ),
        migrations.AddField(
            model_name='addressreapeatedposition',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='positions', to='disposerv.repeatedpositionaddress'),
        ),
        migrations.AddField(
            model_name='addressreapeatedposition',
            name='position',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='addressposition', to='disposerv.repeatedcontractposition'),
        ),
        migrations.AddField(
            model_name='addressposition',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='positions', to='disposerv.positionaddress'),
        ),
        migrations.AddField(
            model_name='addressposition',
            name='position',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='addressposition', to='disposerv.contractposition'),
        ),
    ]
