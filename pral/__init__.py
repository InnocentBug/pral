#!/usr/bin/env python
from dataclasses import asdict, dataclass

import numpy as np


@dataclass(frozen=True)
class _InputParam:
    N_diblock: int = 64
    f_diblock: float = 8 / 64
    N_homo: int = 6
    chi_AB: float = 40.0
    chi_AC: float = 2.0
    chi_BC: float = 30.0
    kappa: float = 50.0
    homo_concentration: float = 0.02
    external_field_A: float = -1.0
    external_field_B: float = 0
    external_field_C: float = 1.0

    def to_numpy(self):
        asdict(self)
        return np.asdict(self.values())


#     @staticmethod
#     def from_numpy(numpy_array):
#         assert


#     def __init__(name:str, N_diblock
#     nN_beads:int=190320


# def write_xml(name, Npoly=64, f=8/64, Nhomo=6, Nbeads=190320, homo_conc=0.02, chiAB=40, chi):
#     assert name in ["small", "medium", "large"]


#     Nhomo_beads = Nbeads*concentration
#     n_homo = int(Nhomo_beads/Nhomo)

#     Npoly_beads = Nbeads - n_homo*Nhomo
#     n_poly = int(Npoly_beads/Npoly)
#     NA = int(f*Npoly)
#     NB = int((1-f)*Npoly)

#     xml_string = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n"
#     xml_string += "<soma version=\"0.2.0\">\n"
#     xml_string += "  <interactions>\n"
#     xml_string += "    <kappaN>\n"
#     xml_string += "      40\n"
#     xml_string += "    </kappaN>\n"
#     xml_string += "    <chiN>\n"
#     xml_string += "      A B 40\n"
#     xml_string += "      A C 2\n"
#     xml_string += "      B C 30\n"
#     xml_string += "    </chiN>\n"
#     xml_string += "    <bonds>\n"
#     xml_string += "    A A  harmonic\n"
#     xml_string += "    A B  harmonic\n"
#     xml_string += "    A C  harmonic\n"
#     xml_string += "\n"
#     xml_string += "    B B  harmonic\n"
#     xml_string += "    B C  harmonic\n"
#     xml_string += "\n"
#     xml_string += "    C C harmonic\n"
#     xml_string += "    </bonds>\n"
#     xml_string += "  </interactions>\n"
#     xml_string += "  <A>\n"
#     xml_string += "    <dt>\n"
#     xml_string += "    0.17\n"
#     xml_string += "    </dt>\n"
#     xml_string += "  </A>\n"
#     xml_string += "  <time>\n"
#     xml_string += "    0\n"
#     xml_string += "  </time>\n"
#     xml_string += "    <reference_Nbeads>\n"
#     xml_string += f"    {Npoly}\n"
#     xml_string += "  </reference_Nbeads>\n"
#     xml_string += "  <lxyz>\n"
#     xml_string += "    5 1 1\n"
#     xml_string += "  </lxyz>\n"
#     xml_string += "  <nxyz>\n"
#     xml_string += "    27 6 7\n"
#     xml_string += "  </nxyz>\n"
#     xml_string += "  <poly_arch>\n"
#     xml_string += f"    {n_poly} "+"A{"+str(NA)+"}B{"+str(NB)+"}\n"
#     xml_string += f"    {n_homo} "+"C{"+str(Nhomo)+"}\n"
#     xml_string += "  </poly_arch>\n"
#     xml_string += "  <analysis>\n"
#     xml_string += "    <Re>\n"
#     xml_string += "      <DeltaMC> 500 </DeltaMC>\n"
#     xml_string += "    </Re>\n"
#     xml_string += "    <Rg>\n"
#     xml_string += "      <DeltaMC> 500 </DeltaMC>\n"
#     xml_string += "    </Rg>\n"
#     xml_string += "    <density_var>\n"
#     xml_string += "      <DeltaMC> 500 </DeltaMC>\n"
#     xml_string += "    </density_var>\n"
#     xml_string += "    <bond_anisotropy>\n"
#     xml_string += "      <DeltaMC> 500 </DeltaMC>\n"
#     xml_string += "    </bond_anisotropy>\n"
#     xml_string += "    <acc_ratio>\n"
#     xml_string += "      <DeltaMC> 500 </DeltaMC>\n"
#     xml_string += "    </acc_ratio>\n"
#     xml_string += "    <MSD>\n"
#     xml_string += "      <DeltaMC> 500 </DeltaMC>\n"
#     xml_string += "    </MSD>\n"
#     xml_string += "    <density_field>\n"
#     xml_string += "      <DeltaMC> 5000 </DeltaMC>\n"
#     xml_string += "      <compression> gzip </compression>\n"
#     xml_string += "    </density_field>\n"
#     xml_string += "    <non_bonded_energy>\n"
#     xml_string += "      <DeltaMC> 5000</DeltaMC>\n"
#     xml_string += "    </non_bonded_energy>\n"
#     xml_string += "    <bonded_energy>\n"
#     xml_string += "      <DeltaMC> 5000</DeltaMC>\n"
#     xml_string += "    </bonded_energy>\n"
#     xml_string += "  </analysis>\n"
#     xml_string += "  <area51>\n"
#     xml_string += "    <box>\n"
#     xml_string += "      <point>0 0 0</point><point>27 6 1</point><value>1</value>\n"
#     xml_string += "    </box>\n"
#     xml_string += "  </area51>\n"
#     xml_string += "  <external_field>\n"
#     xml_string += "    <box>\n"
#     xml_string += "      <point>0 0 -1</point><point>26 5 2</point><value>-1 0 1 </value>\n"
#     xml_string += "    </box>\n"
#     xml_string += "  </external_field>\n"
#     xml_string += "</soma>\n"


#     with open("coord.xml", "w") as file_handle:
#         file_handle.write(xml_string)


# def run_dir(concentration):
#     os.mkdir(f"conc{concentration}")
#     os.chdir(f"conc{concentration}")

#     write_xml(concentration)
#     sp.call(["../ConfGen.py", "-i", "coord.xml"])
#     sp.call(["../SOMA", "-c", "coord.h5", "-a", "coord_ana.h5", "-o", "0", "-t", "100000"])

#     os.chdir("..")

# def main(argv):
#     if len(argv) != 0:
#         print("./script.py")
#         return

#     conc_list = [0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.2]
#     for conc in conc_list:
#         run_dir(conc)

# if __name__ == "__main__":
#     main(sys.argv[1:])
