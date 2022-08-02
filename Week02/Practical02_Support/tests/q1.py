test = {
	"name": "q1",
	"points": 2,
	"suites": [ 
		{
			"cases": [ 
				{
					"code": r"""
					>>> import sys
					>>> sys.stdout.write('skip '); r = np.array(get_rear_wheel_location(np.array([0., 0.]), theta=-np.pi/2, length=3)) # doctest:+ELLIPSIS
					skip ...
					>>> answer = np.array([0,  3])
					>>> np.all(np.isclose(r, answer)) 
					True
					""",
					"hidden": True,
					"locked": False,
				},
				{
					"code": r"""
					>>> import sys
					>>> sys.stdout.write('skip '); r = np.array(get_rear_wheel_location(np.array([-2., 3.]), theta=np.pi/4, length=.5)) # doctest:+ELLIPSIS
					skip ...
					>>> answer = np.array([-2.35355339, 2.64644661])
					>>> np.all(np.isclose(r, answer))
					True
					""",
					"hidden": True,
					"locked": False,
				}, 
				{
					"code": r"""
					>>> import sys
					>>> sys.stdout.write('skip '); r = np.array(get_rear_wheel_location(np.array([0., 10.]), theta=-np.pi/3, length=.1)) # doctest:+ELLIPSIS
					skip ...
					>>> answer = np.array([-0.05, 10.08660254])
					>>> np.all(np.isclose(r, answer)) 
					True
					""",
					"hidden": True,
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
