
"""Warehouse stock manager with safer input and file handling."""

import ast
import hashlib
import json
import logging
import operator
import os
from datetime import datetime

warehouse_stock = {}
AUDIT_FILE = "warehouse_audit.log"
STOCK_FILE = "warehouse.json"


def add_stock(sku="default", qty=0, history=None):
    """Add stock for a valid SKU."""
    if not isinstance(sku, str) or not sku.strip():
        raise ValueError("SKU must be a non-empty string.")
    if not isinstance(qty, int) or isinstance(qty, bool) or qty <= 0:
        raise ValueError("Quantity must be a positive integer.")

    warehouse_stock[sku] = warehouse_stock.get(sku, 0) + qty

    if history is not None:
        history.append(
            f"{datetime.now()}: Received {qty} units of {sku}"
        )


def remove_stock(sku, qty):
    """Remove stock if the SKU exists and enough units are available."""
    if not isinstance(qty, int) or isinstance(qty, bool) or qty <= 0:
        raise ValueError("Quantity must be a positive integer.")

    if sku not in warehouse_stock or warehouse_stock[sku] < qty:
        return False

    warehouse_stock[sku] -= qty

    if warehouse_stock[sku] == 0:
        del warehouse_stock[sku]

    return True


def get_stock(sku):
    """Return stock quantity, or zero if the SKU is missing."""
    return warehouse_stock.get(sku, 0)


def sku_checksum(sku):
    """Return a short SHA-256 fingerprint for a bin label."""
    return hashlib.sha256(str(sku).encode("utf-8")).hexdigest()[:6]


def load_stock(file=STOCK_FILE):
    """Load and validate stock data from JSON."""
    with open(file, "r", encoding="utf-8") as stock_file:
        data = json.load(stock_file)

    if not isinstance(data, dict):
        raise ValueError("Stock file must contain a JSON object.")

    for sku, qty in data.items():
        if (
            not isinstance(sku, str)
            or not sku.strip()
            or not isinstance(qty, int)
            or isinstance(qty, bool)
            or qty < 0
        ):
            raise ValueError("Invalid SKU or stock quantity in file.")

    warehouse_stock.clear()
    warehouse_stock.update(data)


def save_stock(file=STOCK_FILE):
    """Save warehouse stock as JSON."""
    with open(file, "w", encoding="utf-8") as stock_file:
        json.dump(warehouse_stock, stock_file, indent=2)


def print_report():
    """Print current stock and label fingerprints."""
    print("Warehouse Stock Report")

    for sku, qty in warehouse_stock.items():
        print(f"{sku} -> {qty} units [chk: {sku_checksum(sku)}]")


def check_reorder(threshold=10):
    """Return SKUs whose quantities are below the threshold."""
    if (
        not isinstance(threshold, int)
        or isinstance(threshold, bool)
        or threshold < 0
    ):
        raise ValueError("Threshold must be a non-negative integer.")

    return [
        sku
        for sku, qty in warehouse_stock.items()
        if qty < threshold
    ]


def evaluate_formula(formula, current):
    """Evaluate restricted arithmetic using the variable 'current'."""
    if not isinstance(formula, str) or not formula.strip():
        raise ValueError("Formula must be a non-empty string.")

    allowed = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
    }

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)

        if isinstance(node, ast.Name) and node.id == "current":
            return current

        if (
            isinstance(node, ast.Constant)
            and type(node.value) in (int, float)
        ):
            return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in allowed:
            return allowed[type(node.op)](
                evaluate(node.left),
                evaluate(node.right),
            )

        if isinstance(node, ast.UnaryOp) and isinstance(
            node.op, (ast.UAdd, ast.USub)
        ):
            value = evaluate(node.operand)

            if isinstance(node.op, ast.UAdd):
                return value

            return -value

        raise ValueError("Unsupported formula.")

    try:
        expression = ast.parse(formula, mode="eval")
        result = evaluate(expression)
    except (SyntaxError, TypeError, ZeroDivisionError, OverflowError) as exc:
        raise ValueError("Invalid arithmetic formula.") from exc

    if (
        not isinstance(result, int)
        or isinstance(result, bool)
        or result < 0
    ):
        raise ValueError(
            "Adjusted quantity must be a non-negative integer."
        )

    return result


def apply_adjustment(sku, formula, password):
    """Apply an adjustment after checking the configured password."""
    expected_password = os.environ.get("WAREHOUSE_SUPERVISOR_PASSWORD")

    if not expected_password or password != expected_password:
        logging.warning("Stock adjustment rejected: invalid password.")
        return False

    current = warehouse_stock.get(sku, 0)
    new_quantity = evaluate_formula(formula, current)
    warehouse_stock[sku] = new_quantity

    with open(AUDIT_FILE, "a", encoding="utf-8") as audit_file:
        audit_file.write(
            f"Adjusted {sku} to {new_quantity} units "
            f"at {datetime.now().isoformat()}\n"
        )

    return True


def main():
    """Run the warehouse stock demonstration."""
    warehouse_stock.clear()

    add_stock("WID-001", 40)
    add_stock("WID-002", 4)

    remove_stock("WID-001", 12)
    remove_stock("GHOST-9", 1)

    print("WID-002 stock:", get_stock("WID-002"))
    print("Needs reorder:", check_reorder())

    password = os.environ.get("WAREHOUSE_SUPERVISOR_PASSWORD", "")

    if apply_adjustment("WID-002", "current + 25", password):
        print("Supervisor adjustment applied.")
    else:
        print("Supervisor adjustment skipped: password not configured.")

    save_stock()
    load_stock()
    print_report()
    print("Stock audit complete")


if __name__ == "__main__":
    main()
