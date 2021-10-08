from opentrons import protocol_api, types
import numpy as np
from opentrons.commands.commands import blow_out

# metadata
metadata = {
    'protocolName': 'Chacha demo in details',
    'author': 'tv',
    'description': 'Testing Chacha with P300',
    'apiLevel': '2.10'
}

rows = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P']

blocking_position = {
    'slide1': {'rows': ['F', 'G'], 'cols': ['2', '3']},
    'slide2': {'rows': ['F', 'G'], 'cols': ['9', '10']},
    'slide3': {'rows': ['F', 'G'], 'cols': ['16', '17']},
    'slide4': {'rows': ['F', 'G'], 'cols': ['23', '24']},
    }

def chacha_wash(protocol, pipette, chacha, n):
    for i in range(n):
        pipette.move_to(chacha['A6'].top(20))
        pipette.move_to(chacha['A6'].top(-5), speed=20)
        pipette.move_to(chacha['A6'].top(-10), speed=150)
        protocol.delay(seconds=5)
        pipette.move_to(chacha['L6'].top(20))
        pipette.move_to(chacha['L6'].top(), speed=20)

def chacha_blocking(protocol, pipette, chacha, from_tupe, volume, to_cols, to_rows):
    pipette.aspirate(volume, from_tupe)
    for col in to_cols:
        for row in to_rows:
            pipette.dispense(volume/4, location=chacha[row+col].top(), rate=0.5)
    pipette.blow_out(location=chacha[to_rows[-1]+to_cols[-1]].top())
   

def run(protocol: protocol_api.ProtocolContext):
    # labware
    tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', location='1')
    chacha = protocol.load_labware('corning_384_wellplate_112ul_flat', location='2')
    tuberack = protocol.load_labware('opentrons_15_tuberack_falcon_15ml_conical', location='7')
    # pipettes
    left_pipette = protocol.load_instrument(
         'p300_single', 'left', tip_racks=[tiprack])

    # H20 at Tuberack A1
    h2o_tube = tuberack['A1']

    #command
    left_pipette.pick_up_tip()
    
    # left_pipette.aspirate(300, tuberack['A1'])
    # left_pipette.dispense(300, tuberack['A1'].top(-10))

    # left_pipette.blow_out(tuberack['A1'].top(-10))

    chacha_blocking(protocol, left_pipette, chacha, h2o_tube, 300, blocking_position['slide1']['cols'], blocking_position['slide1']['rows'])
    chacha_blocking(protocol, left_pipette, chacha, h2o_tube, 300, blocking_position['slide2']['cols'], blocking_position['slide2']['rows'])
    chacha_blocking(protocol, left_pipette, chacha, h2o_tube, 300, blocking_position['slide3']['cols'], blocking_position['slide3']['rows'])
    chacha_wash(protocol, left_pipette, chacha, 3)

    left_pipette.return_tip()