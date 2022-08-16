test = {
    "name": "markers",
    "points": 3,
    "suites": [ 
        {
            "cases": [ 
                {
                    "code": r"""
                    >>> import pickle
                    >>> a_file = open("Practical04_Support/pickle/expected_output.pk", "rb")
                    >>> data = pickle.load(a_file)
                    >>> true_markers = data["markers"]
                    >>> total_markers = true_markers.shape[0]
                    >>> predicted_markers = np.round(slammer.markers.T,2)
                    >>> total_correct = np.sum(np.all(np.isclose(np.round(slammer.markers.T,2), true_markers[slammer.taglist], rtol=0.02, atol=0.01), axis=1))
                    >>> total_correct >= total_markers * 0.5
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