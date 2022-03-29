from dataclasses import dataclass, asdict, field

from . import business2018, lulucf2018
from .inputs import Inputs
from .utils import div


@dataclass
class CO2eEmissions:
    # Used by a, p_fermen, p_manure, p_soil, p_other, p_other_liming
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore

    @classmethod
    def sum(cls, *co2es: "CO2eEmissions") -> "CO2eEmissions":
        return cls(
            CO2e_combustion_based=sum(c.CO2e_combustion_based for c in co2es),
            CO2e_production_based=sum(c.CO2e_production_based for c in co2es),
            CO2e_total=sum(c.CO2e_total for c in co2es),
        )


@dataclass
class Vars1:
    # Used by p
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    energy: float = None  # type: ignore


@dataclass
class Vars2:
    # Used by g
    CO2e_total: float = None  # type: ignore


@dataclass
class CO2eFromFermentationOrManure(CO2eEmissions):
    # Used by p_fermen_dairycow, p_fermen_nondairy, p_fermen_swine, p_fermen_poultry, p_fermen_oanimal, p_manure_dairycow, p_manure_nondairy, p_manure_swine, p_manure_poultry, p_manure_oanimal, p_manure_deposition
    CO2e_production_based_per_t: float = None  # type: ignore
    amount: float = None  # type: ignore -- in tons of manure ...

    @classmethod
    def calc_fermen(
        cls, inputs: Inputs, what: str, *, alias: str | None = None
    ) -> "CO2eFromFermentationOrManure":
        CO2e_combustion_based = 0.0
        # This line and the next might just be a little too cute.
        # They make the callsite nice and short, but forego any type checking
        # I'll keep it like this for now, but this is one of the places where
        # a better overall design is probably lurking somewhere
        CO2e_production_based_per_t = inputs.fact(
            "Fact_A_P_fermen_" + what + "_ratio_CO2e_to_amount_2018"
        )
        # Also don't ask me why we called swine except when we called them pig
        amount = getattr(
            inputs.entries, "a_fermen_" + (what if alias is None else alias) + "_amount"
        )
        CO2e_production_based = amount * CO2e_production_based_per_t
        CO2e_total = CO2e_production_based + CO2e_combustion_based
        return cls(
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_t=CO2e_production_based_per_t,
            CO2e_total=CO2e_total,
            amount=amount,
        )

    @classmethod
    def calc_manure(
        cls, inputs: Inputs, what: str, *, amount: float
    ) -> "CO2eFromFermentationOrManure":
        CO2e_combustion_based = 0.0
        CO2e_production_based_per_t = getattr(
            inputs.entries, "a_manure_" + what + "_ratio_CO2e_to_amount"
        )
        CO2e_production_based = amount * CO2e_production_based_per_t
        CO2e_total = CO2e_production_based + CO2e_combustion_based
        return cls(
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_t=CO2e_production_based_per_t,
            CO2e_total=CO2e_total,
            amount=amount,
        )

    @classmethod
    def calc_deposition(
        cls,
        inputs: Inputs,
        *,
        p_fermen_dairycow: "CO2eFromFermentationOrManure",
        p_fermen_nondairy: "CO2eFromFermentationOrManure",
        p_fermen_swine: "CO2eFromFermentationOrManure",
        p_fermen_oanimal: "CO2eFromFermentationOrManure",
    ) -> "CO2eFromFermentationOrManure":
        """This computes the deposition of reactive nitrogen of animals (excluding poultry)"""

        CO2e_combustion_based = 0.0
        CO2e_production_based_per_t = (
            inputs.entries.a_manure_deposition_ratio_CO2e_to_amount
        )
        amount = (
            p_fermen_dairycow.amount
            + p_fermen_nondairy.amount
            + p_fermen_swine.amount
            + p_fermen_oanimal.amount
        )
        CO2e_production_based = amount * CO2e_production_based_per_t
        CO2e_total = CO2e_production_based + CO2e_combustion_based
        return cls(
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_t=CO2e_production_based_per_t,
            CO2e_total=CO2e_total,
            amount=amount,
        )


