test = {
    "name": "state",
    "points": 3,
    "suites": [ 
        {
            "cases": [ 
                {
                    "code": r"""
                    >>> import pickle
                    >>> a_file = open("Practical04_Support/pickle/expected_output.pk", "rb")
                    >>> data = pickle.load(a_file)
                    >>> total_correct = np.sum(np.all(np.isclose(state, data["state"], rtol=0.05, atol=0.05), axis=1))
                    >>> total_correct >= data["state"].shape[0] * 0.5
                    True
                    """,
                    "hidden": False,
                    "locked": False,
                }
            ],
            "scored": False,
            "setup": "",
            "teardown": "",
            "type": "doctest"
        }
    ]
}