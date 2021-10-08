from opentrons import protocol_api, types
import numpy as np

# metadata
metadata = {
    'protocolName': 'Chacha demo in details',
    'author': 'tv',
    'description': 'Testing Chacha with P300',
    'apiLevel': '2.10'
}

rows = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P']

def chacha_wash(protocol, pipette, chacha, n):

    # for i in np.arange(-1.0, 1.0, 0.2):
    #     center_cart = types.Location(chacha['A6'].from_center_cartesian(-1, 1, -i), chacha["A6"])
    #     pipette.move_to(location=center_cart, speed=200)
        #protocol.delay(seconds=2)
        #protocol.pause(f"z={i} waiting")
    #center_cart = types.Location(chacha['A6'].from_center_cartesian(-1, 1, 1), chacha["A6"])
    #pipette.move_to(location=center_cart, speed=50)

    for i in range(3):
        pipette.move_to(chacha['A6'].top(20))
        pipette.move_to(chacha['A6'].top(-10), speed=20)
        #protocol.pause("Check z offset")
        pipette.move_to(chacha['N6'].top(20))
        pipette.move_to(chacha['N6'].top(), speed=20)   

    # for i in np.arange(-1.0, -0.5, -0.1):
    #     center_cart = types.Location(chacha['P6'].from_center_cartesian(-1, 1, -i), chacha["P6"])
    #     pipette.dispense(location=center_cart)
    #     protocol.pause(f"z={i} waiting")
        #protocol.delay(seconds=2) 

    #center_cart = types.Location(chacha['P6'].from_center_cartesian(-1, 1, 1), chacha["P6"])


def run(protocol: protocol_api.ProtocolContext):
    # labware
    tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', location='1')
    chacha = protocol.load_labware('corning_384_wellplate_112ul_flat', location='2')
    # pipettes
    left_pipette = protocol.load_instrument(
         'p300_single', 'left', tip_racks=[tiprack])

    #command
    left_pipette.pick_up_tip()

    #chacha_wash(protocol, left_pipette, chacha, 5)

    
    #left_pipette.dispense(location=center_cart)
        
    #protocol.delay(seconds=1)    
    
    left_pipette.return_tip()