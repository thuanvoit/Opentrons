from opentrons import protocol_api

#meta
metadata = {
    'protocolName': 'p1000',
    'author': 'thuanvo',
    'description': 'Demo version',
    'apiLevel': '2.10'
}

def run(protocol: protocol_api.ProtocolContext):

    pipette = protocol.load_instrument('p1000_single', 'right', tip_racks=[])

    well = protocol.load_labware('agilent_1_reservoir_290ml', location='5')

    pipette.move_to(well['A1'].top())

    protocol.delay(seconds=1)

    pipette.move_to(well['A1'].bottom())

    protocol.pause()
    
    for i in range(10):

        pipette.move_to(well['A1'].top(i))

        protocol.pause()
    
    protocol.home()
    
    