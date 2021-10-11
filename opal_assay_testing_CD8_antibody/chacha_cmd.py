# rows chacha_labware
rows = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P']


#wash stuff
def chacha_washing(protocol, pipette, chacha_labware, wash_n_time):
    for i in range(wash_n_time):
        pipette.move_to(chacha_labware['A6'].top(20))
        pipette.move_to(chacha_labware['A6'].top(-5), speed=20)
        pipette.move_to(chacha_labware['A6'].top(-10), speed=150)
        pipette.move_to(chacha_labware['L6'].top(5))
        pipette.move_to(chacha_labware['A6'].top(20))
        pipette.move_to(chacha_labware['A6'].top(-5), speed=50)
        pipette.move_to(chacha_labware['A6'].top(-10), speed=170)
        protocol.delay(seconds=5)
        pipette.move_to(chacha_labware['L6'].top(20))
        pipette.move_to(chacha_labware['L6'].top(), speed=20)

#blocking method
def chacha_blocking(protocol, pipette, chacha_labware, from_tupe, volume, to_cols, to_rows):
    pipette.aspirate(volume, from_tupe)
    for col in to_cols:
        for row in to_rows:
            pipette.dispense(volume/4, location=chacha_labware[row+col].top(), rate=0.5)
    pipette.blow_out(location=chacha_labware[to_rows[-1]+to_cols[-1]].top())
   