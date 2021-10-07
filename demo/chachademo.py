from opentrons import protocol_api, types
import numpy as np

# metadata
metadata = {
    'protocolName': 'Chacha demo in details',
    'author': 'tv',
    'description': 'Simple protocol to get started using OT2',
    'apiLevel': '2.10'
}

rows = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P']

def run(protocol: protocol_api.ProtocolContext):
    # labware
    tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', location='1')
    chacha = protocol.load_labware('corning_384_wellplate_112ul_flat', location='2')
    # pipettes
    left_pipette = protocol.load_instrument(
         'p300_single', 'left', tip_racks=[tiprack])

    #command
    left_pipette.pick_up_tip()

    for i in np.arange(0.0, 1.0, 0.2):
        center_cart = types.Location(chacha['A6'].from_center_cartesian(-1, 1, -i), chacha["A6"])

        left_pipette.aspirate(1, center_cart)
        
        protocol.delay(seconds=1) 

    center_cart = types.Location(chacha['P6'].from_center_cartesian(-1, 1, 1), chacha["P6"])

    left_pipette.aspirate(1, center_cart)
        
    protocol.delay(seconds=1)    
    
    left_pipette.drop_tip()