"""base

Revision ID: 0c07baa8d7b2
Revises: 
Create Date: 2022-11-21 00:32:43.382370

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "0c07baa8d7b2"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "config",
        sa.Column("key", sa.Text(), nullable=False),
        sa.Column("value", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("key"),
    )
    op.create_index(op.f("ix_config_key"), "config", ["key"], unique=True)
    op.create_table(
        "usage_points",
        sa.Column("usage_point_id", sa.Text(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("cache", sa.Boolean(), nullable=False),
        sa.Column("consumption", sa.Boolean(), nullable=False),
        sa.Column("consumption_detail", sa.Boolean(), nullable=False),
        sa.Column("production", sa.Boolean(), nullable=False),
        sa.Column("production_detail", sa.Boolean(), nullable=False),
        sa.Column("consumption_price_base", sa.Float(), nullable=False),
        sa.Column("consumption_price_hc", sa.Float(), nullable=False),
        sa.Column("consumption_price_hp", sa.Float(), nullable=False),
        sa.Column("production_price", sa.Float(), nullable=False),
        sa.Column("offpeak_hours_0", sa.Text(), nullable=True),
        sa.Column("offpeak_hours_1", sa.Text(), nullable=True),
        sa.Column("offpeak_hours_2", sa.Text(), nullable=True),
        sa.Column("offpeak_hours_3", sa.Text(), nullable=True),
        sa.Column("offpeak_hours_4", sa.Text(), nullable=True),
        sa.Column("offpeak_hours_5", sa.Text(), nullable=True),
        sa.Column("offpeak_hours_6", sa.Text(), nullable=True),
        sa.Column("plan", sa.Text(), nullable=False),
        sa.Column("refresh_addresse", sa.Boolean(), nullable=False),
        sa.Column("refresh_contract", sa.Boolean(), nullable=False),
        sa.Column("token", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("usage_point_id"),
    )
    op.create_index(
        op.f("ix_usage_points_usage_point_id"),
        "usage_points",
        ["usage_point_id"],
        unique=True,
    )
    op.create_table(
        "addresses",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("usage_point_id", sa.Text(), nullable=False),
        sa.Column("street", sa.Text(), nullable=True),
        sa.Column("locality", sa.Text(), nullable=True),
        sa.Column("postal_code", sa.Text(), nullable=True),
        sa.Column("insee_code", sa.Text(), nullable=True),
        sa.Column("city", sa.Text(), nullable=True),
        sa.Column("country", sa.Text(), nullable=True),
        sa.Column("geo_points", sa.Text(), nullable=True),
        sa.Column("count", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["usage_point_id"],
            ["usage_points.usage_point_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sqlite_autoincrement=True,
    )
    op.create_index(op.f("ix_addresses_id"), "addresses", ["id"], unique=True)
    op.create_index(
        op.f("ix_addresses_usage_point_id"),
        "addresses",
        ["usage_point_id"],
        unique=False,
    )
    op.create_table(
        "consumption_daily",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("usage_point_id", sa.Text(), nullable=False),
        sa.Column("date", sa.DateTime(), nullable=False),
        sa.Column("value", sa.Integer(), nullable=False),
        sa.Column("blacklist", sa.Integer(), nullable=False),
        sa.Column("fail_count", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["usage_point_id"],
            ["usage_points.usage_point_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sqlite_autoincrement=True,
    )
    op.create_index(op.f("ix_consumption_daily_id"), "consumption_daily", ["id"], unique=True)
    op.create_index(
        op.f("ix_consumption_daily_usage_point_id"),
        "consumption_daily",
        ["usage_point_id"],
        unique=False,
    )
    op.create_table(
        "consumption_detail",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("usage_point_id", sa.Text(), nullable=False),
        sa.Column("date", sa.DateTime(), nullable=False),
        sa.Column("value", sa.Integer(), nullable=False),
        sa.Column("interval", sa.Integer(), nullable=False),
        sa.Column("measure_type", sa.Text(), nullable=False),
        sa.Column("blacklist", sa.Integer(), nullable=False),
        sa.Column("fail_count", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["usage_point_id"],
            ["usage_points.usage_point_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        # sqlite_autoincrement=True
    )
    op.create_index(op.f("ix_consumption_detail_id"), "consumption_detail", ["id"], unique=True)
    op.create_index(
        op.f("ix_consumption_detail_usage_point_id"),
        "consumption_detail",
        ["usage_point_id"],
        unique=False,
    )
    op.create_table(
        "contracts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("usage_point_id", sa.Text(), nullable=False),
        sa.Column("usage_point_status", sa.Text(), nullable=False),
        sa.Column("meter_type", sa.Text(), nullable=False),
        sa.Column("segment", sa.Text(), nullable=False),
        sa.Column("subscribed_power", sa.Text(), nullable=False),
        sa.Column("last_activation_date", sa.DateTime(), nullable=False),
        sa.Column("distribution_tariff", sa.Text(), nullable=False),
        sa.Column("offpeak_hours_0", sa.Text(), nullable=True),
        sa.Column("offpeak_hours_1", sa.Text(), nullable=True),
        sa.Column("offpeak_hours_2", sa.Text(), nullable=True),
        sa.Column("offpeak_hours_3", sa.Text(), nullable=True),
        sa.Column("offpeak_hours_4", sa.Text(), nullable=True),
        sa.Column("offpeak_hours_5", sa.Text(), nullable=True),
        sa.Column("offpeak_hours_6", sa.Text(), nullable=True),
        sa.Column("contract_status", sa.Text(), nullable=False),
        sa.Column("last_distribution_tariff_change_date", sa.DateTime(), nullable=False),
        sa.Column("count", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["usage_point_id"],
            ["usage_points.usage_point_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        # sqlite_autoincrement=True
    )
    op.create_index(op.f("ix_contracts_id"), "contracts", ["id"], unique=True)
    op.create_index(
        op.f("ix_contracts_usage_point_id"),
        "contracts",
        ["usage_point_id"],
        unique=False,
    )
    op.create_table(
        "production_daily",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("usage_point_id", sa.Text(), nullable=False),
        sa.Column("date", sa.DateTime(), nullable=False),
        sa.Column("value", sa.Integer(), nullable=False),
        sa.Column("blacklist", sa.Integer(), nullable=False),
        sa.Column("fail_count", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["usage_point_id"],
            ["usage_points.usage_point_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        # sqlite_autoincrement=True
    )
    op.create_index(op.f("ix_production_daily_id"), "production_daily", ["id"], unique=True)
    op.create_index(
        op.f("ix_production_daily_usage_point_id"),
        "production_daily",
        ["usage_point_id"],
        unique=False,
    )
    op.create_table(
        "production_detail",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("usage_point_id", sa.Text(), nullable=False),
        sa.Column("date", sa.DateTime(), nullable=False),
        sa.Column("value", sa.Integer(), nullable=False),
        sa.Column("interval", sa.Integer(), nullable=False),
        sa.Column("measure_type", sa.Text(), nullable=False),
        sa.Column("blacklist", sa.Integer(), nullable=False),
        sa.Column("fail_count", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["usage_point_id"],
            ["usage_points.usage_point_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        # sqlite_autoincrement=True
    )
    op.create_index(op.f("ix_production_detail_id"), "production_detail", ["id"], unique=True)
    op.create_index(
        op.f("ix_production_detail_usage_point_id"),
        "production_detail",
        ["usage_point_id"],
        unique=False,
    )
    op.create_table(
        "statistique",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("usage_point_id", sa.Text(), nullable=False),
        sa.Column("key", sa.Text(), nullable=False),
        sa.Column("value", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["usage_point_id"],
            ["usage_points.usage_point_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sqlite_autoincrement=True,
    )
    op.create_index(op.f("ix_statistique_id"), "statistique", ["id"], unique=True)
    op.create_index(
        op.f("ix_statistique_usage_point_id"),
        "statistique",
        ["usage_point_id"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_statistique_usage_point_id"), table_name="statistique")
    op.drop_index(op.f("ix_statistique_id"), table_name="statistique")
    op.drop_table("statistique")
    op.drop_index(op.f("ix_production_detail_usage_point_id"), table_name="production_detail")
    op.drop_index(op.f("ix_production_detail_id"), table_name="production_detail")
    op.drop_table("production_detail")
    op.drop_index(op.f("ix_production_daily_usage_point_id"), table_name="production_daily")
    op.drop_index(op.f("ix_production_daily_id"), table_name="production_daily")
    op.drop_table("production_daily")
    op.drop_index(op.f("ix_contracts_usage_point_id"), table_name="contracts")
    op.drop_index(op.f("ix_contracts_id"), table_name="contracts")
    op.drop_table("contracts")
    op.drop_index(op.f("ix_consumption_detail_usage_point_id"), table_name="consumption_detail")
    op.drop_index(op.f("ix_consumption_detail_id"), table_name="consumption_detail")
    op.drop_table("consumption_detail")
    op.drop_index(op.f("ix_consumption_daily_usage_point_id"), table_name="consumption_daily")
    op.drop_index(op.f("ix_consumption_daily_id"), table_name="consumption_daily")
    op.drop_table("consumption_daily")
    op.drop_index(op.f("ix_addresses_usage_point_id"), table_name="addresses")
    op.drop_index(op.f("ix_addresses_id"), table_name="addresses")
    op.drop_table("addresses")
    op.drop_index(op.f("ix_usage_points_usage_point_id"), table_name="usage_points")
    op.drop_table("usage_points")
    op.drop_index(op.f("ix_config_key"), table_name="config")
    op.drop_table("config")
    # ### end Alembic commands ###
