from dataclasses import dataclass, asdict, field
from .inputs import Inputs
from .utils import div
from . import (
    fuels2018,
    agri2030,
    business2030,
    heat2030,
    industry2030,
    residences2030,
    transport2030,
)


@dataclass
class FColVars2030:
    demand_electricity: float = None
    demand_hydrogen: float = None
    energy: float = None
    CO2e_cb: float = None
    CO2e_pb: float = None
    CO2e_pb_per_MWh: float = None
    CO2e_total: float = None
    change_energy_MWh: float = None
    change_energy_pct: float = None
    change_CO2e_t: float = None
    CO2e_total_2021_estimated: float = None
    cost_climate_saved: float = None
    invest_pa: float = None
    invest_per_x: float = None
    invest: float = None
    pct_of_wage: float = None
    cost_wage: float = None
    ratio_wage_to_emplo: float = None
    demand_emplo: float = None
    power_to_be_installed: float = None
    full_load_hour: float = None
    change_CO2e_pct: float = None
    action: float = None
    emplo_existing: float = None
    demand_emplo_new: float = None
    invest_pa_outside: float = None
    invest_outside: float = None
    cost_mro_pa: float = None


@dataclass
class F30:
    f: FColVars2030 = field(default_factory=FColVars2030)
    g: FColVars2030 = field(default_factory=FColVars2030)
    d: FColVars2030 = field(default_factory=FColVars2030)
    d_r: FColVars2030 = field(default_factory=FColVars2030)
    d_b: FColVars2030 = field(default_factory=FColVars2030)
    d_i: FColVars2030 = field(default_factory=FColVars2030)
    d_t: FColVars2030 = field(default_factory=FColVars2030)
    d_a: FColVars2030 = field(default_factory=FColVars2030)
    p: FColVars2030 = field(default_factory=FColVars2030)

    d_e_hydrogen_reconv: FColVars2030 = field(default_factory=FColVars2030)
    p_petrol: FColVars2030 = field(default_factory=FColVars2030)
    p_jetfuel: FColVars2030 = field(default_factory=FColVars2030)
    p_diesel: FColVars2030 = field(default_factory=FColVars2030)
    p_bioethanol: FColVars2030 = field(default_factory=FColVars2030)
    p_biodiesel: FColVars2030 = field(default_factory=FColVars2030)
    p_biogas: FColVars2030 = field(default_factory=FColVars2030)
    p_emethan: FColVars2030 = field(default_factory=FColVars2030)
    p_hydrogen: FColVars2030 = field(default_factory=FColVars2030)
    p_hydrogen_reconv: FColVars2030 = field(default_factory=FColVars2030)

    # only medded for fuels pdf text
    p_hydrogen_total: FColVars2030 = field(default_factory=FColVars2030)
    p_efuels: FColVars2030 = field(default_factory=FColVars2030)

    def dict(self):
        return asdict(self)


