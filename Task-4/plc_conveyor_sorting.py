# ============================================================
# DECODELABS PROJECT 4
# PLC-BASED CONVEYOR SORTING SYSTEM
#
# Simulated industrial control system demonstrating:
# - Digital input mapping
# - Digital output mapping
# - Conveyor sequence control
# - Box size detection
# - Pneumatic sorting pushers
# - Emergency Stop safety interlock
# - State-machine based PLC logic
# ============================================================


# ------------------------------------------------------------
# DIGITAL INPUTS
# ------------------------------------------------------------

class DigitalInputs:

    def __init__(self):

        self.start_button = False
        self.stop_button = False
        self.emergency_stop = False

        self.box_sensor = False
        self.small_box_sensor = False
        self.large_box_sensor = False


# ------------------------------------------------------------
# DIGITAL OUTPUTS
# ------------------------------------------------------------

class DigitalOutputs:

    def __init__(self):

        self.conveyor_motor = False
        self.small_box_pusher = False
        self.large_box_pusher = False
        self.green_indicator = False
        self.red_indicator = False


# ------------------------------------------------------------
# PLC CONTROLLER
# ------------------------------------------------------------

class ConveyorPLC:

    def __init__(self):

        self.inputs = DigitalInputs()
        self.outputs = DigitalOutputs()

        self.system_running = False
        self.current_box = None

        self.total_boxes = 0
        self.small_boxes = 0
        self.large_boxes = 0
        self.rejected_boxes = 0

    # --------------------------------------------------------
    # SAFETY INTERLOCK
    # --------------------------------------------------------

    def safety_interlock(self):

        if self.inputs.emergency_stop:

            self.system_running = False

            self.outputs.conveyor_motor = False
            self.outputs.small_box_pusher = False
            self.outputs.large_box_pusher = False

            self.outputs.green_indicator = False
            self.outputs.red_indicator = True

            print()
            print("!!! EMERGENCY STOP ACTIVATED !!!")
            print("Conveyor motor: OFF")
            print("All pneumatic pushers: OFF")
            print("System safely stopped.")

            return False

        self.outputs.red_indicator = False

        return True

    # --------------------------------------------------------
    # START SYSTEM
    # --------------------------------------------------------

    def start_system(self):

        if not self.safety_interlock():

            return

        if self.inputs.start_button:

            self.system_running = True
            self.outputs.conveyor_motor = True
            self.outputs.green_indicator = True

            print()
            print("START BUTTON ACTIVATED")
            print("Conveyor motor: ON")
            print("System running.")

    # --------------------------------------------------------
    # STOP SYSTEM
    # --------------------------------------------------------

    def stop_system(self):

        if self.inputs.stop_button:

            self.system_running = False

            self.outputs.conveyor_motor = False
            self.outputs.small_box_pusher = False
            self.outputs.large_box_pusher = False

            self.outputs.green_indicator = False

            print()
            print("STOP BUTTON ACTIVATED")
            print("Conveyor motor: OFF")
            print("System stopped.")

    # --------------------------------------------------------
    # DETECT BOX
    # --------------------------------------------------------

    def detect_box(self):

        if not self.system_running:

            return

        if self.inputs.box_sensor:

            self.total_boxes += 1

            print()
            print("BOX DETECTED ON CONVEYOR")

            if self.inputs.small_box_sensor:

                self.current_box = "SMALL"

                print("Box classification: SMALL")

            elif self.inputs.large_box_sensor:

                self.current_box = "LARGE"

                print("Box classification: LARGE")

            else:

                self.current_box = "UNKNOWN"

                print("Box classification: UNKNOWN")

    # --------------------------------------------------------
    # SORT BOX
    # --------------------------------------------------------

    def sort_box(self):

        if not self.system_running:

            return

        if self.current_box == "SMALL":

            self.outputs.conveyor_motor = False
            self.outputs.small_box_pusher = True

            print()
            print("SORTING ACTION")
            print("Small-box pusher: EXTENDED")
            print("Small box sorted successfully.")

            self.small_boxes += 1

            # Retract pusher
            self.outputs.small_box_pusher = False

            self.outputs.conveyor_motor = True

            print("Small-box pusher: RETRACTED")
            print("Conveyor motor: ON")

        elif self.current_box == "LARGE":

            self.outputs.conveyor_motor = False
            self.outputs.large_box_pusher = True

            print()
            print("SORTING ACTION")
            print("Large-box pusher: EXTENDED")
            print("Large box sorted successfully.")

            self.large_boxes += 1

            # Retract pusher
            self.outputs.large_box_pusher = False

            self.outputs.conveyor_motor = True

            print("Large-box pusher: RETRACTED")
            print("Conveyor motor: ON")

        elif self.current_box == "UNKNOWN":

            print()
            print("SORTING ACTION")
            print("Unknown box detected.")
            print("Box sent to reject/inspection area.")

            self.rejected_boxes += 1

        self.current_box = None

    # --------------------------------------------------------
    # PROCESS ONE BOX
    # --------------------------------------------------------

    def process_box(self, box_type):

        if not self.system_running:

            print()
            print("Cannot process box.")
            print("Conveyor system is not running.")

            return

        # Reset sensors
        self.inputs.box_sensor = False
        self.inputs.small_box_sensor = False
        self.inputs.large_box_sensor = False

        # Box enters detection zone
        self.inputs.box_sensor = True

        if box_type == "SMALL":

            self.inputs.small_box_sensor = True

        elif box_type == "LARGE":

            self.inputs.large_box_sensor = True

        self.detect_box()

        self.sort_box()

        # Reset box sensor
        self.inputs.box_sensor = False

    # --------------------------------------------------------
    # EMERGENCY STOP TEST
    # --------------------------------------------------------

    def test_emergency_stop(self):

        print()
        print("SAFETY TEST")
        print("------------------------------")

        self.inputs.emergency_stop = True

        self.safety_interlock()

        if not self.outputs.conveyor_motor:

            print("E-STOP TEST: PASSED")
            print("Motor was immediately switched OFF.")

        else:

            print("E-STOP TEST: FAILED")

        # Reset emergency stop
        self.inputs.emergency_stop = False

        print()
        print("Emergency stop reset.")

    # --------------------------------------------------------
    # SYSTEM STATUS
    # --------------------------------------------------------

    def show_status(self):

        print()
        print("SYSTEM STATUS")
        print("------------------------------")

        print(
            "Conveyor Motor:",
            "ON" if self.outputs.conveyor_motor else "OFF"
        )

        print(
            "Small Pusher:",
            "ON" if self.outputs.small_box_pusher else "OFF"
        )

        print(
            "Large Pusher:",
            "ON" if self.outputs.large_box_pusher else "OFF"
        )

        print(
            "Green Indicator:",
            "ON" if self.outputs.green_indicator else "OFF"
        )

        print(
            "Red Safety Indicator:",
            "ON" if self.outputs.red_indicator else "OFF"
        )

    # --------------------------------------------------------
    # PRODUCTION SUMMARY
    # --------------------------------------------------------

    def show_summary(self):

        print()
        print("=" * 50)
        print("PRODUCTION SUMMARY")
        print("=" * 50)

        print(
            "Total boxes processed:",
            self.total_boxes
        )

        print(
            "Small boxes sorted:",
            self.small_boxes
        )

        print(
            "Large boxes sorted:",
            self.large_boxes
        )

        print(
            "Rejected/unknown boxes:",
            self.rejected_boxes
        )


