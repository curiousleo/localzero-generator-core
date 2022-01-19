#!/usr/bin/env python
# coding: utf-8

from dataclasses import dataclass
from setup import *
import time

@dataclass
class f:
    def __init__(self, value: float, unit: str):
        self.value = value
        self.unit = unit

    def __add__(self, other):
        print('operands: ', self.value, other.value)
        if self.value is None or other.value is None:
            return f(None)
        else:
            return f(self.value + other.value, self.unit)

@dataclass
class BColVars2030:
    energy: float = None
    pct_energy: float = None
    pct_x: float = None
    area_m2: float = None
    pct_nonrehab: float = None
    pct_rehab: float = None
    area_m2_nonrehab: float = None
    area_m2_rehab: float = None
    area_ha_available: float = None
    area_ha_available_pct_of_action: float = None
    demand_heatnet: float = None
    demand_biomass: float = None
    demand_solarth: float = None
    demand_heatpump: float = None
    demand_ediesel: float = None
    demand_emethan: float = None
    demand_emplo_new: float = None
    demand_ediesel: float = None
    demand_heat_nonrehab: float = None
    demand_heat_rehab: float = None
    demand_change: float = None
    rate_rehab_pa: float = None
    fec_factor_averaged: float = None
    cost_fuel: float = None
    cost_fuel_per_MWh: float = None
    CO2e_cb_per_MWh: float = None
    CO2e_pb:float = None
    CO2e_cb: float = None
    CO2e_total: float = None
    CO2e_total_2021_estimated: float = None
    change_energy_MWh: float = None
    change_energy_pct: float = None
    change_CO2e_pct: float = None
    change_CO2e_t: float = None
    cost_climate_saved: float = None
    change_cost_energy: float = None
    action: float = None
    invest_pa: float = None
    invest_pa_com: float = None
    invest: float = None
    invest_com: float = None
    pct_of_wage: float = None
    cost_wage: float = None
    ratio_wage_to_emplo: float = None
    ratio_wage_to_emplo: float = None
    demand_electricity: float = None
    demand_emplo: float = None
    emplo_existing: float = None
    invest_per_x: float = None
    power_to_be_installed: float = None
    power_installed: float = None
    full_load_hour: float = None
    cost_mro: float = None
    energy_installable: float = None
    power_to_be_installed_pct: float = None

@dataclass
class B30:
    # Klassenvariablen für GHD
    b: BColVars2030 = BColVars2030()
    g: BColVars2030 = BColVars2030()
    g_consult: BColVars2030 = BColVars2030()
    p: BColVars2030 = BColVars2030()
    p_nonresi: BColVars2030 = BColVars2030()
    p_nonresi_com: BColVars2030 = BColVars2030()
    p_elec_elcon: BColVars2030 = BColVars2030()
    p_elec_heatpump: BColVars2030 = BColVars2030()
    p_vehicles: BColVars2030 = BColVars2030()
    p_other: BColVars2030 = BColVars2030()
    s: BColVars2030 = BColVars2030()
    s_gas: BColVars2030 = BColVars2030()
    s_emethan: BColVars2030 = BColVars2030()
    s_lpg: BColVars2030 = BColVars2030()
    s_petrol: BColVars2030 = BColVars2030()
    s_jetfuel: BColVars2030 = BColVars2030()
    s_diesel: BColVars2030 = BColVars2030()
    s_fueloil: BColVars2030 = BColVars2030()
    s_biomass: BColVars2030 = BColVars2030()
    s_coal: BColVars2030 = BColVars2030()
    s_heatnet: BColVars2030 = BColVars2030()
    s_elec_heating: BColVars2030 = BColVars2030()
    s_heatpump: BColVars2030 = BColVars2030()
    s_solarth: BColVars2030 = BColVars2030()
    s_elec: BColVars2030 = BColVars2030()
    rp_p: BColVars2030 = BColVars2030()
    rb: BColVars2030 = BColVars2030()

    # erzeuge dictionry
    def dict(self):
        return asdict(self)



# Berechnungsfunktion im Sektor GHD für 2018

