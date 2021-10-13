from opentrons import protocol_api
from opentrons.commands.protocol_commands import delay

##################
# rows chacha_labware
rows = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P']


#wash stuff
def chacha_washing(protocol, pipette, chacha_labware, wash_n_time):
    for i in range(wash_n_time):
        pipette.move_to(chacha_labware['A6'].top(20))
        pipette.move_to(chacha_labware['A6'].top(-5), speed=100)
        pipette.move_to(chacha_labware['A6'].top(-13))
        

        pipette.move_to(chacha_labware['L6'].top(20))
        pipette.move_to(chacha_labware['L6'].top(-2), speed=50)


        pipette.move_to(chacha_labware['A6'].top(20))
        pipette.move_to(chacha_labware['A6'].top(-5), speed=100)
        pipette.move_to(chacha_labware['A6'].top(-13))

        protocol.delay(seconds=5)
        pipette.move_to(chacha_labware['L6'].top(20))
        pipette.move_to(chacha_labware['L6'].top(-2), speed=50)


#quick wash
def chacha_quickwash(protocol, pipette, chacha_labware):
    pipette.move_to(chacha_labware['A6'].top(20))
    pipette.move_to(chacha_labware['A6'].top(-5), speed=50)
    pipette.move_to(chacha_labware['A6'].top(-10), speed=150)
    protocol.delay(seconds=5)
    pipette.move_to(chacha_labware['L6'].top(20))
    pipette.move_to(chacha_labware['L6'].top(), speed=20)

#blocking method
def chacha_blocking(protocol, pipette, tuberack, chacha_labware, from_tupe, volume, to_cols, to_rows):
    pipette.aspirate(volume, tuberack[from_tupe])
    for col in to_cols:
        for row in to_rows:
            pipette.dispense(volume/4, location=chacha_labware[row+col].top(), rate=0.5)
    pipette.blow_out(location=chacha_labware[to_rows[-1]+to_cols[-1]].top())
    

# TBST RINSING
def rinsing_with_tbst(protocol, pipette, tuberack, chacha_labware, slides_number, blocking_position, antibody_solution):
    ######## RINSE TBST ##############################################
    pipette.pick_up_tip()


    # Washing TBST 6 times (30 seconds * 6 = 2 mins)
    volume_per_slide = 200
    for j in range(6):
        for i in range(slides_number):
            chacha_blocking(protocol, pipette, tuberack, chacha_labware, 
                                    antibody_solution['tbst'], 
                                    volume_per_slide, 
                                    blocking_position[f'slide{i+1}']['cols'], 
                                    blocking_position[f'slide{i+1}']['rows'])
        protocol.delay(seconds=30)
        chacha_quickwash(protocol, pipette, chacha_labware)
    
    # Last drain before next step
    chacha_washing(protocol, pipette, chacha_labware, 3)
    
    #Remove OLD Tip
    pipette.drop_tip()
    ######## REMOVE TBST #############################################
##################

#meta
metadata = {
    'protocolName': 'Opal Assay Testing CD8 Antibody',
    'author': 'thuanvo',
    'description': 'Demo version',
    'apiLevel': '2.10'
}
    #   RECOMMENDED AREA
    #  ___________________
    # |                   |
    # |      A            |
    # |   ___________     |
    # |  |   B       |    |
    # |  |   C       | OR |  <==  B and C
    # |  |-----------|    |
    # |  |   D       |    |
    # |  |   E       | OR |  <==  D and E
    # |  |-----------|    |
    # |  |   F       |    |
    # |  |   G       | OR |  <==  F and G
    # |  |___________|    |
    # |      H            |
    # |      I            |
    # |      J            |
    # |      K            |
    # |      L            |
    # |      M            |
    # |      N            |
    # |      O            |
    # |      P            |
    # |___________________|
    # |###################|
    # |##### SLIDE #######|
    # |___________________|

# INTRODUCE BLOCKING POSITION
slides_number = 4

blocking_position = {
    'slide1': { 'cols': ['2', '3'], # KEEP CONSTANT
                'rows': ['D', 'E'], # OR
                        #['B', 'C'],
                        #['F', 'G'],
                },
    'slide2': { 'cols': ['9', '10'], # KEEP CONSTANT
                'rows': ['D', 'E'], # OR
                        #['B', 'C'],
                        #['F', 'G'],
                },
    'slide3': { 'cols': ['16', '17'], # KEEP CONSTANT
                'rows': ['D', 'E'], # OR
                        #['B', 'C'],
                        #['F', 'G'],
                },
    'slide4': { 'cols': ['23', '24'], # KEEP CONSTANT
                'rows': ['D', 'E'], # OR
                        #['B', 'C'],
                        #['F', 'G'],
                },
    }




