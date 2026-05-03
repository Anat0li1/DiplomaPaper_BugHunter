"""initial schema

Revision ID: 20260503_0001
Revises:
Create Date: 2026-05-03 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "20260503_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("username", sa.String(length=80), nullable=False),
        sa.Column("email", sa.String(length=120), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("active_role", sa.String(length=20), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )

    op.create_table(
        "boards",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "bug_reports",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("given_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("preconditions", sa.Text(), nullable=True),
        sa.Column("postconditions", sa.Text(), nullable=True),
        sa.Column("actual_result", sa.Text(), nullable=True),
        sa.Column("expected_result", sa.Text(), nullable=True),
        sa.Column("severity", sa.String(length=20), nullable=True),
        sa.Column("priority", sa.String(length=20), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=True),
        sa.Column("system_and_browser_inf", sa.String(length=200), nullable=True),
        sa.Column("version", sa.String(length=50), nullable=True),
        sa.Column("environment", sa.String(length=100), nullable=True),
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("test_case_id", sa.String(length=36), nullable=True),
        sa.Column("is_system", sa.Boolean(), nullable=True),
        sa.Column("comments", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "shops",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )

    op.create_table(
        "test_cases",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("given_id", sa.String(length=50), nullable=True),
        sa.Column("application_group", sa.String(length=100), nullable=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("priority", sa.Integer(), nullable=True),
        sa.Column("is_system", sa.Boolean(), nullable=True),
        sa.Column("preconditions", sa.Text(), nullable=True),
        sa.Column("postconditions", sa.Text(), nullable=True),
        sa.Column("version", sa.String(length=50), nullable=True),
        sa.Column("environment", sa.String(length=100), nullable=True),
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("comments", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "categories",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("shop_id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.ForeignKeyConstraint(["shop_id"], ["shops.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("shop_id", "name", name="unique_category_per_shop"),
    )

    op.create_table(
        "columns",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("board_id", sa.String(length=36), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("ordering", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["board_id"], ["boards.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "products",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("shop_id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("price", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=True),
        sa.Column("image_url", sa.String(length=500), nullable=True),
        sa.Column("category", sa.String(length=100), nullable=True),
        sa.ForeignKeyConstraint(["shop_id"], ["shops.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_foreign_key(
        "fk_bug_reports_test_case_id_test_cases",
        "bug_reports",
        "test_cases",
        ["test_case_id"],
        ["id"],
    )

    op.create_table(
        "bug_steps",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("bug_report_id", sa.String(length=36), nullable=False),
        sa.Column("number", sa.Integer(), nullable=False),
        sa.Column("step_name", sa.String(length=200), nullable=False),
        sa.ForeignKeyConstraint(["bug_report_id"], ["bug_reports.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "cart_items",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("product_id", sa.String(length=36), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "orders",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("total_amount", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "tasks",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("column_id", sa.String(length=36), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("doer", sa.String(length=100), nullable=True),
        sa.Column("start_time", sa.DateTime(), nullable=True),
        sa.Column("end_time", sa.DateTime(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=True),
        sa.Column("priority", sa.String(length=20), nullable=True),
        sa.ForeignKeyConstraint(["column_id"], ["columns.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "test_steps",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("test_case_id", sa.String(length=36), nullable=False),
        sa.Column("number", sa.Integer(), nullable=False),
        sa.Column("step_name", sa.String(length=200), nullable=False),
        sa.Column("test_data", sa.Text(), nullable=True),
        sa.Column("expected_result", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["test_case_id"], ["test_cases.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "order_items",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("order_id", sa.String(length=36), nullable=False),
        sa.Column("product_id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("price", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["order_id"], ["orders.id"]),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("order_items")
    op.drop_table("test_steps")
    op.drop_table("tasks")
    op.drop_table("orders")
    op.drop_table("cart_items")
    op.drop_table("bug_steps")
    op.drop_constraint("fk_bug_reports_test_case_id_test_cases", "bug_reports", type_="foreignkey")
    op.drop_table("products")
    op.drop_table("columns")
    op.drop_table("categories")
    op.drop_table("test_cases")
    op.drop_table("shops")
    op.drop_table("bug_reports")
    op.drop_table("boards")
    op.drop_table("users")
