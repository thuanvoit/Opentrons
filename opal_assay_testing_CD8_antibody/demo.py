from opentrons import protocol_api
from opentrons.commands.protocol_commands import delay

##################
# rows chacha_labware
rows = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P']

class Opentron_Chacha:
    def __init__(self, protocol, pipette, chacha_labware, tuberack, antibody_solution, blocking_position):
        self.protocol = protocol
        self.pipette = pipette
        self.chacha_labware = chacha_labware
        self.tuberack = tuberack
        self.antibody_solution = antibody_solution
        self.blocking_position = blocking_position

    def check_antibodies(self):
        for antibody in self.antibody_solution:
            if antibody != "empty":
                self.pipette.move_to(self.chacha_labware[self.antibody_solution[antibody]['position']].top(20))
                self.protocol.comment('--------------------------------------------------')
                self.protocol.comment(f"PLEASE CANCEL IF '{antibody}' IS NOT AT TUBERACK '{self.antibody_solution[antibody]['position']}'")
                self.protocol.comment(f"TASKS WILL RESUME IN 5 SECONDS")
                self.protocol.comment('--------------------------------------------------')
                self.protocol.delay(seconds=5)
        self.protocol.comment("CHECKING SUCESSFULLY")
        
        
    #wash stuff
    def washing(self, wash_n_time):
        for i in range(wash_n_time):
            self.pipette.move_to(self.chacha_labware['A6'].top(20))
            self.pipette.move_to(self.chacha_labware['A6'].top(-5), speed=100)
            self.pipette.move_to(self.chacha_labware['A6'].top(-13))
            

            self.pipette.move_to(self.chacha_labware['L6'].top(20))
            self.pipette.move_to(self.chacha_labware['L6'].top(-2), speed=50)


            self.pipette.move_to(self.chacha_labware['A6'].top(20))
            self.pipette.move_to(self.chacha_labware['A6'].top(-5), speed=100)
            self.pipette.move_to(self.chacha_labware['A6'].top(-13))

            self.protocol.delay(seconds=5)
        self.pipette.move_to(self.chacha_labware['L6'].top(20))
        self.pipette.move_to(self.chacha_labware['L6'].top(-2), speed=50)



    def process_info(self, antibody_type):
        if antibody_type in self.antibody_solution.keys():
            position = self.antibody_solution[antibody_type]['position']
            volume = self.antibody_solution[antibody_type]['volume']
            time = [self.antibody_solution[antibody_type]['time']['mins'], self.antibody_solution[antibody_type]['time']['sec']]
            return [position, volume, time]
        else:
            self.protocol.pause(f"ERROR: '{antibody_type}' is not one of antibody_solution defined")
            return None

    #blocking method
    def blocking(self, antibody_type, to_cols, to_rows):
        info = self.process_info(antibody_type)
        self.pipette.aspirate(info[1], self.tuberack[info[0]])
        for col in to_cols:
            for row in to_rows:
                self.pipette.dispense(info[1]/4, location=self.chacha_labware[row+col].top())
        self.pipette.blow_out(location=self.chacha_labware[to_rows[-1]+to_cols[-1]].top())
        self.protocol.delay(minutes=info[2][0], seconds=info[2][1])
        

    # TBST RINSING
    def rinsing_with_tbst(self, antibody_type, slides_number, n_time):
        info = self.process_info(antibody_type)
        self.pipette.pick_up_tip()

        for n in range(n_time):
            # Washing TBST 6 times (30 seconds * 6 = 2 mins)
            for j in range(6):
                for i in range(slides_number):
                    self.blocking(antibody_type, self.blocking_position[f'slide{i+1}']['cols'], 
                                                        self.blocking_position[f'slide{i+1}']['rows'])
                self.protocol.delay(minutes=info[2][0], seconds=info[2][1])
            self.washing(3)
        
        #Remove OLD Tip
        self.pipette.drop_tip()
        ######## REMOVE TBST #########################

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


