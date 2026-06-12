def validate_data(data):

    errors = []

    co_values = [
        data.get("co1"),
        data.get("co2"),
        data.get("co3"),
        data.get("co4"),
        data.get("co5")
    ]

    # -----------------------------------
    # CO validation
    # -----------------------------------

    for i, val in enumerate(co_values, start=1):

        if val is None:
            errors.append(f"co{i} missing")

        elif not (0 <= val <= 20):
            errors.append(f"co{i} invalid")

    # -----------------------------------
    # TOTAL validation
    # -----------------------------------

    valid_cos = [c for c in co_values if c is not None]

    if len(valid_cos) == 5 and data.get("total") is not None:

        total_calc = sum(valid_cos)

        if total_calc != data["total"]:
            errors.append("Total mismatch")

    else:
        errors.append("Incomplete CO data")

    return errors