def Business2030_calc(root):
    ''''''
    ''' import external values'''
    import json
    if entry('In_M_AGS_com') == 'DG000000':
        excel_path = 'Excel_DG_values.json'
    elif entry('In_M_AGS_com') == '03159016':
        excel_path = 'Excel_Goe_values.json'

    with open(excel_path, 'r') as fp:
        exl = json.load(fp)
    fp.close()
    '''end'''
    root.r30.g_consult.demand_emplo = exl['r30']['g_consult']['demand_emplo']
    root.r30.p_buildings_total.demand_emplo = exl['r30']['p_buildings_total']['demand_emplo']
    root.a30.p_operation_heat.demand_emplo = exl['a30']['p_operation_heat']['demand_emplo']
    root.r30.s_solarth.demand_emplo = exl['r30']['s_solarth']['demand_emplo']
    root.r30.s_heatpump.demand_emplo = exl['r30']['s_heatpump']['demand_emplo']
    root.a30.s_heatpump.demand_emplo = exl['a30']['s_heatpump']['demand_emplo']
    root.r18.p_buildings_total.area_m2 = exl['r18']['p_buildings_total']['area_m2']
    root.e30.p_local_pv_roof.area_ha_available = exl['e30']['p_local_pv_roof']['area_ha_available']
    root.r30.s_solarth.invest_per_x = exl['r30']['s_solarth']['invest_per_x']
    root.r30.s.CO2e_total = exl['r30']['s']['CO2e_total']
    root.r30.p_buildings_total.change_energy_MWh = exl['r30']['p_buildings_total']['change_energy_MWh']
    root.r18.p_buildings_total.energy = exl['r18']['p_buildings_total']['energy']
    root.r30.s.cost_climate_saved = exl['r30']['s']['cost_climate_saved']
    root.r30.s.invest = exl['r30']['s']['invest']
    root.r30.s.invest_com = exl['r30']['s']['invest_com']
    root.r30.s.demand_emplo = exl['r30']['s']['demand_emplo']
    root.r30.g_consult.emplo_existing = exl['r30']['g_consult']['emplo_existing']
    root.r30.p_buildings_total.emplo_existing = exl['r30']['p_buildings_total']['emplo_existing']
    root.r30.s.emplo_existing = exl['r30']['s']['emplo_existing']
    root.r30.g_consult.demand_emplo_new = exl['r30']['g_consult']['demand_emplo_new']
    root.r30.p_buildings_total.demand_emplo_new = exl['r30']['p_buildings_total']['demand_emplo_new']
    root.r30.s.demand_emplo_new = exl['r30']['s']['demand_emplo_new']
    root.r30.p.energy = exl['r30']['p']['energy']
    root.r30.r.CO2e_cb = exl['r30']['r']['CO2e_cb']
    root.r30.r.CO2e_total = exl['r30']['r']['CO2e_total']
    root.r30.r.invest_pa = exl['r30']['r']['invest_pa']
    root.r30.r.invest_pa_com = exl['r30']['r']['invest_pa_com']
    root.r30.r.invest = exl['r30']['r']['invest']
    root.r30.r.invest_com = exl['r30']['r']['invest_com']
    root.r30.r.cost_wage = exl['r30']['r']['cost_wage']
    root.r30.r.demand_emplo = exl['r30']['r']['demand_emplo']
    root.r30.r.demand_emplo_new = exl['r30']['r']['demand_emplo_new']

    start = time.time()
    try:
        Million = 1000000.
        Kalkulationszeitraum = entry('In_M_duration_target')

        #Definitions production
        b18 = root.b18
        b30 = root.b30
        a30 = root.a30

        p = b30.p
        b = b30.b
        g = b30.g
        p_nonresi = b30.p_nonresi
        p_nonresi_com = b30.p_nonresi_com
        p_elec_elcon = b30.p_elec_elcon
        p_elec_heatpump = b30.p_elec_heatpump
        p_vehicles = b30.p_vehicles
        p_other = b30.p_other
        g_consult = b30.g_consult

        #Definitions supply
        s = b30.s
        b18 = root.b18
        r18 = root.r18
        r30 = root.r30
        e18 = root.e18
        e30 = root.e30
        s_gas = b30.s_gas
        s_emethan = b30.s_emethan
        s_lpg = b30.s_lpg
        s_petrol = b30.s_petrol
        s_jetfuel = b30.s_jetfuel
        s_diesel = b30.s_diesel
        s_fueloil = b30.s_fueloil
        s_biomass = b30.s_biomass
        s_coal = b30.s_coal
        s_heatnet = b30.s_heatnet
        s_elec_heating = b30.s_elec_heating
        s_heatpump = b30.s_heatpump
        s_solarth = b30.s_solarth
        s_elec = b30.s_elec
        rp_p = b30.rp_p
        rb = b30.rb

        #Calculation
        p_nonresi.rate_rehab_pa = entry('In_R_rehab_rate_pa')
        p_nonresi.pct_rehab = (
            min(1., fact('Fact_B_P_ratio_renovated_to_not_renovated_2021')  +
            p_nonresi.rate_rehab_pa * entry('In_M_duration_target'))
        )
        p_nonresi.pct_nonrehab = 1 - p_nonresi.pct_rehab
        p_nonresi.area_m2_nonrehab = p_nonresi.pct_nonrehab * b18.p_nonresi.area_m2

        p_nonresi.demand_heat_nonrehab = (
            p_nonresi.area_m2_nonrehab *
            (b18.p_nonresi.factor_adapted_to_fec - fact('Fact_B_P_ratio_renovated_to_not_renovated_2021') *
             ass('Ass_B_D_ratio_fec_to_area_2050')) / (1 - fact('Fact_B_P_ratio_renovated_to_not_renovated_2021'))
        )
        p_nonresi.area_m2_rehab = p_nonresi.pct_rehab * b18.p_nonresi.area_m2
        p_nonresi.demand_heat_rehab = (
                p_nonresi.area_m2_rehab * ass('Ass_B_D_ratio_fec_to_area_2050')
        )
        p_nonresi.energy = p_nonresi.demand_heat_nonrehab + p_nonresi.demand_heat_rehab

        p_nonresi.fec_factor_averaged = p_nonresi.energy / b18.p_nonresi.area_m2
        p_nonresi.invest_per_x = fact('Fact_R_P_energetical_renovation_cost_business')
        p_nonresi.change_energy_MWh = p_nonresi.energy - b18.p_nonresi.energy
        p_nonresi.area_m2 = b18.p_nonresi.area_m2
        p_nonresi.invest_pa_com = p_nonresi_com.invest_pa_com
        p_nonresi.invest = (
                p_nonresi.area_m2_rehab * (1 - fact('Fact_B_P_ratio_renovated_to_not_renovated_2021')) *
                p_nonresi.invest_per_x
        )
        p_nonresi.invest_pa = p_nonresi.invest / Kalkulationszeitraum
        p_nonresi.pct_of_wage = fact('Fact_B_P_renovations_ratio_wage_to_main_revenue_2017')
        p_nonresi.cost_wage = p_nonresi.invest / Kalkulationszeitraum * p_nonresi.pct_of_wage
        p_nonresi.ratio_wage_to_emplo = fact('Fact_B_P_renovations_wage_per_person_per_year_2017')
        p_nonresi.demand_emplo = p_nonresi.cost_wage / p_nonresi.ratio_wage_to_emplo

        p_nonresi_com.fec_factor_averaged = p_nonresi.fec_factor_averaged
        p_nonresi_com.area_m2_rehab = (
                p_nonresi.area_m2_rehab *
                ass('Ass_H_ratio_municipal_non_res_buildings_to_all_non_res_buildings_2050')
        )
        p_nonresi_com.area_m2 = b18.p_nonresi_com.area_m2
        p_nonresi_com.energy = p_nonresi_com.area_m2 * p_nonresi_com.fec_factor_averaged
        p_nonresi_com.change_energy_MWh = p_nonresi_com.energy - b18.p_nonresi_com.energy
        p_nonresi_com.invest_per_x = p_nonresi.invest_per_x
        p_nonresi_com.invest_com = (
            p_nonresi_com.area_m2_rehab * (1 - fact('Fact_B_P_ratio_renovated_to_not_renovated_2021')) *
            p_nonresi_com.invest_per_x
        )
        p_nonresi_com.invest_pa_com = p_nonresi_com.invest_com / Kalkulationszeitraum

        p_elec_elcon.demand_change = ass('Ass_B_D_fec_elec_elcon_change')
        p_elec_elcon.energy = (
            b18.p_elec_elcon.energy *
            (entry('In_M_population_com_203X') / entry('In_M_population_com_2018')) *
            (1 + p_elec_elcon.demand_change)
        )
        s_heatnet.energy = (
                entry('In_R_heatnet_ratio_year_target') *
                p_nonresi.fec_factor_averaged *
                b18.p_nonresi.area_m2
        )
        p_vehicles.demand_change = ass('Ass_B_D_fec_vehicles_change')
        p_vehicles.energy = b18.p_vehicles.energy * (1 + p_vehicles.demand_change)
        p_vehicles.demand_ediesel = p_vehicles.energy
        s_coal.pct_energy = 0
        s_gas.energy = 0
        s_lpg.energy = 0
        s_coal.energy = 0
        s_petrol.energy = 0
        s_jetfuel.energy = 0
        s_diesel.energy = p_vehicles.demand_ediesel
        s_fueloil.energy = 0
        s_biomass.energy = (
                b18.s_biomass.number_of_buildings * p_nonresi.fec_factor_averaged * b18.p_nonresi.area_m2 /
                b18.p_nonresi.number_of_buildings
        )

        s_elec_heating.energy = 0

        s_solarth.area_ha_available = e30.p_local_pv_roof.area_ha_available
        s_solarth.area_ha_available_pct_of_action = ass('Ass_E_P_local_pv_roof_potential')
        s_solarth.energy_installable = (
            s_solarth.area_ha_available * s_solarth.area_ha_available_pct_of_action *
            ass('Ass_R_P_soltherm_specific_yield_per_sqm') * 10000
        )
        s_solarth.power_to_be_installed_pct = entry('In_H_solartherm_to_be_inst')
        s_solarth.energy = (
            max(
                b18.p_nonresi.area_m2 / (r18.p_buildings_total.area_m2 + b18.p_nonresi.area_m2) *
                s_solarth.energy_installable * s_solarth.power_to_be_installed_pct,
                b18.s_solarth.energy)
        )
        s_heatpump.energy = (
            p_nonresi.demand_heat_rehab -
            (s_biomass.energy + s_heatnet.energy + s_solarth.energy) *
            p_nonresi.pct_rehab
        )
        p_elec_heatpump.energy = (
                s_heatpump.energy / fact('Fact_R_S_heatpump_mean_annual_performance_factor_all')
        )
        p_elec_elcon.demand_electricity = p_elec_elcon.energy
        p_elec_heatpump.demand_electricity = p_elec_heatpump.energy

        p_other.demand_electricity = (
                p_elec_elcon.demand_electricity + p_elec_heatpump.demand_electricity
        )
        p.demand_electricity = p_other.demand_electricity
        s_elec.energy = p.demand_electricity

        s_emethan.energy = (
            max(0,
                p_nonresi.energy - s_biomass.energy - s_heatnet.energy - s_heatpump.energy - s_solarth.energy)
        )
        p_other.energy = (
            p_elec_elcon.energy +
            p_elec_heatpump.energy +
            p_vehicles.energy
        ) #SUM(p_elec_elcon.energy:p_vehicles.energy)

        p.energy = (
                p_nonresi.energy + p_other.energy
        )
        s.energy = p.energy

        s_heatnet.pct_energy = s_heatnet.energy / s.energy


        s_gas.pct_energy = ass('Ass_R_S_fec_ratio_fossil_to_total_2050')

        s_biomass.pct_energy = s_biomass.energy / s.energy
        s_heatpump.pct_energy = s_heatpump.energy / s.energy
        s_solarth.pct_energy = s_solarth.energy / s.energy
        s_emethan.pct_energy = s_emethan.energy / s.energy
        s_diesel.pct_energy = s_diesel.energy / s.energy
        s_fueloil.pct_energy = 0
        s_heatnet.pct_energy = s_heatnet.energy / s.energy
        s_elec.pct_energy = s_elec.energy / s.energy

        s_gas.cost_fuel_per_MWh = ass('Ass_R_S_gas_energy_cost_factor_2035')
        s_biomass.cost_fuel_per_MWh = b18.s_biomass.cost_fuel_per_MWh
        s_biomass.cost_fuel = (
            s_biomass.energy * s_biomass.cost_fuel_per_MWh / Million
        )
        s_heatnet.cost_fuel_per_MWh = 0

        s_gas.cost_fuel = s_gas.energy * s_gas.cost_fuel_per_MWh / Million
        s_fueloil.cost_fuel = 0
        s_coal.cost_fuel = 0
        s_heatnet.cost_fuel = s_heatnet.energy * s_heatnet.cost_fuel_per_MWh / Million
        s_heatpump.cost_fuel = 0

        s.cost_fuel = (
            s_biomass.cost_fuel
        )

        s_gas.CO2e_cb_per_MWh = b18.s_gas.CO2e_cb_per_MWh
        s_lpg.CO2e_cb_per_MWh = b18.s_lpg.CO2e_cb_per_MWh
        s_petrol.CO2e_cb_per_MWh = b18.s_petrol.CO2e_cb_per_MWh
        s_jetfuel.CO2e_cb_per_MWh = b18.s_jetfuel.CO2e_cb_per_MWh
        s_diesel.CO2e_cb_per_MWh = b18.s_diesel.CO2e_cb_per_MWh
        s_fueloil.CO2e_cb_per_MWh = b18.s_fueloil.CO2e_cb_per_MWh
        s_biomass.CO2e_cb_per_MWh = b18.s_biomass.CO2e_cb_per_MWh
        s_coal.CO2e_cb_per_MWh = b18.s_coal.CO2e_cb_per_MWh
        s_heatnet.CO2e_cb_per_MWh = 0
        s_elec_heating.CO2e_cb_per_MWh = 0
        s_heatpump.CO2e_cb_per_MWh = 0
        s_solarth.CO2e_cb_per_MWh = 0


        s_gas.CO2e_cb = s_gas.energy * s_gas.CO2e_cb_per_MWh
        s_lpg.CO2e_cb = s_lpg.energy * s_lpg.CO2e_cb_per_MWh
        s_petrol.CO2e_cb = s_petrol.energy * s_petrol.CO2e_cb_per_MWh
        s_jetfuel.CO2e_cb = s_jetfuel.energy * s_jetfuel.CO2e_cb_per_MWh
        s_diesel.CO2e_cb = 0
        s_fueloil.CO2e_cb = s_fueloil.energy * s_fueloil.CO2e_cb_per_MWh
        s_biomass.CO2e_cb = s_biomass.energy * s_biomass.CO2e_cb_per_MWh
        s_coal.CO2e_cb = s_coal.energy * s_coal.CO2e_cb_per_MWh
        s_heatnet.CO2e_cb = s_heatnet.energy * s_heatnet.CO2e_cb_per_MWh
        s_elec_heating.CO2e_cb = s_elec_heating.energy * s_elec_heating.CO2e_cb_per_MWh
        s_heatpump.CO2e_cb = s_heatpump.energy * s_heatpump.CO2e_cb_per_MWh
        s_solarth.CO2e_cb = s_solarth.energy * s_solarth.CO2e_cb_per_MWh

        s_emethan.CO2e_cb_per_MWh = fact('Fact_T_S_methan_EmFa_tank_wheel_2018')
        s_emethan.CO2e_cb = (
                s_emethan.energy * s_emethan.CO2e_cb_per_MWh
        )
        s.CO2e_cb = (
            s_gas.CO2e_cb +
            s_emethan.CO2e_cb +
            s_lpg.CO2e_cb +
            s_petrol.CO2e_cb +
            s_jetfuel.CO2e_cb +
            s_diesel.CO2e_cb +
            s_fueloil.CO2e_cb +
            s_biomass.CO2e_cb +
            s_coal.CO2e_cb +
            s_heatnet.CO2e_cb +
            s_heatpump.CO2e_cb +
            s_solarth.CO2e_cb
        ) #	(SUM(s_gas.CO2e_cb:s_solarth.CO2e_cb))


        s.CO2e_total = 0 + s.CO2e_cb


        s.change_energy_MWh = s.energy - b18.s.energy
        s_gas.change_energy_MWh = s_gas.energy - b18.s_gas.energy
        s_lpg.change_energy_MWh = s_lpg.energy - b18.s_lpg.energy
        s_petrol.change_energy_MWh = s_petrol.energy - b18.s_petrol.energy
        s_jetfuel.change_energy_MWh = s_jetfuel.energy - b18.s_jetfuel.energy
        s_diesel.change_energy_MWh = s_diesel.energy - b18.s_diesel.energy
        s_fueloil.change_energy_MWh = s_fueloil.energy - b18.s_fueloil.energy
        s_biomass.change_energy_MWh = s_biomass.energy - b18.s_biomass.energy
        s_coal.change_energy_MWh = s_coal.energy - b18.s_coal.energy
        s_heatnet.change_energy_MWh = s_heatnet.energy - b18.s_heatnet.energy
        s_elec_heating.change_energy_MWh = s_elec_heating.energy - b18.s_elec_heating.energy
        s_heatpump.change_energy_MWh = s_heatpump.energy - b18.s_heatpump.energy
        s_solarth.change_energy_MWh = s_solarth.energy - b18.s_solarth.energy


        s.change_energy_pct = s.change_energy_MWh / b18.s.energy
        s_gas.change_energy_pct = s_gas.change_energy_MWh / b18.s_gas.energy
        s_lpg.change_energy_pct = s_lpg.change_energy_MWh / b18.s_lpg.energy
        s_petrol.change_energy_pct = s_petrol.change_energy_MWh / b18.s_petrol.energy
        s_jetfuel.change_energy_pct = s_jetfuel.change_energy_MWh / b18.s_jetfuel.energy
        s_diesel.change_energy_pct = s_diesel.change_energy_MWh / b18.s_diesel.energy
        s_fueloil.change_energy_pct = s_fueloil.change_energy_MWh / b18.s_fueloil.energy
        s_biomass.change_energy_pct = s_biomass.change_energy_MWh / b18.s_biomass.energy
        s_coal.change_energy_pct = s_coal.change_energy_MWh / b18.s_coal.energy
        s_heatnet.change_energy_pct = s_heatnet.change_energy_MWh / b18.s_heatnet.energy
        s_elec_heating.change_energy_pct = s_elec_heating.change_energy_MWh / b18.s_elec_heating.energy
        s_heatpump.change_energy_pct = s_heatpump.change_energy_MWh / b18.s_heatpump.energy
        s_solarth.change_energy_pct = s_solarth.change_energy_MWh / b18.s_solarth.energy

        s.change_CO2e_t = s.CO2e_cb - b18.s.CO2e_cb
        s_gas.change_CO2e_t = s_gas.CO2e_cb - b18.s_gas.CO2e_cb
        s_lpg.change_CO2e_t = s_lpg.CO2e_cb - b18.s_lpg.CO2e_cb
        s_petrol.change_CO2e_t = s_petrol.CO2e_cb - b18.s_petrol.CO2e_cb
        s_jetfuel.change_CO2e_t = s_jetfuel.CO2e_cb - b18.s_jetfuel.CO2e_cb
        s_diesel.change_CO2e_t = s_diesel.CO2e_cb - b18.s_diesel.CO2e_cb
        s_fueloil.change_CO2e_t = s_fueloil.CO2e_cb - b18.s_fueloil.CO2e_cb
        s_biomass.change_CO2e_t = s_biomass.CO2e_cb - b18.s_biomass.CO2e_cb
        s_coal.change_CO2e_t = s_coal.CO2e_cb - b18.s_coal.CO2e_cb
        s_emethan.change_CO2e_t =  - s_emethan.energy * b18.s_gas.CO2e_cb_per_MWh
        s_heatnet.change_CO2e_t = s_heatnet.CO2e_cb
        s_elec_heating.change_CO2e_t = s_elec_heating.CO2e_cb
        s_solarth.change_CO2e_t = s_solarth.CO2e_cb
        s.change_CO2ee_pct = (s.change_CO2e_t / b18.s.CO2e_cb)

        p_nonresi.change_CO2e_t = 0
        s_heatpump.change_CO2e_t = s.change_CO2e_t - (s_emethan.change_CO2e_t + p_nonresi.change_CO2e_t)

        s_gas.CO2e_total_2021_estimated = b18.s_gas.CO2e_cb * fact('Fact_M_CO2e_wo_lulucf_2021_vs_2018')
        s_lpg.CO2e_total_2021_estimated = b18.s_lpg.CO2e_cb * fact('Fact_M_CO2e_wo_lulucf_2021_vs_2018')
        s_petrol.CO2e_total_2021_estimated = b18.s_petrol.CO2e_cb * fact('Fact_M_CO2e_wo_lulucf_2021_vs_2018')
        s_jetfuel.CO2e_total_2021_estimated = b18.s_jetfuel.CO2e_cb * fact('Fact_M_CO2e_wo_lulucf_2021_vs_2018')
        s_diesel.CO2e_total_2021_estimated = b18.s_diesel.CO2e_cb * fact('Fact_M_CO2e_wo_lulucf_2021_vs_2018')
        s_fueloil.CO2e_total_2021_estimated = b18.s_fueloil.CO2e_cb * fact('Fact_M_CO2e_wo_lulucf_2021_vs_2018')
        s_biomass.CO2e_total_2021_estimated = b18.s_biomass.CO2e_cb * fact('Fact_M_CO2e_wo_lulucf_2021_vs_2018')
        s_coal.CO2e_total_2021_estimated = b18.s_coal.CO2e_cb * fact('Fact_M_CO2e_wo_lulucf_2021_vs_2018')
        s_heatnet.CO2e_total_2021_estimated = b18.s_heatnet.CO2e_cb * fact('Fact_M_CO2e_wo_lulucf_2021_vs_2018')
        s_elec_heating.CO2e_total_2021_estimated = b18.s_elec_heating.CO2e_cb * fact('Fact_M_CO2e_wo_lulucf_2021_vs_2018')
        s_heatpump.CO2e_total_2021_estimated = b18.s_heatpump.CO2e_cb * fact('Fact_M_CO2e_wo_lulucf_2021_vs_2018')
        s_solarth.CO2e_total_2021_estimated = b18.s_solarth.CO2e_cb * fact('Fact_M_CO2e_wo_lulucf_2021_vs_2018')

        s.CO2e_total_2021_estimated = (
            s_gas.CO2e_total_2021_estimated +
            s_lpg.CO2e_total_2021_estimated +
            s_petrol.CO2e_total_2021_estimated +
            s_jetfuel.CO2e_total_2021_estimated +
            s_diesel.CO2e_total_2021_estimated +
            s_fueloil.CO2e_total_2021_estimated +
            s_biomass.CO2e_total_2021_estimated +
            s_coal.CO2e_total_2021_estimated
            #todo all the rest
        )

        #    SUM(s_gas.CO2e_total_2021_estimated:s_solarth.CO2e_total_2021_estimated)

        KlimaneutraleJahre = entry('In_M_duration_neutral')

        # todo: CO2e_pb not definied
        s_gas.cost_climate_saved = (
            (s_gas.CO2e_total_2021_estimated - (s_gas.CO2e_cb) ) *
            KlimaneutraleJahre * fact('Fact_M_cost_per_CO2e_2020')
        )
        s_lpg.cost_climate_saved = (
                (s_lpg.CO2e_total_2021_estimated - (s_lpg.CO2e_cb) ) *
                KlimaneutraleJahre * fact('Fact_M_cost_per_CO2e_2020')
        )
        s_petrol.cost_climate_saved = (
                (s_petrol.CO2e_total_2021_estimated - (s_petrol.CO2e_cb) ) *
                KlimaneutraleJahre * fact('Fact_M_cost_per_CO2e_2020')
        )
        s_jetfuel.cost_climate_saved = (
                (s_jetfuel.CO2e_total_2021_estimated - (s_jetfuel.CO2e_cb) ) *
                KlimaneutraleJahre * fact('Fact_M_cost_per_CO2e_2020')
        )
        s_diesel.cost_climate_saved = (
                (s_diesel.CO2e_total_2021_estimated - (s_diesel.CO2e_cb) ) *
                KlimaneutraleJahre * fact('Fact_M_cost_per_CO2e_2020')
        )
        s_fueloil.cost_climate_saved = (
                (s_fueloil.CO2e_total_2021_estimated - (s_fueloil.CO2e_cb) ) *
                KlimaneutraleJahre * fact('Fact_M_cost_per_CO2e_2020')
        )
        s_biomass.cost_climate_saved = (
                (s_biomass.CO2e_total_2021_estimated - (s_biomass.CO2e_cb) ) *
                KlimaneutraleJahre * fact('Fact_M_cost_per_CO2e_2020')
        )
        s_coal.cost_climate_saved = (
                (s_coal.CO2e_total_2021_estimated - (s_coal.CO2e_cb) ) *
                KlimaneutraleJahre * fact('Fact_M_cost_per_CO2e_2020')
        )
        s_heatnet.cost_climate_saved = (
                (s_heatnet.CO2e_total_2021_estimated - (s_heatnet.CO2e_cb) ) *
                KlimaneutraleJahre * fact('Fact_M_cost_per_CO2e_2020')
        )
        s_elec_heating.cost_climate_saved = (
                (s_elec_heating.CO2e_total_2021_estimated - (s_elec_heating.CO2e_cb) ) *
                KlimaneutraleJahre * fact('Fact_M_cost_per_CO2e_2020')
        )
        s_heatpump.cost_climate_saved = (
                (s_heatpump.CO2e_total_2021_estimated - (s_heatpump.CO2e_cb) ) *
                KlimaneutraleJahre * fact('Fact_M_cost_per_CO2e_2020')
        )
        s_solarth.cost_climate_saved = (
                (s_solarth.CO2e_total_2021_estimated - (s_solarth.CO2e_cb) ) *
                KlimaneutraleJahre * fact('Fact_M_cost_per_CO2e_2020')
        )
        s.cost_climate_saved = (
                (s.CO2e_total_2021_estimated - s.CO2e_cb) *
                entry('In_M_duration_neutral') * fact('Fact_M_cost_per_CO2e_2020')
        )
        s.change_cost_energy = s.cost_fuel - b18.s.cost_fuel
        s_gas.change_cost_energy = s_gas.cost_fuel - b18.s_gas.cost_fuel
        s_fueloil.change_cost_energy = s_fueloil.cost_fuel - b18.s_fueloil.cost_fuel
        s_biomass.change_cost_energy = s_biomass.cost_fuel - b18.s_biomass.cost_fuel
        s_coal.change_cost_energy = s_coal.cost_fuel - b18.s_coal.cost_fuel
        s_heatnet.change_cost_energy = s_heatnet.cost_fuel - b18.s_heatnet.cost_fuel
        s_heatpump.change_cost_energy = s_heatpump.cost_fuel - b18.s_heatpump.cost_fuel


        #s_heatpump.actionAusbau
        #s_solarth.actionAusbau

        s_gas.full_load_hour = fact('Fact_B_S_full_usage_hours_buildings')
        s_heatpump.full_load_hour = fact('Fact_B_S_full_usage_hours_buildings')

        s_gas.full_load_hour = (fact('Fact_B_S_full_usage_hours_buildings'))
        s_heatpump.full_load_hour = (fact('Fact_B_S_full_usage_hours_buildings'))
        s_heatpump.power_installed = b18.s_heatpump.energy / s_heatpump.full_load_hour
        s_heatpump.power_to_be_installed = (
            max(s_heatpump.energy / s_heatpump.full_load_hour - s_heatpump.power_installed, 0)
        )
        s_heatpump.invest_per_x = fact('Fact_R_S_heatpump_cost')
        s_heatpump.invest = s_heatpump.invest_per_x * s_heatpump.power_to_be_installed * 1000
        s_heatpump.invest_pa = s_heatpump.invest / Kalkulationszeitraum

        s_heatpump.pct_of_wage = fact('Fact_B_P_plumbing_ratio_wage_to_main_revenue_2017')
        s_heatpump.cost_wage = s_heatpump.invest_pa * s_heatpump.pct_of_wage
        s_solarth.pct_of_wage = fact('Fact_B_P_plumbing_ratio_wage_to_main_revenue_2017')

        s_solarth.invest = (
            b18.p_nonresi.area_m2 / (r18.p_buildings_total.area_m2 + b18.p_nonresi.area_m2) *
            e30.p_local_pv_roof.area_ha_available *
            entry('In_H_solartherm_to_be_inst') *
            r30.s_solarth.invest_per_x * 10000
        )

        s_solarth.invest_pa = s_solarth.invest / Kalkulationszeitraum
        s_solarth.cost_wage = s_solarth.invest_pa * s_solarth.pct_of_wage
        s_solarth.ratio_wage_to_emplo = fact('Fact_B_P_heating_wage_per_person_per_year')
        s_solarth.demand_emplo = s_solarth.cost_wage / s_solarth.ratio_wage_to_emplo
        s_heatpump.ratio_wage_to_emplo = fact('Fact_B_P_heating_wage_per_person_per_year')
        s_heatpump.demand_emplo = s_heatpump.cost_wage / s_heatpump.ratio_wage_to_emplo

        s_heatpump.emplo_existing = (
            fact('Fact_B_P_install_heating_emplo_2017') * entry('In_M_population_com_2018') /
            entry('In_M_population_nat') * s_heatpump.demand_emplo /
            (r30.s_solarth.demand_emplo + r30.s_heatpump.demand_emplo +
             s_heatpump.demand_emplo + s_solarth.demand_emplo + a30.s_heatpump.demand_emplo)
        )

        g_consult.ratio_wage_to_emplo = fact('Fact_R_G_energy_consulting_cost_personel')
        g_consult.invest = (
            fact('Fact_R_G_energy_consulting_cost_appt_building_ge_3_flats') *
            b18.p_nonresi.number_of_buildings
        )
        g_consult.invest_pa = g_consult.invest / Kalkulationszeitraum
        g_consult.cost_wage = g_consult.invest_pa
        g_consult.demand_emplo = g_consult.cost_wage / g_consult.ratio_wage_to_emplo
        g_consult.invest_com = g_consult.invest
        p_nonresi.change_energy_pct = p_nonresi.change_energy_MWh / b18.p_nonresi.energy
        p_nonresi_com.change_energy_pct = p_nonresi_com.change_energy_MWh / b18.p_nonresi_com.energy

        s.invest = s_heatpump.invest + s_solarth.invest
        s_heatpump.invest_com = (
            s_heatpump.invest *
            ass('Ass_H_ratio_municipal_non_res_buildings_to_all_non_res_buildings_2050')
        )
        s_solarth.invest_com = (
            s_solarth.invest *
            ass('Ass_H_ratio_municipal_non_res_buildings_to_all_non_res_buildings_2050')
        )
        s.invest_com = (
            s_heatpump.invest_com + s_solarth.invest_com
        )
        s_solarth.invest_pa_com = s_solarth.invest_com / Kalkulationszeitraum
        s_solarth.invest_per_x = ass('Ass_R_P_soltherm_cost_per_sqm')
        s_heatpump.invest_pa_com = s_heatpump.invest_com / Kalkulationszeitraum
        s_lpg.pct_energy = ass('Ass_R_S_fec_ratio_fossil_to_total_2050')
        s_petrol.pct_energy = ass('Ass_R_S_fec_ratio_fossil_to_total_2050')
        s_jetfuel.pct_energy = (ass('Ass_R_S_fec_ratio_fossil_to_total_2050'))
        s.pct_energy = (
            s_gas.pct_energy +
            s_emethan.pct_energy +
            s_lpg.pct_energy +
            s_petrol.pct_energy +
            s_jetfuel.pct_energy +
            s_diesel.pct_energy +
            s_fueloil.pct_energy +
            s_biomass.pct_energy +
            s_coal.pct_energy +
            s_heatnet.pct_energy +
            s_heatpump.pct_energy +
            s_solarth.pct_energy +
            s_elec.pct_energy
        ) #SUM(s_gas.pct_energy:s_elec.pct_energy)

        s.CO2e_total = s.CO2e_cb

        p_nonresi.emplo_existing = (
            fact('Fact_B_P_renovation_emplo_2017') * p_nonresi.demand_emplo /
            (r30.p_buildings_total.demand_emplo + p_nonresi.demand_emplo + a30.p_operation_heat.demand_emplo) *
            entry('In_M_population_com_2018') / entry('In_M_population_nat')
        )
        p_nonresi.cost_mro = p_nonresi.invest * (1.5/100) #%

        b.CO2e_cb = (s.CO2e_cb)
        b.CO2e_total = (s.CO2e_total)
        b.change_energy_MWh = (s.change_energy_MWh)
        b.change_energy_pct = (s.change_energy_pct)
        b.change_CO2e_t = (s.change_CO2e_t)
        s.change_CO2e_pct = ((s.change_CO2e_t / b18.s.CO2e_cb))
        b.CO2e_total_2021_estimated = (s.CO2e_total_2021_estimated)
        b.cost_climate_saved = (s.cost_climate_saved)
        g.invest_pa = (g_consult.invest_pa)
        g_consult.invest_pa_com = (g_consult.invest_com / entry('In_M_duration_target'))
        g.invest = (g_consult.invest)
        g.invest_com = (g_consult.invest_com)
        g.cost_wage = (g_consult.cost_wage)
        g.demand_emplo = (g_consult.demand_emplo)
        g_consult.emplo_existing = (fact('Fact_R_G_energy_consulting_total_personel') * g_consult.demand_emplo / (r30.g_consult.demand_emplo + g_consult.demand_emplo) * entry('In_M_population_com_2018') / entry('In_M_population_nat'))
        p.invest_pa = (p_nonresi.invest_pa)
        p_nonresi.invest_pa_com = (p_nonresi_com.invest_pa_com)
        p.invest = (p_nonresi.invest)
        p_nonresi.invest_com = (p_nonresi_com.invest_com)
        p.cost_wage = (p_nonresi.cost_wage)
        p.demand_emplo = (p_nonresi.demand_emplo)
        p_nonresi.demand_emplo_new = (max(0,p_nonresi.demand_emplo - p_nonresi.emplo_existing))
        g.invest_pa_com = (g_consult.invest_pa_com)
        g_consult.demand_emplo_new = (max(0,g_consult.demand_emplo - g_consult.emplo_existing))
        g.demand_emplo_new = (g_consult.demand_emplo_new)
        p.demand_heatnet = (s_heatnet.energy)
        p.demand_biomass = (s_biomass.energy)
        p.demand_solarth = (s_solarth.energy)
        p.demand_heatpump = (s_heatpump.energy)
        p_other.demand_ediesel = (p_vehicles.demand_ediesel)
        p.demand_emethan = (s_emethan.energy)
        p.change_energy_MWh = (p.energy - b18.p.energy)
        p.change_energy_pct = (p.change_energy_MWh / b18.p.energy)
        s.invest_pa = (s_heatpump.invest_pa + s_solarth.invest_pa)
        s.invest_pa_com = (s_heatpump.invest_pa_com + s_solarth.invest_pa_com)
        b.invest = (g.invest + p.invest + s.invest)
        p.invest_com = (p_nonresi.invest_com)
        s.cost_wage = (s_heatpump.cost_wage + s_solarth.cost_wage)
        s.demand_emplo = (s_heatpump.demand_emplo + s_solarth.demand_emplo)
        s_heatpump.demand_emplo_new = (max(0,s_heatpump.demand_emplo - s_heatpump.emplo_existing))
        p.invest_pa_com = (p_nonresi.invest_pa_com)
        b.invest_com = (g.invest_com + p.invest_com + s.invest_com)
        p.demand_emplo_new = (p_nonresi.demand_emplo_new)
        p_nonresi_com.invest = (p_nonresi_com.area_m2_rehab * (1 - fact('Fact_B_P_ratio_renovated_to_not_renovated_2021')) * p_nonresi_com.invest_per_x)
        p_nonresi_com.invest_pa = (p_nonresi_com.invest / entry('In_M_duration_target'))
        p.demand_ediesel = (p_other.demand_ediesel)
        p_other.change_energy_MWh = (p_other.energy - b18.p_other.energy)
        p_other.change_energy_pct = (p_other.change_energy_MWh / b18.p_other.energy)
        p_elec_elcon.change_energy_MWh = (p_elec_elcon.energy - b18.p_elec_elcon.energy)
        p_elec_elcon.change_energy_pct = (p_elec_elcon.change_energy_MWh / b18.p_elec_elcon.energy)
        p_elec_heatpump.change_energy_MWh = (p_elec_heatpump.energy - b18.p_elec_heatpump.energy)
        p_elec_heatpump.change_energy_pct = (p_elec_heatpump.change_energy_MWh / b18.p_elec_heatpump.energy)
        p_vehicles.change_energy_MWh = (p_vehicles.energy - b18.p_vehicles.energy)
        p_vehicles.change_energy_pct = (p_vehicles.change_energy_MWh / b18.p_vehicles.energy)
        b.change_CO2e_pct = (s.change_CO2e_pct)
        b.invest_pa = (g.invest_pa + p.invest_pa + s.invest_pa)
        b.invest_pa_com = (g.invest_pa_com + p.invest_pa_com + s.invest_pa_com)
        b.cost_wage = (g.cost_wage + p.cost_wage + s.cost_wage)
        b.demand_emplo = (g.demand_emplo + p.demand_emplo + s.demand_emplo)
        s_solarth.emplo_existing = (fact('Fact_B_P_install_heating_emplo_2017') * entry('In_M_population_com_2018') / entry('In_M_population_nat') * s_solarth.demand_emplo / (r30.s_solarth.demand_emplo + r30.s_heatpump.demand_emplo + s_heatpump.demand_emplo + s_solarth.demand_emplo + a30.s_heatpump.demand_emplo))
        s_gas.CO2e_total = (s_gas.CO2e_cb)
        s_gas.change_CO2e_pct = (s_gas.change_CO2e_t / b18.s_gas.CO2e_cb)
        s_emethan.CO2e_total = (s_emethan.CO2e_cb)
        s_emethan.change_energy_MWh = (s_emethan.energy - 0)
        s_emethan.CO2e_total_2021_estimated = (0 * fact('Fact_M_CO2e_wo_lulucf_2021_vs_2018'))
        s_emethan.cost_climate_saved = ((s_emethan.CO2e_total_2021_estimated - s_emethan.CO2e_cb) * entry('In_M_duration_neutral') * fact('Fact_M_cost_per_CO2e_2020'))
        s_lpg.CO2e_total = (s_lpg.CO2e_cb)
        s_lpg.change_CO2e_pct = (s_lpg.change_CO2e_t / b18.s_lpg.CO2e_cb)
        s_petrol.CO2e_total = (s_petrol.CO2e_cb)
        s_petrol.change_CO2e_pct = (s_petrol.change_CO2e_t / b18.s_petrol.CO2e_cb)
        s_jetfuel.CO2e_total = (s_jetfuel.CO2e_cb)
        s_jetfuel.change_CO2e_pct = (s_jetfuel.change_CO2e_t / b18.s_jetfuel.CO2e_cb)
        s_diesel.CO2e_total = (s_diesel.CO2e_cb)
        s_diesel.change_CO2e_pct = (s_diesel.change_CO2e_t / b18.s_diesel.CO2e_cb)
        s_fueloil.CO2e_total = (s_fueloil.CO2e_cb)
        s_fueloil.change_CO2e_pct = (s_fueloil.change_CO2e_t / b18.s_fueloil.CO2e_cb)
        s_biomass.CO2e_total = (s_biomass.CO2e_cb)
        s_biomass.change_CO2e_pct = (s_biomass.change_CO2e_t / b18.s_biomass.CO2e_cb)
        s_coal.CO2e_total = (s_coal.CO2e_cb)
        s_coal.change_CO2e_pct = (s_coal.change_CO2e_t / b18.s_coal.CO2e_cb)
        s_heatnet.CO2e_total = (s_heatnet.CO2e_cb)
        s_heatpump.CO2e_total = (s_heatpump.CO2e_cb)
        s_solarth.demand_emplo_new = (max(0,s_solarth.demand_emplo - s_solarth.emplo_existing))
        s_solarth.CO2e_total = (s_solarth.CO2e_cb)
        s.demand_emplo_new = (s_heatpump.demand_emplo_new + s_solarth.demand_emplo_new)
        b.demand_emplo_new = (g.demand_emplo_new + p.demand_emplo_new + s.demand_emplo_new)
        s_elec.CO2e_cb_per_MWh = (b18.s_elec.CO2e_cb_per_MWh)
        s_elec.CO2e_cb = (s_elec.energy * s_elec.CO2e_cb_per_MWh)
        s_elec.CO2e_total = (s_elec.CO2e_cb)
        s_elec.change_energy_MWh = (s_elec.energy - b18.s_elec.energy)
        s_elec.change_energy_pct = (s_elec.change_energy_MWh / b18.s_elec.energy)
        s_elec.change_CO2e_t = (s_elec.CO2e_cb - b18.s_elec.CO2e_cb)
        s_elec.CO2e_total_2021_estimated = (b18.s_elec.CO2e_cb * fact('Fact_M_CO2e_wo_lulucf_2021_vs_2018'))
        s_elec.cost_climate_saved = ((s_elec.CO2e_total_2021_estimated - s_elec.CO2e_cb) * entry('In_M_duration_neutral') * fact('Fact_M_cost_per_CO2e_2020'))
        s_elec_heating.pct_energy = (ass('Ass_R_S_fec_ratio_elec_heating_to_total_2050'))
        s_elec_heating.CO2e_total = (s_elec_heating.CO2e_cb)
        rp_p.CO2e_total = (r30.s.CO2e_total + s.CO2e_total)
        rp_p.change_energy_MWh = ((r30.p_buildings_total.change_energy_MWh + p_nonresi.change_energy_MWh))
        rp_p.change_energy_pct = ((rp_p.change_energy_MWh) / (r18.p_buildings_total.energy + b18.p_nonresi.energy))
        rp_p.change_CO2e_t = (rp_p.CO2e_total - b18.rp_p.CO2e_total)
        rp_p.change_CO2e_pct = (rp_p.change_CO2e_t / b18.rp_p.CO2e_total)
        rp_p.cost_climate_saved = (r30.s.cost_climate_saved + s.cost_climate_saved)
        rp_p.invest = (r30.s.invest + s.invest)
        rp_p.invest_com = (r30.s.invest_com + s.invest_com)
        rp_p.demand_emplo = (r30.g_consult.demand_emplo + r30.p_buildings_total.demand_emplo + r30.s.demand_emplo + g_consult.demand_emplo + p_nonresi.demand_emplo + s.demand_emplo)
        rp_p.emplo_existing = (r30.g_consult.emplo_existing + r30.p_buildings_total.emplo_existing + r30.s.emplo_existing + g_consult.emplo_existing + p_nonresi.emplo_existing + 0)
        rp_p.demand_emplo_new = (r30.g_consult.demand_emplo_new + r30.p_buildings_total.demand_emplo_new + r30.s.demand_emplo_new + g_consult.demand_emplo_new + p_nonresi.demand_emplo_new + s.demand_emplo_new)
        rb.energy = (r30.p.energy + p.energy)
        rb.CO2e_cb = (r30.r.CO2e_cb + b.CO2e_cb)
        rb.CO2e_total = (r30.r.CO2e_total + b.CO2e_total)
        rb.change_energy_MWh = (rb.energy - b18.rb.energy)
        rb.change_energy_pct = (rb.change_energy_MWh / b18.rb.energy)
        rb.change_CO2e_t = (rb.CO2e_cb - b18.rb.CO2e_cb)
        rb.change_CO2e_pct = (rb.change_CO2e_t / b18.rb.CO2e_cb)
        rb.CO2e_total_2021_estimated = (b18.rb.CO2e_cb * fact('Fact_M_CO2e_wo_lulucf_2021_vs_2018'))
        rb.cost_climate_saved = ((rb.CO2e_total_2021_estimated - rb.CO2e_cb) * entry('In_M_duration_neutral') * fact('Fact_M_cost_per_CO2e_2020'))
        rb.invest_pa = (r30.r.invest_pa + b.invest_pa)
        rb.invest_pa_com = (r30.r.invest_pa_com + b.invest_pa_com)
        rb.invest = (r30.r.invest + b.invest)
        rb.invest_com = (r30.r.invest_com + b.invest_com)
        rb.cost_wage = (r30.r.cost_wage + b.cost_wage)
        rb.demand_emplo = (r30.r.demand_emplo + b.demand_emplo)
        rb.demand_emplo_new = (r30.r.demand_emplo_new + b.demand_emplo_new)

    except Exception as e:
        raise



