from opentrons import protocol_api

metadata = {
    'protocolName': 'opal_assay_testing_CD8',
    'author': 'thuanvo',
    'description': 'Testing Opal Assay CD8 Protocol',
    'apiLevel': '2.10'
}

def run(protocol: protocol_api.ProtocolContext):
    tiprack_300ul = protocol.load_labware('opentrons_96_tiprack_300ul', '1')
    mothership_15ml = protocol.load_labware('mothership_24_tuberack_15000ul', '2')