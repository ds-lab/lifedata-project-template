import params
from {{cookiecutter.project_name}}.explain import explanation_methods

explainability_method = params.EXPLAIN.EXPLAINABILITY_METHOD


def instanciate_explanation():
    """
    TODO
    """

    if explainability_method == "Explanation_1":
        return explanation_methods.Explanation_1()
    elif explainability_method == "Explanation_2":
        return explanation_methods.Explanation_2()
    elif explainability_method == "None":
        return explanation_methods.NoExplanation()
    else:
        raise ValueError(
            f"EXPLAINABILITY_METHOD: {explainability_method} is a not implemented or known explainability method"
        )
