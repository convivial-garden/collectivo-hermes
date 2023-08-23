"""Setup function of the hermes disposerv extension."""
from django.conf import settings
from collectivo.dashboard.models import DashboardTile, DashboardTileButton
from collectivo.extensions.models import Extension
from collectivo.menus.models import MenuItem
from collectivo.components.models import Component




def setup(sender, **kwargs):
    """Initialize extension after database is ready."""

    extension = Extension.objects.register(
        name="disposerv",
        label="Hermes Dispo",
        description="Integration with the direct loan system from habitat.",
        version="1.0.0",
    )

    # User objects
    MenuItem.objects.register(
        name="disposerv",
        label="Dispo",
        parent="main",
        icon_name="pi-money-bill",
        component="1",
        extension=extension,
        requires_group="collectivo.disposerv.user",
        link="http://localhost:8005",
        target="component",
    )

    button = DashboardTileButton.objects.register(
        name="disposerv_button",
        label="Weiter",
        link="http://localhost:8005",
        link_type="external",
    )

    tile = DashboardTile.objects.register(
        name="disposerv_tile",
        label="Dispo",
        extension=extension,
        source="db",
        content="Hier kannst du deine Pakete einsehen und verwalten.",
        requires_group="collectivo.direktkredit.user",
    )


    Component.objects.register(
        name='disposerv',
        type='remote',
        path='http://localhost:4173/assets/disposerv.js',
        extension=extension,
    )

    tile.buttons.set([button])

    # Admin objects
    # TODO Warning if os environ var is missing
    MenuItem.objects.register(
        name="disposerv_admin",
        label="Dispo admin2",
        icon_name="pi-money-bill",
        parent="admin",
        component="1",
        extension=extension,
        requires_group="collectivo.core.admin",
        route="disposerv/disposerv",
        target="component",
        order=1,
    )