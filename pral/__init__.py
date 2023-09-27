#!/usr/bin/env python
import os
import subprocess as sp
from dataclasses import asdict, dataclass, fields
from typing import Union

import numpy as np


class ParameterRangeException(Exception):
    def __init__(
        self,
        name: str,
        value: Union[float, int],
        limit: Union[tuple[int, int], tuple[float, float]],
    ):
        self.name = name
        self.value = value
        self.limit = limit

    def __str__(self):
        return f"{self.name} parameter {self.value} out of range {self.limit}"


@dataclass(frozen=True)
class _InputParamRange:
    N_diblock: tuple[int, int] = (32, 256)
    f_diblock: tuple[float, float] = (0.05, 0.55)
    N_homo: tuple[int, int] = (4, 256)
    chi_AB: tuple[float, float] = (0, 128)
    chi_AC: tuple[float, float] = (0, 128)
    chi_BC: tuple[float, float] = (0, 128)
    kappa: tuple[float, float] = (40, 256)
    homo_concentration: tuple[float, float] = (0.0, 0.5)
    external_field_A: tuple[float, float] = (-10.0, 10)
    external_field_B: tuple[float, float] = (-10.0, 10.0)
    external_field_C: tuple[float, float] = (-10.0, 10.0)


@dataclass
class InputParam:
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
        self_dict = asdict(self)
        return np.asarray(list(self_dict.values()))

    @staticmethod
    def from_numpy(numpy_array):
        instance = InputParam()
        assert len(asdict(instance)) == len(numpy_array)
        return InputParam(*numpy_array)

    def __post_init__(self):
        validator = _InputParamRange()
        for field in fields(self):
            limit = getattr(validator, field.name)
            value = getattr(self, field.name)
            if value < limit[0]:
                raise ParameterRangeException(field.name, value, limit)
            if value > limit[1]:
                raise ParameterRangeException(field.name, value, limit)


