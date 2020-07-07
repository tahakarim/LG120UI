token = None
expier_time = None
payload = {
            "field_id": "12345678901",
            "is_ctf": False,
            "is_headland_width_optimized": False,
            "headland_width": 0,
            "constraints": [
                {
                    "width": 10,
                    "priority": 1,
                    "turning_radius": 10,
                    "ramp_up_distance": 10,
                    "ramp_down_distance": 10
                }
            ],
            "field": {
                "name": "Skywalker Ranch",
                "boundary": [
                    {
                        "lat": "123", "long": "456"
                    },
                    {
                        "lat": "234", "long": "567"
                    },
                    {
                        "lat": "345", "long": "678"
                    },
                    {
                        "lat": "456", "long": "789"
                    }
                ],
                "gate": [
                    {
                        "lat": "123", "long": "456"
                    }
                ],
                "row_direction": [
                    {
                        "lat": "123", "long": "456"
                    }
                ]
            }
        }
