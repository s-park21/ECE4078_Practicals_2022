test = {
    "name": "architecture",
    "points": 3,
    "suites": [
        {
            "cases": [
                {
                    "code": r"""
                    >>> import pickle
                    >>> a_file = open("Practical05_Support/pickle/expected_architecture.pk", "rb")
                    >>> true_model = pickle.load(a_file)
                    >>> st_model = ConvNet()
                    >>> layers_condition = []
                    >>> for param_tensor, param_tensor_new in zip(st_model.state_dict(), true_model.state_dict()):
                    ...     layers_condition.append((st_model.state_dict()[param_tensor_new].size() ==  true_model.state_dict()[param_tensor_new].size()))
                    >>> all(layers_condition)
                    True
                    """,
                    "hidden": False,
                    "locked": False,
                }
            ],
            "scored": True,
            "setup": "",
            "teardown": "",
            "type": "doctest"
        }
    ]
}