class SystemParamter:
    @dataclass
    class _InternalSystemParam:
        name: str
        n_homo: int
        n_diblock: int
        NA: int
        NB: int
        L: list[float]
        NL: list[int]
        nN_beads: int

    _system_param: _InternalSystemParam
    _param: InputParam

    def __init__(self, name: str, parameters: InputParam, nN_beads: int = 190320):
        _acceptable_size_names = ("small", "medium", "large")
        if name not in _acceptable_size_names:
            raise RuntimeError("Systems have to of size {_acceptable_size_names} but got {name}")
        self._param = parameters

        nN_homo_beads = nN_beads * self.homo_concentration
        n_homo = int(nN_homo_beads / self.N_homo)
        nN_diblock_beads = nN_beads - n_homo * self.N_homo
        n_diblock = int(nN_diblock_beads / self.N_diblock)
        NA = int(self.f_diblock * self.N_diblock)
        NB = int(self.N_diblock - NA)

        DL = 1 / 7.0
        volume = 5.0
        if name == "small":
            L = np.asarray([volume / (1 + 2 * DL), 1 + 2 * DL, 1.0])
            NL = (np.asarray(L) / DL).astype(int)
        if name == "medium":
            L = np.asarray([volume / (1 + DL), 1 + DL, 1.0])
            NL = (np.asarray(L) / DL).astype(int)
        if name == "large":
            L = np.asarray([volume, 1, 1.0])
            NL = (np.asarray(L) / DL).astype(int)
        # Add for area 51
        NL[0] += 1
        self._system_param = SystemParamter._InternalSystemParam(
            name=name,
            n_homo=n_homo,
            n_diblock=n_diblock,
            NA=NA,
            NB=NB,
            L=L,
            NL=NL,
            nN_beads=nN_beads,
        )

    def __getattr__(self, key):
        if key not in ("_system_param", "_param"):
            try:
                return getattr(self._system_param, key)
            except AttributeError:
                return getattr(self._param, key)
        self.__getattribute__(key)

    def get_soma_xml_str(self):
        xml_string = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        xml_string += '<soma version="0.2.0">\n'
        xml_string += "  <interactions>\n"
        xml_string += "    <kappaN>\n"
        xml_string += f"      {self.kappa}\n"
        xml_string += "    </kappaN>\n"
        xml_string += "    <chiN>\n"
        xml_string += f"      A B {self.chi_AB}\n"
        xml_string += f"      A C {self.chi_AC}\n"
        xml_string += f"      B C {self.chi_BC}\n"
        xml_string += "    </chiN>\n"
        xml_string += "    <bonds>\n"
        xml_string += "    A A  harmonic\n"
        xml_string += "    A B  harmonic\n"
        xml_string += "    A C  harmonic\n"
        xml_string += "\n"
        xml_string += "    B B  harmonic\n"
        xml_string += "    B C  harmonic\n"
        xml_string += "\n"
        xml_string += "    C C harmonic\n"
        xml_string += "    </bonds>\n"
        xml_string += "  </interactions>\n"
        xml_string += "  <A>\n"
        xml_string += "    <dt>\n"
        xml_string += "    0.17\n"
        xml_string += "    </dt>\n"
        xml_string += "  </A>\n"
        xml_string += "  <time>\n"
        xml_string += "    0\n"
        xml_string += "  </time>\n"
        xml_string += "    <reference_Nbeads>\n"
        xml_string += "    64\n"
        xml_string += "  </reference_Nbeads>\n"
        xml_string += "  <lxyz>\n"
        xml_string += f"    {self.L[0]} {self.L[1]} {self.L[2]}\n"
        xml_string += "  </lxyz>\n"
        xml_string += "  <nxyz>\n"
        xml_string += f"    {self.NL[0]} {self.NL[1]} {self.NL[2]}\n"
        xml_string += "  </nxyz>\n"
        xml_string += "  <poly_arch>\n"
        xml_string += f"    {self.n_diblock} " + "A{" + str(self.NA) + "}B{" + str(self.NB) + "}\n"
        xml_string += f"    {self.n_homo} " + "C{" + str(self.N_homo) + "}\n"
        xml_string += "  </poly_arch>\n"
        xml_string += "  <analysis>\n"
        xml_string += "    <Re>\n"
        xml_string += "      <DeltaMC> 500 </DeltaMC>\n"
        xml_string += "    </Re>\n"
        xml_string += "    <Rg>\n"
        xml_string += "      <DeltaMC> 500 </DeltaMC>\n"
        xml_string += "    </Rg>\n"
        xml_string += "    <density_var>\n"
        xml_string += "      <DeltaMC> 500 </DeltaMC>\n"
        xml_string += "    </density_var>\n"
        xml_string += "    <bond_anisotropy>\n"
        xml_string += "      <DeltaMC> 500 </DeltaMC>\n"
        xml_string += "    </bond_anisotropy>\n"
        xml_string += "    <acc_ratio>\n"
        xml_string += "      <DeltaMC> 500 </DeltaMC>\n"
        xml_string += "    </acc_ratio>\n"
        xml_string += "    <MSD>\n"
        xml_string += "      <DeltaMC> 500 </DeltaMC>\n"
        xml_string += "    </MSD>\n"
        xml_string += "    <density_field>\n"
        xml_string += "      <DeltaMC> 5000 </DeltaMC>\n"
        xml_string += "      <compression> gzip </compression>\n"
        xml_string += "    </density_field>\n"
        xml_string += "    <non_bonded_energy>\n"
        xml_string += "      <DeltaMC> 5000</DeltaMC>\n"
        xml_string += "    </non_bonded_energy>\n"
        xml_string += "    <bonded_energy>\n"
        xml_string += "      <DeltaMC> 5000</DeltaMC>\n"
        xml_string += "    </bonded_energy>\n"
        xml_string += "  </analysis>\n"
        xml_string += "  <area51>\n"
        xml_string += "    <box>\n"
        xml_string += f"      <point>0 0 0</point><point>{self.NL[0]} {self.NL[1]} 1</point><value>1</value>\n"
        xml_string += "    </box>\n"
        xml_string += "  </area51>\n"
        xml_string += "  <external_field>\n"
        xml_string += "    <box>\n"
        xml_string += f"      <point>0 0 -1</point><point>{self.NL[0]-1} {self.NL[1]-1} 2</point>"
        xml_string += f"<value>{self.external_field_A} {self.external_field_B} {self.external_field_C}</value>\n"
        xml_string += "    </box>\n"
        xml_string += "  </external_field>\n"
        xml_string += "</soma>\n"

        return xml_string

    def write_soma_xml(self):
        with open(f"{self.name}.xml", "w") as file_handle:
            file_handle.write(self.get_soma_xml_str())


def run_param(param):
    os.mkdir("00_tmp_running")
    os.chdir("00_tmp_running")

    for name in ("small", "medium", "large"):
        system = SystemParamter(name, param)
        system.write_soma_xml()
        sp.call(["../ConfGen.py", "-i", f"{name}.xml"])
        sp.call(["../SOMA", "-c", f"{name}.h5", "-o", "0", "-t", "100000", "-f", f"{name}_end.h5"])
        sp.call(
            [
                "../SOMA",
                "-c",
                f"{name}_end.h5",
                "-a",
                f"{name}_ana.h5",
                "-o",
                "0",
                "-t",
                "100000",
                "-f",
                f"{name}_end.h5",
            ]
        )

    os.chdir("..")
    os.rename("00_tmp_running", f"{param}")
