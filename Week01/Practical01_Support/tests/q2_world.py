test = {
	"name": "q2_world",
	"points": 2,
	"suites": [ 
		{
			"cases": [ 
				{
					"code": r"""
					>>> r = np.round(get_point_in_world_frame(point_c=np.array([0, 1, 3]), gamma=0, disp_c=2, alpha=0, beta=0, disp_b=-1), 2).flatten()
					>>> answer = np.array([0., 0., 5.]).flatten()
					>>> np.all(np.isclose(r, answer))
					True
					""",
					"hidden": True,
					"locked": False,
				},
				{
					"code": r"""
					>>> r = np.round(get_point_in_world_frame(point_c=np.array([2, 0, 2]), gamma=np.pi/2, disp_c=2, alpha=np.pi/2, beta=np.pi/4, disp_b=-1), 2).flatten()
					>>> answer = np.array([0.71, 2., -0.71]).flatten()
					>>> np.all(np.isclose(r, answer))
					True
					""",
					"hidden": True,
					"locked": False,
				},
				{
					"code": r"""
					>>> r = np.round(get_point_in_world_frame(point_c=np.array([1, 1, 1]), gamma=-np.pi/3, disp_c=5, alpha=np.pi/4, beta=np.pi/3, disp_b=10), 2).flatten()
					>>> answer = np.array([-0.25, -0.27, 12.71]).flatten()
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