@dataclass
class CO2eFromSoil(CO2eEmissions):
    # Used by p_soil_fertilizer, p_soil_manure, p_soil_sludge, p_soil_ecrop, p_soil_grazing, p_soil_residue, p_soil_orgfarm, p_soil_orgloss, p_soil_leaching, p_soil_deposition
    CO2e_production_based_per_t: float = None  # type: ignore
    area_ha: float = None  # type: ignore

    @classmethod
    def calc(cls, ratio_CO2e_to_ha: float, area_ha: float) -> "CO2eFromSoil":
        CO2e_combustion_based = 0.0
        # Huh? This line looks really odd.  Is that a we combined multiple different variables in the same spreadsheet column
        # modelling oddity?
        CO2e_production_based_per_t = ratio_CO2e_to_ha
        CO2e_production_based = area_ha * CO2e_production_based_per_t
        CO2e_total = CO2e_production_based + CO2e_combustion_based
        return cls(
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_t=CO2e_production_based_per_t,
            CO2e_total=CO2e_total,
            area_ha=area_ha,
        )


@dataclass
class CO2eFromOther(CO2eEmissions):
    # Used by p_other_liming_dolomite, p_other_urea, p_other_ecrop, p_other_liming_calcit
    CO2e_production_based_per_t: float = None  # type: ignore
    prod_volume: float = None  # type: ignore -- in tons

    @classmethod
    def calc(
        cls, inputs: Inputs, what: str, *, ratio_suffix="_ratio"
    ) -> "CO2eFromOther":
        # No idea why we use ratio_ with
        #   Fact_A_P_other_liming_calcit_ratio_CO2e_pb_to_amount_2018
        # but not with
        #   Fact_A_P_other_urea_CO2e_pb_to_amount_2018
        CO2e_combustion_based = 0.0
        CO2e_production_based_per_t = inputs.fact(
            "Fact_A_P_other_" + what + ratio_suffix + "_CO2e_pb_to_amount_2018"
        )
        prod_volume = getattr(inputs.entries, "a_other_" + what + "_prod_volume")
        CO2e_production_based = prod_volume * CO2e_production_based_per_t
        CO2e_total = CO2e_production_based
        return cls(
            CO2e_combustion_based=CO2e_combustion_based,
            CO2e_production_based=CO2e_production_based,
            CO2e_production_based_per_t=CO2e_production_based_per_t,
            CO2e_total=CO2e_total,
            prod_volume=prod_volume,
        )


@dataclass
class Vars7:
    # Used by p_other_kas
    CO2e_production_based: float = None  # type: ignore
    CO2e_production_based_per_t: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    prod_volume: float = None  # type: ignore


@dataclass
class Vars8:
    # Used by p_operation, p_operation_elec_heatpump
    energy: float = None  # type: ignore


@dataclass
class Vars9:
    # Used by p_operation_heat
    area_m2: float = None  # type: ignore
    energy: float = None  # type: ignore
    factor_adapted_to_fec: float = None  # type: ignore
    pct_energy: float = None  # type: ignore


@dataclass
class Vars10:
    # Used by p_operation_elec_elcon, p_operation_vehicles
    energy: float = None  # type: ignore
    pct_energy: float = None  # type: ignore


@dataclass
class Vars11:
    # Used by s
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    energy: float = None  # type: ignore
    pct_energy: float = None  # type: ignore


@dataclass
class Vars12:
    # Used by s_petrol, s_diesel, s_fueloil, s_lpg, s_gas, s_biomass, s_elec, s_heatpump
    CO2e_combustion_based: float = None  # type: ignore
    CO2e_combustion_based_per_MWh: float = None  # type: ignore
    CO2e_production_based: float = None  # type: ignore
    CO2e_total: float = None  # type: ignore
    energy: float = None  # type: ignore
    pct_energy: float = None  # type: ignore


