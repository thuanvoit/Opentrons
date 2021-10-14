#Importing necessary operating files

from opentrons import protocol_api

metadata = {'apiLevel':'2.0',
           'protocolName': 'ChaChaDemo2',
           'author': 'Luke',
           'description': 'test'}

def run(protocol: protocol_api.ProtocolContext):

    # Pipette and Tip Configuration

    tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', '8')
    p300 = protocol.load_instrument('p300_single',
        mount='left',
        tip_racks=[tiprack],
    )

    # Defining Aliquots and Slides

    mothership = protocol.load_labware('opentrons_24_tuberack_nest_2ml_snapcap', '1')
    chacha = protocol.load_labware('corning_96_wellplate_360ul_flat', '3')
    wf = protocol.load_labware('axygen_1_reservoir_90ml', '10')


    # 1. Application of Stain Demo

    p300.pick_up_tip()
    p300.move_to(mothership['A1'].top(130))
    p300.mix(5, 200, mothership['A1'])
    p300.aspirate(300, mothership['A1'])
    p300.move_to(mothership['A1'].top(130))
    p300.dispense(100, chacha['F2'])
    p300.dispense(100, chacha['G2'])
    p300.dispense(100, chacha['H2'])
    p300.move_to(mothership['A1'].top(130))
    p300.aspirate(100, mothership['A1'])
    p300.move_to(mothership['A1'].top(130))
    p300.dispense(100, chacha['H2'])
    p300.drop_tip()


    # 2. Wash Demo (600ul/slide/wash)
    p300.move_to(chacha['A7'].bottom(-28))
    protocol.delay(seconds=5)
    p300.move_to(chacha['H7'].bottom(-11))
    p300.pick_up_tip(tiprack['B1'])

    for x in range(0, 2):
        #   Slide A
        p300.aspirate(300, wf['A1'])
        p300.move_to(chacha['F2'].top())
        theta = 0.0
        while p300.current_volume > 0:
            well_edge = chacha['F2'].from_center(r=2.0, theta=theta, h=0.9)
            destination = (chacha['F2'], well_edge)
            p300.move_to(destination.top())
            p300.dispense(20)
            theta += 0.314
        p300.aspirate(300, wf['A1'])
        while p300.current_volume > 0:
            well_edge = chacha['H2'].from_center(r=2.0, theta=theta, h=0.9)
            destination = (chacha['H2'], well_edge)
            p300.move_to(destination.top())
            p300.dispense(20)
            theta += 0.314

            #   Slide A Rinse
        p300.aspirate(300, wf['A1'])
        p300.move_to(chacha['H1'].top(5))
        p300.dispense(100)
        p300.move_to(chacha['H2'].top(5))
        p300.dispense(100)
        p300.move_to(chacha['H3'].top(5))
        p300.dispense(100)

        p300.return_tip(tiprack['B1'])
        p300.move_to(chacha['H7'].bottom(-11))
        p300.pick_up_tip(tiprack['B1'])


