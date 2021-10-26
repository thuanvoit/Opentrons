# position from center
center_cart = types.Location(chacha['A6'].from_center_cartesian(-1, 1, -i), chacha["A6"])
pipette.move_to(location=center_cart, speed=200)