def calc(
    inputs: Inputs,
    *,
    f18: fuels2018.F18,
    a30: agri2030.A30,
    b30: business2030.B30,
    h30: heat2030.H30,
    i30: industry2030.I30,
    r30: residences2030.R30,
    t30: transport2030.T30,
) -> F30:
    def fact(n):
        return inputs.fact(n)

    def ass(n):
        return inputs.ass(n)

    def entry(n):
        return inputs.entry(n)

    Million = 1000000

    f30 = F30()

    """ Start"""
    f30.d_r.energy = r30.p.demand_emethan
    f30.d_b.energy = b30.p.demand_ediesel + b30.p.demand_emethan
    f30.d_i.energy = i30.p.demand_emethan + i30.p.demand_hydrogen
    f30.d_t.energy = (
        t30.t.demand_epetrol
        + t30.t.demand_ediesel
        + t30.t.demand_ejetfuel
        + t30.t.demand_hydrogen
    )
    f30.d_a.energy = (
        a30.p_operation.demand_epetrol
        + a30.p_operation.demand_ediesel
        + a30.p_operation.demand_emethan
    )
    f30.p_petrol.energy = t30.t.demand_epetrol + a30.p_operation.demand_epetrol
    f30.p_jetfuel.energy = t30.t.demand_ejetfuel
    f30.p_diesel.energy = (
        b30.p.demand_ediesel + t30.t.demand_ediesel + a30.p_operation.demand_ediesel
    )
    f30.p_emethan.energy = (
        r30.p.demand_emethan
        + b30.p.demand_emethan
        + i30.p.demand_emethan
        + a30.p_operation.demand_emethan
    )
    f30.p_hydrogen.energy = i30.p.demand_hydrogen + t30.t.demand_hydrogen
    # ---------------------------
    f30.p_bioethanol.change_energy_MWh = -f18.p_bioethanol.energy
    f30.p_biodiesel.change_energy_MWh = -f18.p_biodiesel.energy
    f30.p_biogas.change_energy_MWh = -f18.p_biogas.energy
    f30.p_petrol.CO2e_total_2021_estimated = f18.p_petrol.CO2e_total * fact(
        "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
    )
    f30.p_jetfuel.CO2e_total_2021_estimated = f18.p_jetfuel.CO2e_total * fact(
        "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
    )
    f30.p_diesel.CO2e_total_2021_estimated = f18.p_diesel.CO2e_total * fact(
        "Fact_M_CO2e_wo_lulucf_2021_vs_2018"
    )
    f30.p_bioethanol.CO2e_total_2021_estimated = (
        f30.p_biodiesel.CO2e_total_2021_estimated
    ) = (
        f30.p_biogas.CO2e_total_2021_estimated
    ) = (
        f30.p_emethan.CO2e_total_2021_estimated
    ) = (
        f30.p_hydrogen.CO2e_total_2021_estimated
    ) = f30.p_hydrogen_reconv.CO2e_total_2021_estimated = 0

    # ---------------------------------------
    f30.p_petrol.CO2e_pb_per_MWh = -1 * fact("Fact_T_S_petrol_EmFa_tank_wheel_2018")
    f30.p_petrol.pct_of_wage = ass("Ass_S_constr_renew_gas_pct_of_wage_2017")
    f30.p_petrol.ratio_wage_to_emplo = ass("Ass_S_constr_renew_gas_wage_per_year_2017")
    f30.p_petrol.invest_per_x = ass("Ass_S_power_to_x_invest_per_power")
    f30.p_petrol.full_load_hour = ass("Ass_S_power_to_x_full_load_hours2")
    f30.p_jetfuel.CO2e_pb_per_MWh = -1 * fact("Fact_T_S_petroljet_EmFa_tank_wheel_2018")
    f30.p_jetfuel.pct_of_wage = ass("Ass_S_constr_renew_gas_pct_of_wage_2017")
    f30.p_jetfuel.ratio_wage_to_emplo = ass("Ass_S_constr_renew_gas_wage_per_year_2017")
    f30.p_jetfuel.invest_per_x = ass("Ass_S_power_to_x_invest_per_power")
    f30.p_jetfuel.full_load_hour = ass("Ass_S_power_to_x_full_load_hours2")
    f30.p_diesel.CO2e_pb_per_MWh = -1 * fact("Fact_T_S_diesel_EmFa_tank_wheel_2018")
    f30.p_diesel.pct_of_wage = ass("Ass_S_constr_renew_gas_pct_of_wage_2017")
    f30.p_diesel.ratio_wage_to_emplo = ass("Ass_S_constr_renew_gas_wage_per_year_2017")
    f30.p_diesel.invest_per_x = ass("Ass_S_power_to_x_invest_per_power")
    f30.p_diesel.full_load_hour = ass("Ass_S_power_to_x_full_load_hours2")
    f30.p_emethan.CO2e_pb_per_MWh = -1 * fact("Fact_T_S_methan_EmFa_tank_wheel_2018")
    f30.p_hydrogen.CO2e_pb_per_MWh = 0.0
    f30.p_hydrogen_reconv.CO2e_pb_per_MWh = 0
    # --------------------------------
    f30.p_emethan.pct_of_wage = ass("Ass_S_constr_renew_gas_pct_of_wage_2017")
    f30.p_emethan.ratio_wage_to_emplo = ass("Ass_S_constr_renew_gas_wage_per_year_2017")
    f30.p_emethan.invest_per_x = ass("Ass_S_methan_invest_per_power")
    f30.p_emethan.full_load_hour = ass("Ass_S_power_to_x_full_load_hours2")
    f30.p_hydrogen.pct_of_wage = ass("Ass_S_constr_renew_gas_pct_of_wage_2017")
    f30.p_hydrogen.ratio_wage_to_emplo = ass(
        "Ass_S_constr_renew_gas_wage_per_year_2017"
    )
    f30.p_hydrogen.invest_per_x = ass("Ass_S_electrolyses_invest_per_power")
    f30.p_hydrogen.full_load_hour = ass("Ass_F_P_electrolysis_full_load_hours")
    f30.p_hydrogen_reconv.invest_per_x = ass("Ass_S_electrolyses_invest_per_power")
    # ---------------------------------------
    f30.p_hydrogen_reconv.pct_of_wage = ass("Ass_S_constr_renew_gas_pct_of_wage_2017")
    # --------------------------------------
    f30.p_hydrogen_reconv.ratio_wage_to_emplo = ass(
        "Ass_S_constr_renew_gas_wage_per_year_2017"
    )
    # --------------------------------------
    f30.p_hydrogen_reconv.full_load_hour = ass("Ass_F_P_electrolysis_full_load_hours")
    # --------------------------------------
    f30.p_petrol.demand_electricity = f30.p_petrol.energy / ass(
        "Ass_S_power_to_x_efficiency"
    )
    f30.p_petrol.change_energy_MWh = f30.p_petrol.energy - f18.p_petrol.energy
    f30.p_jetfuel.demand_electricity = f30.p_jetfuel.energy / ass(
        "Ass_S_power_to_x_efficiency"
    )
    f30.p_jetfuel.change_energy_MWh = f30.p_jetfuel.energy - f18.p_jetfuel.energy
    f30.p_diesel.demand_electricity = f30.p_diesel.energy / ass(
        "Ass_S_power_to_x_efficiency"
    )
    f30.p_diesel.change_energy_MWh = f30.p_diesel.energy - f18.p_diesel.energy
    f30.p_emethan.demand_electricity = f30.p_emethan.energy / ass(
        "Ass_S_methan_efficiency"
    )  # -----------------------
    f30.p_emethan.change_energy_MWh = f30.p_emethan.energy
    f30.p_hydrogen.demand_electricity = f30.p_hydrogen.energy / ass(
        "Ass_F_P_electrolysis_efficiency"
    )

    f30.p_hydrogen.change_energy_MWh = f30.p_hydrogen.energy
    f30.p_bioethanol.change_energy_pct = div(
        f30.p_bioethanol.change_energy_MWh, f18.p_bioethanol.energy
    )
    f30.p_biodiesel.change_energy_pct = div(
        f30.p_biodiesel.change_energy_MWh, f18.p_biodiesel.energy
    )
    f30.p_biogas.change_energy_pct = div(
        f30.p_biogas.change_energy_MWh, f18.p_biogas.energy
    )
    # -------------------------------------
    f30.p.CO2e_total_2021_estimated = (
        f30.p_petrol.CO2e_total_2021_estimated
        + f30.p_jetfuel.CO2e_total_2021_estimated
        + f30.p_diesel.CO2e_total_2021_estimated
        + f30.p_bioethanol.CO2e_total_2021_estimated
        + f30.p_biodiesel.CO2e_total_2021_estimated
        + f30.p_biogas.CO2e_total_2021_estimated
        + f30.p_emethan.CO2e_total_2021_estimated
        + f30.p_hydrogen.CO2e_total_2021_estimated
        + f30.p_hydrogen_reconv.CO2e_total_2021_estimated
    )  # SUM(p_petrol.CO2e_total_2021_estimated:p_hydrogen_reconv.CO2e_total_2021_estimated)
    f30.p_petrol.CO2e_pb = f30.p_petrol.CO2e_pb_per_MWh * f30.p_petrol.energy
    f30.p_jetfuel.CO2e_pb = f30.p_jetfuel.CO2e_pb_per_MWh * f30.p_jetfuel.energy
    f30.p_diesel.CO2e_pb = f30.p_diesel.CO2e_pb_per_MWh * f30.p_diesel.energy
    f30.p_emethan.CO2e_pb = f30.p_emethan.CO2e_pb_per_MWh * f30.p_emethan.energy
    f30.p_hydrogen.CO2e_pb = f30.p_hydrogen_reconv.CO2e_pb = 0
    # --------------------------------
    f30.p_petrol.power_to_be_installed = div(
        f30.p_petrol.demand_electricity, f30.p_petrol.full_load_hour
    )
    f30.p_petrol.change_energy_pct = div(
        f30.p_petrol.change_energy_MWh, f18.p_petrol.energy
    )
    f30.p_jetfuel.power_to_be_installed = div(
        f30.p_jetfuel.demand_electricity, f30.p_jetfuel.full_load_hour
    )
    f30.p_jetfuel.change_energy_pct = div(
        f30.p_jetfuel.change_energy_MWh, f18.p_jetfuel.energy
    )
    f30.p_diesel.power_to_be_installed = f30.p_diesel.demand_electricity / ass(
        "Ass_S_power_to_x_full_load_hours2"
    )
    f30.p_diesel.change_energy_pct = div(
        f30.p_diesel.change_energy_MWh, f18.p_diesel.energy
    )
    f30.p_emethan.power_to_be_installed = div(
        f30.p_emethan.demand_electricity, f30.p_emethan.full_load_hour
    )
    # ---------------------------------------
    f30.p_hydrogen.power_to_be_installed = f30.p_hydrogen.demand_electricity / ass(
        "Ass_F_P_electrolysis_full_load_hours"
    )
    f30.p_hydrogen_reconv.energy = (
        (
            h30.p.demand_electricity
            + r30.p.demand_electricity
            + b30.p.demand_electricity
            + i30.p.demand_electricity
            + t30.t.demand_electricity
            + a30.p_operation.demand_electricity
            + f30.p_petrol.demand_electricity
            + f30.p_jetfuel.demand_electricity
            + f30.p_diesel.demand_electricity
            + f30.p_emethan.demand_electricity
            + f30.p_hydrogen.demand_electricity
        )
        * ass("Ass_E_P_renew_reverse_addon_to_demand_2035")
        / ass("Ass_E_P_renew_reverse_gud_efficiency")
    )
    f30.f.CO2e_total_2021_estimated = f30.p.CO2e_total_2021_estimated
    f30.p_petrol.CO2e_total = f30.p_petrol.CO2e_pb
    f30.p_jetfuel.CO2e_total = f30.p_jetfuel.CO2e_pb
    f30.p_diesel.CO2e_total = f30.p_diesel.CO2e_pb
    f30.p_hydrogen.CO2e_total = f30.p_hydrogen_reconv.CO2e_total = 0
    f30.p_biodiesel.change_CO2e_t = -f18.p_biodiesel.CO2e_total
    f30.p_bioethanol.change_CO2e_t = f30.p_biodiesel.change_CO2e_t
    f30.p_hydrogen.change_CO2e_t = (
        f30.p_hydrogen_reconv.change_CO2e_t
    ) = f30.p_biogas.change_CO2e_t = 0
    f30.p.CO2e_pb = (
        f30.p_petrol.CO2e_pb
        + f30.p_jetfuel.CO2e_pb
        + f30.p_diesel.CO2e_pb
        + f30.p_emethan.CO2e_pb
        + f30.p_hydrogen.CO2e_pb
        + f30.p_hydrogen_reconv.CO2e_pb
    )  # SUM(p_petrol.CO2e_pb:p_hydrogen_reconv.CO2e_pb)

    f30.p_emethan.CO2e_total = f30.p_emethan.CO2e_pb
    # ---------------------------------
    f30.p_petrol.invest = f30.p_petrol.power_to_be_installed * ass(
        "Ass_S_power_to_x_invest_per_power"
    )
    f30.p_jetfuel.invest = f30.p_jetfuel.power_to_be_installed * ass(
        "Ass_S_power_to_x_invest_per_power"
    )
    f30.p_diesel.invest = f30.p_diesel.power_to_be_installed * ass(
        "Ass_S_power_to_x_invest_per_power"
    )
    f30.p_emethan.invest = f30.p_emethan.power_to_be_installed * ass(
        "Ass_S_methan_invest_per_power"
    )
    # ---------------------------------------
    f30.p_hydrogen.invest = f30.p_hydrogen.power_to_be_installed * ass(
        "Ass_S_electrolyses_invest_per_power"
    )
    f30.d_e_hydrogen_reconv.energy = f30.p_hydrogen_reconv.energy
    f30.p.energy = (
        f30.p_petrol.energy
        + f30.p_jetfuel.energy
        + f30.p_diesel.energy
        + f30.p_emethan.energy
        + f30.p_hydrogen.energy
        + f30.p_hydrogen_reconv.energy
    )  # SUM(p_petrol.energy:p_hydrogen_reconv.energy)
    f30.p_hydrogen_reconv.demand_electricity = f30.p_hydrogen_reconv.energy / ass(
        "Ass_F_P_electrolysis_efficiency"
    )
    f30.p_hydrogen_reconv.change_energy_MWh = f30.p_hydrogen_reconv.energy
    # ---------------------------------
    f30.p_petrol.change_CO2e_t = f30.p_petrol.CO2e_total - f18.p_petrol.CO2e_total
    f30.p_petrol.cost_climate_saved = (
        (f30.p_petrol.CO2e_total_2021_estimated - f30.p_petrol.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    f30.p_jetfuel.change_CO2e_t = f30.p_jetfuel.CO2e_total - f18.p_jetfuel.CO2e_total
    f30.p_jetfuel.cost_climate_saved = (
        (f30.p_jetfuel.CO2e_total_2021_estimated - f30.p_jetfuel.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    f30.p_diesel.change_CO2e_t = f30.p_diesel.CO2e_total - f18.p_diesel.CO2e_total
    f30.p_diesel.cost_climate_saved = (
        (f30.p_diesel.CO2e_total_2021_estimated - f30.p_diesel.CO2e_total)
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    f30.f.CO2e_pb = f30.p.CO2e_pb
    f30.p.CO2e_total = (
        f30.p_petrol.CO2e_total
        + f30.p_jetfuel.CO2e_total
        + f30.p_diesel.CO2e_total
        + f30.p_emethan.CO2e_total
        + f30.p_hydrogen.CO2e_total
        + f30.p_hydrogen_reconv.CO2e_total
    )  # SUM(p_petrol.CO2e_total:p_hydrogen_reconv.CO2e_total)
    f30.p_emethan.change_CO2e_t = f30.p_emethan.CO2e_total
    # --------------------------------------
    f30.p_emethan.cost_climate_saved = (
        -f30.p_emethan.CO2e_total
        * entry("In_M_duration_neutral")
        * fact("Fact_M_cost_per_CO2e_2020")
    )
    f30.p_bioethanol.cost_climate_saved = (
        f30.p_biodiesel.cost_climate_saved
    ) = (
        f30.p_biogas.cost_climate_saved
    ) = f30.p_hydrogen.cost_climate_saved = f30.p_hydrogen_reconv.cost_climate_saved = 0
    f30.p_petrol.invest_pa = f30.p_petrol.invest / entry("In_M_duration_target")
    f30.p_jetfuel.invest_pa = f30.p_jetfuel.invest / entry("In_M_duration_target")
    f30.p_diesel.invest_pa = f30.p_diesel.invest / entry("In_M_duration_target")
    f30.p_emethan.invest_pa = f30.p_emethan.invest / entry("In_M_duration_target")
    # --------------------------------------
    f30.p_emethan.invest_outside = f30.p_emethan.invest
    f30.p_hydrogen.invest_pa = f30.p_hydrogen.invest / entry("In_M_duration_target")
    f30.p_hydrogen.invest_outside = f30.p_hydrogen.invest
    f30.d.energy = (
        f30.d_r.energy
        + f30.d_b.energy
        + f30.d_i.energy
        + f30.d_t.energy
        + f30.d_a.energy
        + f30.d_e_hydrogen_reconv.energy
    )  # SUM(d_r.energy:d_e_hydrogen_reconv.energy)
    f30.p.demand_electricity = (
        f30.p_petrol.demand_electricity
        + f30.p_jetfuel.demand_electricity
        + f30.p_diesel.demand_electricity
        + f30.p_emethan.demand_electricity
        + f30.p_hydrogen.demand_electricity
        + f30.p_hydrogen_reconv.demand_electricity
    )  # (SUM(p_petrol.demand_electricity:p_hydrogen_reconv.demand_electricity))
    f30.p_hydrogen_reconv.power_to_be_installed = (
        f30.p_hydrogen_reconv.demand_electricity
        / ass("Ass_F_P_electrolysis_full_load_hours")
    )
    f30.p.change_energy_MWh = (
        f30.p_petrol.change_energy_MWh
        + f30.p_jetfuel.change_energy_MWh
        + f30.p_diesel.change_energy_MWh
        + f30.p_bioethanol.change_energy_MWh
        + f30.p_biodiesel.change_energy_MWh
        + f30.p_biogas.change_energy_MWh
        + f30.p_emethan.change_energy_MWh
        + f30.p_hydrogen.change_energy_MWh
        + f30.p_hydrogen_reconv.change_energy_MWh
    )  # SUM(p_petrol.change_energy_MWh:p_hydrogen_reconv.change_energy_MWh)
    f30.p_petrol.change_CO2e_pct = div(
        f30.p_petrol.change_CO2e_t, f18.p_petrol.CO2e_total
    )
    f30.p_jetfuel.change_CO2e_pct = div(
        f30.p_jetfuel.change_CO2e_t, f18.p_jetfuel.CO2e_total
    )
    f30.p_diesel.change_CO2e_pct = div(
        f30.p_diesel.change_CO2e_t, f18.p_diesel.CO2e_total
    )
    f30.p_emethan.change_CO2e_pct = div(f30.p_emethan.change_CO2e_t, 0)
    f30.p_hydrogen.change_CO2e_pct = div(f30.p_hydrogen.change_CO2e_t, 0)
    f30.p_hydrogen_reconv.change_CO2e_pct = div(f30.p_hydrogen_reconv.change_CO2e_t, 0)

    f30.f.CO2e_total = f30.p.CO2e_total
    f30.p.change_CO2e_t = (
        f30.p_petrol.change_CO2e_t
        + f30.p_jetfuel.change_CO2e_t
        + f30.p_diesel.change_CO2e_t
        + f30.p_bioethanol.change_CO2e_t
        + f30.p_biodiesel.change_CO2e_t
        + f30.p_biogas.change_CO2e_t
        + f30.p_emethan.change_CO2e_t
        + f30.p_hydrogen.change_CO2e_t
        + f30.p_hydrogen_reconv.change_CO2e_t
    )  # SUM(p_petrol.change_CO2e_t:p_hydrogen_reconv.change_CO2e_t)
    # SUM(p_petrol.change_CO2e_t:p_hydrogen_reconv.change_CO2e_t)
    f30.p.cost_climate_saved = (
        f30.p_petrol.cost_climate_saved
        + f30.p_jetfuel.cost_climate_saved
        + f30.p_diesel.cost_climate_saved
        + f30.p_bioethanol.cost_climate_saved
        + f30.p_biodiesel.cost_climate_saved
        + f30.p_biogas.cost_climate_saved
        + f30.p_emethan.cost_climate_saved
        + f30.p_hydrogen.cost_climate_saved
        + f30.p_hydrogen_reconv.cost_climate_saved
    )  # SUM(p_petrol.cost_climate_saved:p_emethan.cost_climate_saved)
    f30.p_petrol.cost_wage = f30.p_petrol.invest_pa * f30.p_petrol.pct_of_wage
    f30.p_jetfuel.cost_wage = f30.p_jetfuel.invest_pa * f30.p_jetfuel.pct_of_wage
    f30.p_diesel.cost_wage = f30.p_diesel.invest_pa * f30.p_diesel.pct_of_wage
    f30.p_emethan.invest_pa_outside = f30.p_emethan.invest_pa
    f30.p_emethan.cost_wage = f30.p_emethan.invest_pa * f30.p_emethan.pct_of_wage
    # --------------------------------------
    f30.p_hydrogen.invest_pa_outside = f30.p_hydrogen.invest_pa
    f30.p_hydrogen.cost_wage = f30.p_hydrogen.invest_pa * f30.p_hydrogen.pct_of_wage
    f30.p_hydrogen_reconv.invest = (
        f30.p_hydrogen_reconv.power_to_be_installed * f30.p_hydrogen_reconv.invest_per_x
    )
    f30.f.change_energy_MWh = f30.p.change_energy_MWh
    f30.p.change_energy_pct = div(f30.p.change_energy_MWh, f18.p.energy)
    f30.f.change_CO2e_t = f30.p.change_CO2e_t
    f30.p.change_CO2e_pct = div(f30.p.change_CO2e_t, f18.p.CO2e_total)
    f30.f.cost_climate_saved = f30.p.cost_climate_saved
    f30.p_petrol.demand_emplo = div(
        f30.p_petrol.cost_wage, f30.p_petrol.ratio_wage_to_emplo
    )
    f30.p_jetfuel.demand_emplo = div(
        f30.p_jetfuel.cost_wage, f30.p_jetfuel.ratio_wage_to_emplo
    )
    f30.p_diesel.demand_emplo = div(
        f30.p_diesel.cost_wage, f30.p_diesel.ratio_wage_to_emplo
    )
    f30.p_emethan.demand_emplo = div(
        f30.p_emethan.cost_wage, f30.p_emethan.ratio_wage_to_emplo
    )
    f30.p_hydrogen.demand_emplo = (
        div(f30.p_hydrogen.cost_wage, f30.p_hydrogen.ratio_wage_to_emplo)
        if inputs.str_entry("In_M_AGS_com") == "DG000000"
        else 0
    )
    f30.p.invest = (
        f30.p_petrol.invest
        + f30.p_jetfuel.invest
        + f30.p_diesel.invest
        + f30.p_emethan.invest
        + f30.p_hydrogen.invest
        + f30.p_hydrogen_reconv.invest
    )  # SUM(p_petrol.invest:p_hydrogen_reconv.invest)
    f30.p_hydrogen_reconv.invest_pa = f30.p_hydrogen_reconv.invest / entry(
        "In_M_duration_target"
    )
    f30.p_hydrogen_reconv.invest_outside = f30.p_hydrogen_reconv.invest
    f30.f.change_energy_pct = f30.p.change_energy_pct
    f30.f.change_CO2e_pct = f30.p.change_CO2e_pct
    f30.p_petrol.demand_emplo_new = f30.p_petrol.demand_emplo
    f30.p_jetfuel.demand_emplo_new = f30.p_jetfuel.demand_emplo
    f30.p_diesel.demand_emplo_new = f30.p_diesel.demand_emplo
    f30.p_emethan.demand_emplo_new = f30.p_emethan.demand_emplo
    f30.p_hydrogen.demand_emplo_new = f30.p_hydrogen.demand_emplo
    f30.f.invest = f30.p.invest
    f30.p.invest_pa = (
        f30.p_petrol.invest_pa
        + f30.p_jetfuel.invest_pa
        + f30.p_diesel.invest_pa
        + f30.p_emethan.invest_pa
        + f30.p_hydrogen.invest_pa
        + f30.p_hydrogen_reconv.invest_pa
    )  # SUM(p_petrol.invest_pa:p_hydrogen_reconv.invest_pa)
    f30.p_hydrogen_reconv.invest_pa_outside = f30.p_hydrogen_reconv.invest_pa
    f30.p_hydrogen_reconv.cost_wage = (
        f30.p_hydrogen_reconv.invest_pa * f30.p_hydrogen_reconv.pct_of_wage
    )
    f30.p.invest_outside = (
        f30.p_emethan.invest_outside
        + f30.p_hydrogen.invest_outside
        + f30.p_hydrogen_reconv.invest_outside
    )
    f30.f.invest_pa = f30.p.invest_pa
    f30.p.invest_pa_outside = (
        f30.p_emethan.invest_pa_outside
        + f30.p_hydrogen.invest_pa_outside
        + f30.p_hydrogen_reconv.invest_pa_outside
    )
    f30.p.cost_wage = (
        f30.p_petrol.cost_wage
        + f30.p_jetfuel.cost_wage
        + f30.p_diesel.cost_wage
        + f30.p_emethan.cost_wage
        + f30.p_hydrogen.cost_wage
        + f30.p_hydrogen_reconv.cost_wage
    )  # SUM(p_petrol.cost_wage:p_hydrogen_reconv.cost_wage)
    f30.p_hydrogen_reconv.demand_emplo = (
        div(f30.p_hydrogen_reconv.cost_wage, f30.p_hydrogen_reconv.ratio_wage_to_emplo)
        if inputs.str_entry("In_M_AGS_com") == "DG000000"
        else 0
    )
    f30.f.invest_outside = f30.p.invest_outside
    f30.f.invest_pa_outside = f30.p.invest_pa_outside
    f30.f.cost_wage = f30.p.cost_wage
    f30.p.demand_emplo = (
        f30.p_petrol.demand_emplo
        + f30.p_jetfuel.demand_emplo
        + f30.p_diesel.demand_emplo
        + f30.p_emethan.demand_emplo
        + f30.p_hydrogen.demand_emplo
        + f30.p_hydrogen_reconv.demand_emplo
    )  # SUM(p_petrol.demand_emplo:p_hydrogen_reconv.demand_emplo)
    f30.p_hydrogen_reconv.demand_emplo_new = f30.p_hydrogen_reconv.demand_emplo
    f30.f.demand_emplo = f30.p.demand_emplo
    f30.p.demand_emplo_new = (
        f30.p_petrol.demand_emplo_new
        + f30.p_jetfuel.demand_emplo_new
        + f30.p_diesel.demand_emplo_new
        + f30.p_emethan.demand_emplo_new
        + f30.p_hydrogen.demand_emplo_new
        + f30.p_hydrogen_reconv.demand_emplo_new
    )  # SUM(p_petrol.demand_emplo_new:p_hydrogen_reconv.demand_emplo_new)
    f30.f.demand_emplo_new = f30.p.demand_emplo_new

    # only for fuel pdf text
    f30.p_hydrogen_total.energy = f30.p_hydrogen.energy + f30.p_hydrogen_reconv.energy
    f30.p_efuels.energy = (
        f30.p_petrol.energy + f30.p_diesel.energy + f30.p_jetfuel.energy
    )
    f30.p_efuels.change_CO2e_t = (
        f30.p_petrol.change_CO2e_t
        + f30.p_diesel.change_CO2e_t
        + f30.p_jetfuel.change_CO2e_t
    )
    # ------------

    return f30
