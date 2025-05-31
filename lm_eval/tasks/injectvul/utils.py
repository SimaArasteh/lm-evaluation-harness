def calculate_func_score(doc, prediction, *args, **kwargs):
    # Dummy scorer: returns 1.0 if output is non-empty
    return {"tbd": 1.0 if prediction.strip() else 0.0}
