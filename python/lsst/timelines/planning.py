from .activities import *

CCS = "red"
INRIA = "magenta"
TS = "cyan"


def makeActivities(includeMilestones=False):
    """Return a set of Activities, suitable for show_activities

    parameters:
    includeMilestones: `bool`
       Include IMs and related activities

    Return:
       list of lists of `Activities`
    """

    activities = []

    if includeMilestones:
        activities += [
            [
                Color("red"),
                MarkerWidth(1),

                Milestone("IM_1", "2021-04-01", color='red'),
                Milestone("IM_b", "2021-04-30", color='green', align='left'),
                Milestone("IM_c", "2021-03-31", color='green', align='left', valign='bottom'),
                Milestone("IM_d", "2021-05-31"),
                #Milestone("IM_e", "2021-05-31"),
                Milestone("IM_f", "2021-04-15"),
                Milestone("IM_pg", "2021-04-15", valign='bottom'),
                Milestone("IM_g", "2021-07-31"),
                Milestone("IM_h", "2021-09-30"),
            ],
            [
                Color("blue"),
                LengthArrow(5),

                Functionality("ScriptQueue", "2021-03-01"),

                Milestone("OCPS@NTS", "2021-03-26", align="right", valign="bottom"),
                Functionality("OCPS", "2021-04-01"),

                Milestone("Gen3@NTS", "2021-03-29", align="left", valign="top"),
                Functionality("Gen3@CP", "2021-04-05", dy=0.1),

                AdvanceRow(1),

                Color(TS),
                Functionality("M1M2M3", "2021-03-31"),
                Functionality("Slew TMA", "2021-10-01"),

                Color(CCS),
                Functionality("Trending DB in EFD", "2021-03-22"),

                Color(INRIA),
                Functionality("LOVE", "2021-04-01", valign="bottom", dy=-0.1),
                Functionality("AuthList", "2021-05-15"),
                Functionality("Logging@CP", "2021-06-15"),
            ], [
                Activity("ComCam Cold", "2021-03-26", "2021-05-31", color=CCS),
            ],
        ]

    activities += [
        [
            Color("black"),
            MarkerWidth(3),

            Milestone("NEED: Dome Weather Tight", "2021-10-01"),
            Milestone("TMA Contract Complete", "2022-02-07"),
        ],
        [
            Color("yellow"),
            Activity("Bridge Crane Installation", "2021-03-10", 35),
            Activity("Dome Weather Tight",        "2021-09-03", "2021-09-25"),
            Activity("Integrating Structure Installation?", "2021-09-25", "2021-10-20"),
        ], [
            Color("blue"),
            Activity("Installation of M2 hexapod with the TEA on the TMA", "2021-03-01", "2021-04-01"),
            Activity("Refrigeration lines in coordination with the TMA stubs", "2021-04-02", "2021-05-05"),
            Activity("Refrigeration lines flushing", "2021-05-05", "2021-07-10"),

            Color("red"),
            Activity("Install M1M3 w/surrogate on TMA", "2022-02-08", "2022-03-07"),
            Activity("Dynamic M1M3 w/surrogate testing on TMA", "2022-03-08", "2022-04-20"),

            Color("green"),
            Activity("M2 w/surrogate + baffle fit check", "2022-04-21", "2022-05-10"),
            Activity("M2 Glass on Cell", "2022-05-11", "2022-05-31"),
            Activity("M2 on TMA", "2022-05-31", "2022-06-20"),

            AdvanceRow(1),
            Activity("Top End utilities install: (Liq, Air, Power, Fiber, Signal, Refrig, IT infrastructure)",
                "2021-04-01", "2021-07-10"),
            Activity("Cabinet utilities (Power, Data, Liq)", "2021-07-15", "2021-08-10"),
            Activity("Refriger. Cabinet (1 week)", "2021-08-11", 3*7),
            Activity("M2 SW Update and func test", "2021-03-10", "2021-03-31", color="green"),
        ], [
            Color("white", border="green"),
            Activity("AOS integration testing without "
                     "ComCam Including I&T with the rest of the control  network and Ptg, TMA, ...", 
                     "2021-04-01", "2021-06-30"),
            Color("red"),
            Activity("M1M3 SW Update and Func tests", "2021-03-01", "2021-03-31"),
            Activity("M1M3 coating preparation?", "2021-11-10", 30),
            Milestone("Start M2 fit check", "2022-04-20", align="left", valign="bottom"),
            Milestone("TMA Ready for M1M3 Glass", "2022-06-21", align="left"),
            Activity("M1M3 Surrogate to Mirror on Cell", "2022-06-21", "2022-07-31"),
            Activity("M1M3 Glass Coating", "2022-08-01", "2022-08-15", color="orange"),
            Activity("M1M3 Mirror on TMA & thermal control tests", "2022-08-16", "2022-12-31"),

            AdvanceRow(-1),
            Color("violet", border=None),
            Activity("M3 Testing", "2022-08-16", "2022-09-06"),
            Activity("Initial Optical Alignment", "2022-09-07", "2022-09-30"),
            Activity("Active Optics Calibration & Verification", "2022-09-30", "2022-12-31"),
            AdvanceRow(1),
         ], [
            Color("blue"),
            Activity("Cam Hexapod  re-verification", "2021-03-01", "2021-04-30"),
            Color("white", border="green"),
            Activity("Active Optics Software integration testing with ComCam (Level 3)", "2021-06-01", "2021-09-30"),
            Activity("Continued Active Optics Software integration testing without ComCam (Level-3)", 
                     "2021-10-01", "2022-01-10"),
       ], [
            Color("red"),
            Activity("M1M3 thermal control system installation and test", "2021-03-01", "2022-01-10"),
            Milestone("Ready for integrated optical tests", "2022-09-15", align="left"),
            Milestone("Engineering First Light", "2022-11-01", align="right"),
        ], [
            Color("white", border="green"),
            Activity("Final prep for Camera Hexapod,  rotator and CCW", "2021-03-01", "2021-03-15"),
            Activity("Early ComCam, Pathfinder, Rotator, Hexapod and CCW Integration testing (Summit Level 3)",
                     "2021-04-01", "2021-09-30"),

            Activity("ComCam, Rotator, Hexapod and CCW On TMA  (Not on sky)",
                     "2021-10-10", "2022-04-10"),
            Activity("ComCam testing (Not on sky)",
                     "2022-06-01", "2022-09-20"),
            Activity("ComCam testing (on sky)",
                     "2022-09-21", "2022-12-31"),

            AdvanceRow(1),
            Activity("Refrigeration Pathfinder (in ComCam) Operation through CCW (Summit Level 3)",
                     "2021-04-01", "2021-09-30"),
            Activity("Refrigeration Pathfinder (In ComCam) Operation on TMA",
                     "2021-10-10", "2022-04-10"),
            Activity("Refrigeration Pathfinder long term performance",
                     "2022-05-15", "2022-12-31"),
            Color("white", border="magenta"),
            Activity("Install ComCam & Pathfinder on Rotator", "2021-03-15", "2021-03-31"),
            Activity("ComCam installation on the TMA for CCW testing", "2021-10-01", "2021-10-10"),
        ], [
            Color("white", border="green"),
            Activity("Testing CCW, Rotator and  Hex", "2021-03-01", "2021-04-10"),
            Activity("GIS integration and testing on level 3", "2021-04-10", "2021-08-30"),
            Activity("GIS verification testing", "2021-09-01", "2021-12-10"),
            Activity("In-Dome Calibration Systems installation and alignment ", "2022-01-01", "2022-08-15",
                     color="orchid"),
        ], [
            Color("seagreen", border=None),
            Activity("Environmental Awareness System (EAS) @ AuxTel", "2021-03-01", "2021-10-30"),       
            Activity("Environmental Awareness System (EAS) @ MT", "2021-11-01", "2022-10-10"),       
        ], [
            Color("yellow", border="black"),
            Activity("LSSTCam shipping. received in Chile, Assembly & Re-verification", "2022-06-01", "2022-12-31"),   
        ], [
            Milestone("LSSTCam Ready at SLAC 31-May-2022", "2022-06-01", align="left"),
            Milestone("LSSTCam arrives in Chile", "2022-07-01"),
            Milestone("LSSTCam Integration", "2023-01-23", align="left"),
        ], [
            Color("goldenrod"),
            Activity("AT: On sky Testing / Observations with Spectrograph", "2021-03-01", "2022-12-31"),       
        ],
    ]
    
    return activities
    