def run(protocol: protocol_api.ProtocolContext):
    #labware
    tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', location='1')
    chacha_labware = protocol.load_labware('corning_384_wellplate_112ul_flat', location='2')
    tuberack = protocol.load_labware('opentrons_15_tuberack_falcon_15ml_conical', location='7')
    
    #pipettes
    pipette = protocol.load_instrument('p300_single', 'left', tip_racks=[tiprack])

    #tube introduce for opentrons_15_tuberack_falcon_15ml_conical
    antibody_solution = {
        # --- 1ST ROW ---
        'opal_antibody_dilluent': {'position': 'A1', 'volume': 300, 'time': {"mins": 30, "sec": 0}},
        'cd8_antibody': {'position': 'A2', 'volume': 300, 'time': {"mins": 30, "sec": 0}},
        'tbst': {'position': 'A3', 'volume': 200, 'time': {"mins": 0, "sec": 30}},
        'opal_polymer_HRP': {'position': 'A4', 'volume': 300, 'time': {"mins": 10, "sec": 0}},
        'opal_fluorophore': {'position': 'A5', 'volume': 300, 'time': {"mins": 10, "sec": 0}},
        
        # --- 2ND ROW ---
        'ar6_buffer': {'position': 'B1', 'volume': 300, 'time': {"mins": 0, "sec": 5}},
        'empty': {'position': 'B2', 'volume': 0, 'time': {"mins": 0, "sec": 0}},
        'empty': {'position': 'B3', 'volume': 0, 'time': {"mins": 0, "sec": 0}},
        'empty': {'position': 'B4', 'volume': 0, 'time': {"mins": 0, "sec": 0}},
        'empty': {'position': 'B5', 'volume': 0, 'time': {"mins": 0, "sec": 0}},
        # --- 3RD ROW ---
        'empty': {'position': 'C1', 'volume': 0, 'time': {"mins": 0, "sec": 0}},
        'empty': {'position': 'C2', 'volume': 0, 'time': {"mins": 0, "sec": 0}},
        'empty': {'position': 'C3', 'volume': 0, 'time': {"mins": 0, "sec": 0}},
        'empty': {'position': 'C4', 'volume': 0, 'time': {"mins": 0, "sec": 0}},
        'empty': {'position': 'C5', 'volume': 0, 'time': {"mins": 0, "sec": 0}},


    }

    # INTRODUCE BLOCKING POSITION
    slides_number = 4

    #chacha1
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

    #command

    ###################################################################
    ######## BLOCKING using Opal Antibody Dilluent ####################
    ###################################################################

    chacha = Opentron_Chacha(protocol, pipette, chacha_labware, tuberack, antibody_solution, blocking_position)

    chacha.check_antibodies()

    pipette.pick_up_tip()
    
    # BLOCKING
    for i in range(slides_number):
        chacha.blocking('opal_antibody_dilluent', 
                        blocking_position[f'slide{i+1}']['cols'], 
                        blocking_position[f'slide{i+1}']['rows'])

    
    # Drain Blocking Buffer
    chacha.washing(3)

    # Remove the tip
    pipette.drop_tip()
    
    ###################################################################
    ######## PRIMARY ANTIBODY INCUBATION ##############################
    ###################################################################
    pipette.pick_up_tip()
    
    # BLOCKING PRIMARY ANTIBODY INCUBATION
    for i in range(slides_number):
        chacha.blocking('cd8_antibody', 
                        blocking_position[f'slide{i+1}']['cols'], 
                        blocking_position[f'slide{i+1}']['rows'])

    
    # Drain Blocking Buffer
    chacha.washing(wash_n_time=3)

    # Remove the tip
    pipette.drop_tip()

    chacha.rinsing_with_tbst('tbst', slides_number, 5)

    ###################################################################
    ######## SECONDARY HRP ############################################
    ###################################################################
    pipette.pick_up_tip()

    # Aspirate HRP
    for i in range(slides_number):
        chacha.blocking('opal_polymer_HRP', 
                        blocking_position[f'slide{i+1}']['cols'], 
                        blocking_position[f'slide{i+1}']['rows'])
    
    # Drain Blocking Buffer
    chacha.washing(wash_n_time=3)

    # Remove the tip
    pipette.drop_tip()

    chacha.rinsing_with_tbst('tbst', slides_number, 5)


    ###################################################################
    ######## OPAL FLUOROPHORE #########################################
    ###################################################################
    pipette.pick_up_tip()

    # Aspirate HRP
    for i in range(slides_number):
        chacha.blocking('opal_fluorophore', 
                        blocking_position[f'slide{i+1}']['cols'], 
                        blocking_position[f'slide{i+1}']['rows'])

    # Drain HRP Buffer
    chacha.washing(wash_n_time=3)

    # Remove the tip
    pipette.drop_tip()

    chacha.rinsing_with_tbst('tbst', slides_number, 5)

    ######## AR6 BUFFER ##############################################
    pipette.pick_up_tip()
    for i in range(slides_number):
        chacha.blocking('ar6_buffer', 
                        blocking_position[f'slide{i+1}']['cols'], 
                        blocking_position[f'slide{i+1}']['rows'])

    # Drain AR6 Buffer
    chacha.washing(wash_n_time=3)
    pipette.drop_tip()




    