@dataclass
class A18:
    a: CO2eEmissions = field(default_factory=CO2eEmissions)
    p: Vars1 = field(default_factory=Vars1)
    g: Vars2 = field(default_factory=Vars2)
    p_fermen: CO2eEmissions = field(default_factory=CO2eEmissions)
    p_fermen_dairycow: CO2eFromFermentationOrManure = field(
        default_factory=CO2eFromFermentationOrManure
    )
    p_fermen_nondairy: CO2eFromFermentationOrManure = field(
        default_factory=CO2eFromFermentationOrManure
    )
    p_fermen_swine: CO2eFromFermentationOrManure = field(
        default_factory=CO2eFromFermentationOrManure
    )
    p_fermen_poultry: CO2eFromFermentationOrManure = field(
        default_factory=CO2eFromFermentationOrManure
    )
    p_fermen_oanimal: CO2eFromFermentationOrManure = field(
        default_factory=CO2eFromFermentationOrManure
    )
    p_manure: CO2eEmissions = field(default_factory=CO2eEmissions)
    p_manure_dairycow: CO2eFromFermentationOrManure = field(
        default_factory=CO2eFromFermentationOrManure
    )
    p_manure_nondairy: CO2eFromFermentationOrManure = field(
        default_factory=CO2eFromFermentationOrManure
    )
    p_manure_swine: CO2eFromFermentationOrManure = field(
        default_factory=CO2eFromFermentationOrManure
    )
    p_manure_poultry: CO2eFromFermentationOrManure = field(
        default_factory=CO2eFromFermentationOrManure
    )
    p_manure_oanimal: CO2eFromFermentationOrManure = field(
        default_factory=CO2eFromFermentationOrManure
    )
    p_manure_deposition: CO2eFromFermentationOrManure = field(
        default_factory=CO2eFromFermentationOrManure
    )
    p_soil: CO2eEmissions = field(default_factory=CO2eEmissions)
    p_soil_fertilizer: CO2eFromSoil = field(default_factory=CO2eFromSoil)
    p_soil_manure: CO2eFromSoil = field(default_factory=CO2eFromSoil)
    p_soil_sludge: CO2eFromSoil = field(default_factory=CO2eFromSoil)
    p_soil_ecrop: CO2eFromSoil = field(default_factory=CO2eFromSoil)
    p_soil_grazing: CO2eFromSoil = field(default_factory=CO2eFromSoil)
    p_soil_residue: CO2eFromSoil = field(default_factory=CO2eFromSoil)
    p_soil_orgfarm: CO2eFromSoil = field(default_factory=CO2eFromSoil)
    p_soil_orgloss: CO2eFromSoil = field(default_factory=CO2eFromSoil)
    p_soil_leaching: CO2eFromSoil = field(default_factory=CO2eFromSoil)
    p_soil_deposition: CO2eFromSoil = field(default_factory=CO2eFromSoil)
    p_other: CO2eEmissions = field(default_factory=CO2eEmissions)
    p_other_liming_dolomite: CO2eFromOther = field(default_factory=CO2eFromOther)
    p_other_urea: CO2eFromOther = field(default_factory=CO2eFromOther)
    p_other_ecrop: CO2eFromOther = field(default_factory=CO2eFromOther)
    p_other_liming: CO2eEmissions = field(default_factory=CO2eEmissions)
    p_other_liming_calcit: CO2eFromOther = field(default_factory=CO2eFromOther)
    p_other_kas: Vars7 = field(default_factory=Vars7)
    p_operation: Vars8 = field(default_factory=Vars8)
    p_operation_heat: Vars9 = field(default_factory=Vars9)
    p_operation_elec_elcon: Vars10 = field(default_factory=Vars10)
    p_operation_elec_heatpump: Vars8 = field(default_factory=Vars8)
    p_operation_vehicles: Vars10 = field(default_factory=Vars10)
    s: Vars11 = field(default_factory=Vars11)
    s_petrol: Vars12 = field(default_factory=Vars12)
    s_diesel: Vars12 = field(default_factory=Vars12)
    s_fueloil: Vars12 = field(default_factory=Vars12)
    s_lpg: Vars12 = field(default_factory=Vars12)
    s_gas: Vars12 = field(default_factory=Vars12)
    s_biomass: Vars12 = field(default_factory=Vars12)
    s_elec: Vars12 = field(default_factory=Vars12)
    s_heatpump: Vars12 = field(default_factory=Vars12)