# ------------------------------------------------------------
# MAIN PLC SIMULATION
# ------------------------------------------------------------

def main():

    print("=" * 60)
    print("DECODELABS PROJECT 4")
    print("PLC-BASED CONVEYOR SORTING SYSTEM")
    print("=" * 60)

    plc = ConveyorPLC()

    # --------------------------------------------------------
    # INPUT / OUTPUT MAPPING
    # --------------------------------------------------------

    print()
    print("DIGITAL INPUT MAPPING")
    print("------------------------------")

    print("I0.0 = Start Push Button")
    print("I0.1 = Stop Push Button")
    print("I0.2 = Emergency Stop")
    print("I0.3 = Box Detection Sensor")
    print("I0.4 = Small Box Sensor")
    print("I0.5 = Large Box Sensor")

    print()
    print("DIGITAL OUTPUT MAPPING")
    print("------------------------------")

    print("Q0.0 = Conveyor Motor")
    print("Q0.1 = Small Box Pneumatic Pusher")
    print("Q0.2 = Large Box Pneumatic Pusher")
    print("Q0.3 = Green Running Indicator")
    print("Q0.4 = Red Safety Indicator")

    # --------------------------------------------------------
    # START
    # --------------------------------------------------------

    print()
    print("STEP 1: STARTING CONVEYOR")

    plc.inputs.start_button = True

    plc.start_system()

    plc.inputs.start_button = False

    plc.show_status()

    # --------------------------------------------------------
    # PROCESS SMALL BOX
    # --------------------------------------------------------

    print()
    print("STEP 2: SMALL BOX SORTING")

    plc.process_box("SMALL")

    # --------------------------------------------------------
    # PROCESS LARGE BOX
    # --------------------------------------------------------

    print()
    print("STEP 3: LARGE BOX SORTING")

    plc.process_box("LARGE")

    # --------------------------------------------------------
    # PROCESS SECOND SMALL BOX
    # --------------------------------------------------------

    print()
    print("STEP 4: SECOND SMALL BOX")

    plc.process_box("SMALL")

    # --------------------------------------------------------
    # SAFETY TEST
    # --------------------------------------------------------

    print()
    print("STEP 5: EMERGENCY STOP SAFETY TEST")

    plc.test_emergency_stop()

    plc.show_status()

    # --------------------------------------------------------
    # FINAL STATUS
    # --------------------------------------------------------

    print()
    print("STEP 6: FINAL SYSTEM RESULT")

    plc.show_summary()

    print()
    print("=" * 60)
    print("PLC CONVEYOR SORTING SIMULATION COMPLETED")
    print("=" * 60)


# ------------------------------------------------------------
# PROGRAM START
# ------------------------------------------------------------

if __name__ == "__main__":

    main()