def run(protocol: protocol_api.ProtocolContext):
    #labware
    tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', location='1')
    chacha = protocol.load_labware('corning_384_wellplate_112ul_flat', location='2')
    tuberack = protocol.load_labware('opentrons_15_tuberack_falcon_15ml_conical', location='7')
    
    #pipettes
    pipette = protocol.load_instrument('p300_single', 'left', tip_racks=[tiprack])

    #tube introduce for opentrons_15_tuberack_falcon_15ml_conical
    antibody_solution = {
        # --- 1ST ROW ---
        'opal_antibody_dilluent': 'A1',
        'cd8_antibody': 'A2',
        'tbst': 'A3',
        'opal_polymer_HRP': 'A1',
        'opal_fluorophore': 'A5',
        # --- 2ND ROW ---
        'ar6_buffer': 'B1',
        '': 'B2',
        '': 'B3',
        '': 'B4',
        '': 'B5',
        # --- 3RD ROW ---
        '': 'C1',
        '': 'C2',
        '': 'C3',
        '': 'C4',
        '': 'C5',

    }

    #command

    ###################################################################
    ######## BLOCKING using Opal Antibody Dilluent ####################
    ###################################################################
    pipette.pick_up_tip()
    
    # BLOCKING
    volume_per_slide = 300
    for i in range(slides_number):
        chacha_blocking(protocol, pipette, tuberack, chacha, 
                                    antibody_solution['opal_antibody_dilluent'], 
                                    volume_per_slide, 
                                    blocking_position[f'slide{i+1}']['cols'], 
                                    blocking_position[f'slide{i+1}']['rows'])
    # 10 mins incubate
    # protocol.delay(minutes=10)

    # testing
    protocol.delay(seconds=30)

    
    # Drain Blocking Buffer
    chacha_washing(protocol, pipette, chacha, wash_n_time=3)

    # Remove the tip
    pipette.drop_tip()
    
    ###################################################################
    ######## PRIMARY ANTIBODY INCUBATION ##############################
    ###################################################################
    pipette.pick_up_tip()
    
    # BLOCKING PRIMARY ANTIBODY INCUBATION
    volume_per_slide = 300
    for i in range(slides_number):
        chacha_blocking(protocol, pipette, tuberack, chacha, 
                                    antibody_solution['cd8_antibody'], 
                                    volume_per_slide, 
                                    blocking_position[f'slide{i+1}']['cols'], 
                                    blocking_position[f'slide{i+1}']['rows'])
    # 30 mins incubate
    # protocol.delay(minutes=30)

    #testing
    protocol.delay(seconds=30)

    
    # Drain Blocking Buffer
    chacha_washing(protocol, pipette, chacha, wash_n_time=3)

    # Remove the tip
    pipette.drop_tip()

    rinsing_with_tbst(protocol, pipette, tuberack, chacha, slides_number, blocking_position, antibody_solution)

    ###################################################################
    ######## SECONDARY HRP ############################################
    ###################################################################
    pipette.pick_up_tip()

    # Aspirate HRP
    volume_per_slide = 300
    for i in range(slides_number):
        chacha_blocking(protocol, pipette, tuberack, chacha, 
                                    antibody_solution['opal_polymer_HRP'], 
                                    volume_per_slide, 
                                    blocking_position[f'slide{i+1}']['cols'], 
                                    blocking_position[f'slide{i+1}']['rows'])
    # 10 mins incubate
    #protocol.delay(minutes=10)

    #testing
    protocol.delay(seconds=10)
    
    # Drain Blocking Buffer
    chacha_washing(protocol, pipette, chacha, wash_n_time=3)

    # Remove the tip
    pipette.drop_tip()

    rinsing_with_tbst(protocol, pipette, tuberack, chacha, slides_number, blocking_position, antibody_solution)


    # ###################################################################
    # ######## OPAL FLUOROPHORE #########################################
    # ###################################################################
    # pipette.pick_up_tip()

    # # Aspirate HRP
    # volume_per_slide = 300
    # for i in range(slides_number):
    #     chacha_blocking(protocol, pipette, tuberack, chacha, 
    #                                 antibody_solution['opal_fluorophore'], 
    #                                 volume_per_slide, 
    #                                 blocking_position[f'slide{i+1}']['cols'], 
    #                                 blocking_position[f'slide{i+1}']['rows'])
    # # 10 mins incubate
    # #protocol.delay(minutes=10)

    # #testing
    # protocol.delay(seconds=10)


    # # Drain HRP Buffer
    # chacha_washing(protocol, pipette, chacha, wash_n_time=3)

    # # Remove the tip
    # pipette.drop_tip()

    #rinsing_with_tbst(protocol, pipette, tuberack, chacha, slides_number, blocking_position, antibody_solution)

    # ######## AR6 BUFFER ##############################################

    # volume_per_slide = 300
    # for i in range(slides_number):
    #     chacha_blocking(protocol, pipette, tuberack, chacha, 
    #                                 antibody_solution['ar6_buffer'], 
    #                                 volume_per_slide, 
    #                                 blocking_position[f'slide{i+1}']['cols'], 
    #                                 blocking_position[f'slide{i+1}']['rows'])
    # # 10 mins incubate
    # protocol.delay(seconds=5)

    # # Drain AR6 Buffer
    # chacha_washing(protocol, pipette, chacha, wash_n_time=3)




    