def calc(inputs: Inputs, *, l18: lulucf2018.L18, b18: business2018.B18) -> A18:
    def fact(n):
        return inputs.fact(n)

    entries = inputs.entries
    a18 = A18()
    a = a18.a
    p = a18.p
    g = a18.g
    p_fermen = a18.p_fermen
    p_other = a18.p_other
    p_other_kas = a18.p_other_kas
    p_operation = a18.p_operation
    p_operation_heat = a18.p_operation_heat
    p_operation_elec_elcon = a18.p_operation_elec_elcon
    p_operation_vehicles = a18.p_operation_vehicles
    s = a18.s
    s_petrol = a18.s_petrol
    s_diesel = a18.s_diesel
    s_fueloil = a18.s_fueloil
    s_lpg = a18.s_lpg
    s_gas = a18.s_gas
    s_biomass = a18.s_biomass
    s_elec = a18.s_elec
    s_heatpump = a18.s_heatpump
    p_operation_elec_heatpump = a18.p_operation_elec_heatpump
    s_heatpump.energy = 0.0
    s_heatpump.CO2e_production_based = 0.0
    s_heatpump.pct_energy = div(s_heatpump.energy, b18.s.energy)
    s_heatpump.CO2e_combustion_based_per_MWh = fact(
        "Fact_RB_S_heatpump_ratio_CO2e_to_fec"
    )
    s_heatpump.CO2e_combustion_based = (
        s_heatpump.energy * s_heatpump.CO2e_combustion_based_per_MWh
    )
    s_heatpump.CO2e_total = s_heatpump.CO2e_combustion_based
    g.CO2e_total = 0.0
    p_fermen_dairycow = CO2eFromFermentationOrManure.calc_fermen(inputs, "dairycow")
    p_fermen_nondairy = CO2eFromFermentationOrManure.calc_fermen(inputs, "nondairy")
    p_fermen_swine = CO2eFromFermentationOrManure.calc_fermen(
        inputs, "swine", alias="pig"
    )
    p_fermen_poultry = CO2eFromFermentationOrManure.calc_fermen(inputs, "poultry")
    p_fermen_oanimal = CO2eFromFermentationOrManure.calc_fermen(inputs, "oanimal")

    p_manure_dairycow = CO2eFromFermentationOrManure.calc_manure(
        inputs, "dairycow", amount=p_fermen_dairycow.amount
    )
    p_manure_nondairy = CO2eFromFermentationOrManure.calc_manure(
        inputs, "nondairy", amount=p_fermen_nondairy.amount
    )
    p_manure_swine = CO2eFromFermentationOrManure.calc_manure(
        inputs, "swine", amount=p_fermen_swine.amount
    )
    p_manure_poultry = CO2eFromFermentationOrManure.calc_manure(
        inputs, "poultry", amount=p_fermen_poultry.amount
    )
    p_manure_oanimal = CO2eFromFermentationOrManure.calc_manure(
        inputs, "oanimal", amount=p_fermen_oanimal.amount
    )
    p_manure_deposition = CO2eFromFermentationOrManure.calc_deposition(
        inputs,
        p_fermen_dairycow=p_fermen_dairycow,
        p_fermen_nondairy=p_fermen_nondairy,
        p_fermen_swine=p_fermen_swine,
        p_fermen_oanimal=p_fermen_oanimal,
    )
    p_manure = CO2eEmissions.sum(
        p_manure_dairycow,
        p_manure_nondairy,
        p_manure_swine,
        p_manure_poultry,
        p_manure_oanimal,
        p_manure_deposition,
    )

    # crop land soil emissions
    p_soil_fertilizer = CO2eFromSoil.calc(
        inputs.entries.a_soil_fertilizer_ratio_CO2e_to_ha, area_ha=l18.g_crop.area_ha
    )
    p_soil_manure = CO2eFromSoil.calc(
        inputs.entries.a_soil_manure_ratio_CO2e_to_ha, area_ha=l18.g_crop.area_ha
    )
    p_soil_sludge = CO2eFromSoil.calc(
        inputs.entries.a_soil_sludge_ratio_CO2e_to_ha, area_ha=l18.g_crop.area_ha
    )
    p_soil_ecrop = CO2eFromSoil.calc(
        inputs.entries.a_soil_ecrop_ratio_CO2e_to_ha, area_ha=l18.g_crop.area_ha
    )
    p_soil_residue = CO2eFromSoil.calc(
        inputs.entries.a_soil_residue_ratio_CO2e_to_ha, area_ha=l18.g_crop.area_ha
    )

    # grass land soil emissions
    # TODO: Fix spelling of grazing in entries
    p_soil_grazing = CO2eFromSoil.calc(
        inputs.entries.a_soil_crazing_ratio_CO2e_to_ha, area_ha=l18.g_grass.area_ha
    )

    # organic soil emissions
    p_soil_orgfarm = CO2eFromSoil.calc(
        inputs.entries.a_soil_orgfarm_ratio_CO2e_to_ha,
        area_ha=l18.g_crop_org_low.area_ha
        + l18.g_crop_org_high.area_ha
        + l18.g_grass_org_low.area_ha
        + l18.g_grass_org_high.area_ha,
    )
    p_soil_orgloss = CO2eFromSoil.calc(
        inputs.entries.a_soil_orgloss_ratio_CO2e_to_ha,
        area_ha=l18.g_crop_org_low.area_ha + l18.g_crop_org_high.area_ha,
    )

    # other soil emissions
    p_soil_leaching = CO2eFromSoil.calc(
        inputs.entries.a_soil_leaching_ratio_CO2e_to_ha,
        area_ha=l18.g_crop.area_ha + l18.g_grass.area_ha,
    )
    p_soil_deposition = CO2eFromSoil.calc(
        inputs.entries.a_soil_deposition_ratio_CO2e_to_ha,
        area_ha=l18.g_crop.area_ha + l18.g_grass.area_ha,
    )
    p_soil = CO2eEmissions.sum(
        p_soil_fertilizer,
        p_soil_manure,
        p_soil_sludge,
        p_soil_ecrop,
        p_soil_grazing,
        p_soil_residue,
        p_soil_orgfarm,
        p_soil_orgloss,
        p_soil_leaching,
        p_soil_deposition,
    )
    p_other_liming_calcit = CO2eFromOther.calc(inputs, "liming_calcit")
    p_other_liming_dolomite = CO2eFromOther.calc(inputs, "liming_dolomite")
    p_other_liming = CO2eEmissions.sum(p_other_liming_calcit, p_other_liming_dolomite)

    p_other_urea = CO2eFromOther.calc(inputs, "urea", ratio_suffix="")
    p_other_ecrop = CO2eFromOther.calc(inputs, "ecrop")
    p_other_kas = CO2eFromOther.calc(inputs, "kas")

    a18.p_fermen_dairycow = p_fermen_dairycow
    a18.p_fermen_nondairy = p_fermen_nondairy
    a18.p_fermen_swine = p_fermen_swine
    a18.p_fermen_poultry = p_fermen_poultry
    a18.p_fermen_oanimal = p_fermen_oanimal
    a18.p_manure_dairycow = p_manure_dairycow
    a18.p_manure_nondairy = p_manure_nondairy
    a18.p_manure_swine = p_manure_swine
    a18.p_manure_poultry = p_manure_poultry
    a18.p_manure_oanimal = p_manure_oanimal
    a18.p_manure_deposition = p_manure_deposition
    a18.p_manure = p_manure
    a18.p_soil_fertilizer = p_soil_fertilizer
    a18.p_soil_manure = p_soil_manure
    a18.p_soil_sludge = p_soil_sludge
    a18.p_soil_ecrop = p_soil_ecrop
    a18.p_soil_residue = p_soil_residue
    a18.p_soil_grazing = p_soil_grazing
    a18.p_soil_orgfarm = p_soil_orgfarm
    a18.p_soil_orgloss = p_soil_orgloss
    a18.p_soil_leaching = p_soil_leaching
    a18.p_soil_deposition = p_soil_deposition
    a18.p_soil = p_soil
    a18.p_other_liming_calcit = p_other_liming_calcit
    a18.p_other_liming_dolomite = p_other_liming_dolomite
    a18.p_other_liming = p_other_liming
    a18.p_other_urea = p_other_urea
    a18.p_other_ecrop = p_other_ecrop
    a18.p_other_kas = p_other_kas

    p_other.CO2e_combustion_based = 0.0
    p_other.CO2e_production_based = (
        p_other_liming.CO2e_production_based
        + p_other_urea.CO2e_production_based
        + p_other_kas.CO2e_production_based
        + p_other_ecrop.CO2e_production_based
    )
    p_other.CO2e_total = (
        p_other_liming.CO2e_total
        + p_other_urea.CO2e_total
        + p_other_kas.CO2e_total
        + p_other_ecrop.CO2e_total
    )
    s_petrol.CO2e_production_based = 0.0
    s_petrol.CO2e_combustion_based_per_MWh = fact(
        "Fact_T_S_petrol_EmFa_tank_wheel_2018"
    )
    s_petrol.energy = entries.a_petrol_fec
    s_petrol.CO2e_combustion_based = (
        s_petrol.energy * s_petrol.CO2e_combustion_based_per_MWh
    )
    s_petrol.CO2e_total = (
        s_petrol.CO2e_production_based + s_petrol.CO2e_combustion_based
    )
    s_diesel.CO2e_production_based = 0.0
    s_diesel.energy = entries.a_diesel_fec
    s_diesel.CO2e_combustion_based_per_MWh = fact(
        "Fact_T_S_diesel_EmFa_tank_wheel_2018"
    )
    s_diesel.CO2e_combustion_based = (
        s_diesel.energy * s_diesel.CO2e_combustion_based_per_MWh
    )
    s_diesel.CO2e_total = (
        s_diesel.CO2e_production_based + s_diesel.CO2e_combustion_based
    )
    s_fueloil.CO2e_production_based = 0.0
    s_fueloil.energy = entries.a_fueloil_fec
    s_fueloil.CO2e_combustion_based_per_MWh = fact("Fact_H_P_fueloil_cb_EF")
    s_fueloil.CO2e_combustion_based = (
        s_fueloil.energy * s_fueloil.CO2e_combustion_based_per_MWh
    )
    s_fueloil.CO2e_total = (
        s_fueloil.CO2e_production_based + s_fueloil.CO2e_combustion_based
    )
    s_lpg.CO2e_production_based = 0.0
    s_lpg.energy = entries.a_lpg_fec
    s_lpg.CO2e_combustion_based_per_MWh = fact("Fact_T_S_lpg_EmFa_tank_wheel_2018")
    s_lpg.CO2e_combustion_based = s_lpg.energy * s_lpg.CO2e_combustion_based_per_MWh
    s_lpg.CO2e_total = s_lpg.CO2e_production_based + s_lpg.CO2e_combustion_based
    s_gas.CO2e_production_based = 0.0
    s_gas.energy = entries.a_gas_fec
    s_gas.CO2e_combustion_based_per_MWh = fact("Fact_H_P_ngas_cb_EF")
    s_gas.CO2e_combustion_based = s_gas.energy * s_gas.CO2e_combustion_based_per_MWh
    s_gas.CO2e_total = s_gas.CO2e_production_based + s_gas.CO2e_combustion_based
    s_biomass.CO2e_production_based = 0.0
    s_biomass.energy = entries.a_biomass_fec
    s_biomass.CO2e_combustion_based_per_MWh = fact("Fact_RB_S_biomass_CO2e_EF")
    s_biomass.CO2e_combustion_based = (
        s_biomass.energy * s_biomass.CO2e_combustion_based_per_MWh
    )
    s_biomass.CO2e_total = (
        s_biomass.CO2e_production_based + s_biomass.CO2e_combustion_based
    )
    s_elec.CO2e_production_based = 0.0
    s_elec.energy = entries.a_elec_fec
    s_elec.CO2e_combustion_based_per_MWh = fact("Fact_RB_S_elec_ratio_CO2e_to_fec")
    s_elec.CO2e_combustion_based = s_elec.energy * s_elec.CO2e_combustion_based_per_MWh
    s_elec.CO2e_total = s_elec.CO2e_production_based + s_elec.CO2e_combustion_based
    s.CO2e_production_based = 0.0
    s.energy = (
        s_petrol.energy
        + s_diesel.energy
        + s_fueloil.energy
        + s_lpg.energy
        + s_gas.energy
        + s_biomass.energy
        + s_elec.energy
    )
    s_petrol.pct_energy = div(s_petrol.energy, s.energy)
    s_diesel.pct_energy = div(s_diesel.energy, s.energy)
    s_fueloil.pct_energy = div(s_fueloil.energy, s.energy)
    s_biomass.pct_energy = div(s_biomass.energy, s.energy)
    s_elec.pct_energy = div(s_elec.energy, s.energy)
    s_lpg.pct_energy = div(s_lpg.energy, s.energy)
    s_gas.pct_energy = div(s_gas.energy, s.energy)
    s.pct_energy = (
        s_petrol.pct_energy
        + s_diesel.pct_energy
        + s_fueloil.pct_energy
        + s_lpg.pct_energy
        + s_gas.pct_energy
        + s_biomass.pct_energy
        + s_elec.pct_energy
    )
    s.CO2e_combustion_based = (
        s_petrol.CO2e_combustion_based
        + s_diesel.CO2e_combustion_based
        + s_fueloil.CO2e_combustion_based
        + s_lpg.CO2e_combustion_based
        + s_gas.CO2e_combustion_based
        + s_biomass.CO2e_combustion_based
    )
    s.CO2e_total = s.CO2e_production_based + s.CO2e_combustion_based
    p_operation_elec_heatpump.energy = 0
    p_fermen.CO2e_production_based = p_fermen.CO2e_production_based = (
        p_fermen_dairycow.CO2e_production_based
        + p_fermen_nondairy.CO2e_production_based
        + p_fermen_swine.CO2e_production_based
        + p_fermen_poultry.CO2e_production_based
        + p_fermen_oanimal.CO2e_production_based
    )
    p_fermen.CO2e_combustion_based = 0.0
    p_fermen.CO2e_total = (
        p_fermen.CO2e_production_based + p_fermen.CO2e_combustion_based
    )
    p_operation.energy = s.energy
    p_operation_elec_elcon.energy = s_elec.energy
    p_operation_elec_elcon.pct_energy = div(
        p_operation_elec_elcon.energy, p_operation.energy
    )
    p_operation_vehicles.energy = s_petrol.energy + s_diesel.energy
    p_operation_vehicles.pct_energy = div(
        p_operation_vehicles.energy, p_operation.energy
    )
    p_operation_heat.area_m2 = (
        b18.p_nonresi.area_m2
        * fact("Fact_A_P_energy_buildings_ratio_A_to_B")
        / (1 - fact("Fact_A_P_energy_buildings_ratio_A_to_B"))
    )
    p_operation_heat.energy = (
        s_fueloil.energy + s_lpg.energy + s_gas.energy + s_biomass.energy
    )
    p_operation_heat.factor_adapted_to_fec = div(
        p_operation_heat.energy, p_operation_heat.area_m2
    )
    p_operation_heat.pct_energy = div(p_operation_heat.energy, p_operation.energy)
    p.CO2e_production_based = (
        p_fermen.CO2e_production_based
        + p_manure.CO2e_production_based
        + p_soil.CO2e_production_based
        + p_other.CO2e_production_based
    )
    p.CO2e_total = (
        p_fermen.CO2e_total
        + p_manure.CO2e_total
        + p_soil.CO2e_total
        + p_other.CO2e_total
    )
    p.energy = p_operation.energy
    a.CO2e_total = g.CO2e_total + p.CO2e_total + s.CO2e_total
    a.CO2e_production_based = p.CO2e_production_based
    a.CO2e_combustion_based = s.CO2e_combustion_based
    return a18
