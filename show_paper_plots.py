from PIL import Image
import streamlit as st

from typing import List
from functools import partial

DATA_URL = (
    "."
)

uni_pi = f'\N{GREEK SMALL LETTER PI}'
uni_S0 = f'S\N{SUBSCRIPT ZERO}'

nmarkets = 5000

st.title("Plotting the simulation results")
st.header("for the Salani&eacute;-Wolak FRAC paper")

st.markdown(
    "This is a discrete choice model on market-level data, with multinomial logit idiosyncratic preference shocks and mean utilities:")
st.latex(
    r''' U_{ijt} = \beta_0 + x_{jt} (\beta_1 + \pi D_{i}  +\sigma \varepsilon_i) + \xi_{jt} ''')
st.markdown(
    "     where $x$ is the log-price, and $D$ is a demographic variable ('micromoment').")

st.subheader("The true values of the parameters are chosen as follows:")
st.latex(r''' \beta_1 = -4.0 ''')
st.write("  so that the own price semi-elasticity is roughly -2;")
st.latex(
    r''' \beta_0  \text{ is chosen to set the market share } S_0 \text{ of the zero good (see below)} ''')
st.latex(r''' D_i = N(\bar{D}_t, \tau^2)''')
st.latex(r'''   \text{   where } \bar{D}_t=N(0,1) \text{ and }  \tau^2=0.5 ''')

st.subheader("The correlation structure")
st.latex(
    r''' \text{ We draw independently } z_{jt}=N(0,1), \xi_{jt}=N(0,1), and u_{jt}=N(0,1)''')
st.latex(
    r''' \text{   then } x_{jt} = \rho_{xz}  z_{jt} + \sqrt(1 - \rho_{xz}^2) (\rho_{x\xi} \xi_{jt}+u_{jt})''')
st.latex(r'''  \text{     where } \rho_{x\xi}^2 =\rho_{xz}^2=0.5''')

st.subheader("Special cases")
st.latex(r''' \text{ The exogenous models have } \rho_{x\xi} = 0; ''')
st.latex(r''' \text{ The models without a micromoment have } \pi = 0.''')

st.subheader("Notes on the graphs")
st.latex(
    r'''  \text{ The graphs show various simulation results as } \sigma \text{ varies }''')
st.latex(
    r'''  \text{   the horizontal axes use } s^2=\sigma^2+\tau^2\pi^2 \text{, or } \sigma^2 \text{ when } \pi=0.''')
st.write("The 95% confidence intervals shown are computed using the semiparametric efficiency bounds for 100 markets.")
st.write("Given the symmetry in the model, the cross-price semi-elasticities are the same for any two products; ")
st.write("     mean and dispersion are computed across markets.")


@st.cache(persist=True)
def load_plot(plot_type: str, nproducts: int, scenario: int,
              model: str, pi_num: int = None):
    plot_dir = f"{DATA_URL}/J{nproducts}/{model}_v{scenario}/figures_paper"
    T_str = f"T={nmarkets}" if pi_num is None else f"T={nmarkets}_pi{pi_num}"
    plot_root = f"{plot_dir}/{plot_type}_{model}_" + \
                f"J={nproducts}_v{scenario}"
    our_plot = Image.open(f"{plot_root}_{T_str}.png")
    return our_plot


labels_plot_types = ["Pseudo-true values",
                     "Semi-elasticities"]

options_plot_types = ["new_pseudo_vals",
                      "new_semi_elast"]


def format_f(s: str, list_s: List[str], list_labels: List[str]) \
        -> str:
    for i, optn in enumerate(list_s):
        if s == optn:
            return list_labels[i]


plot_types = st.multiselect("Result", options=options_plot_types,
                            format_func=partial(format_f,
                                                list_s=options_plot_types,
                                                list_labels=labels_plot_types))

options_scenarii = [4, 3]
labels_scenarii = [f"{uni_S0} close to 0.9", f"{uni_S0} close to 0.5"]
scenarii = st.multiselect("Market share of the zero good", options=options_scenarii,
                          format_func=partial(format_f,
                                              list_s=options_scenarii,
                                              list_labels=labels_scenarii))

options_models = ["endo_demog", "endo", "exo_demog", "exo"]
labels_models = ["Endogenous, with a micromoment",
                 "Endogenous, no micromoment",
                 "Exogenous, with a micromoment",
                 "Exogenous, no micromoment"]

models = st.multiselect("Model", options=options_models,
                        format_func=partial(format_f,
                                            list_s=options_models,
                                            list_labels=labels_models))

J_vals = st.multiselect("Number of products", [1, 2, 5, 10, 25, 50, 100])

options_pi = [0, 1, 2]
labels_pi = ["0.25", "0.5", "1.0"]

if 'endo_demog' in models or 'exo_demog' in models:
    pi_vals = st.multiselect(f"Value of {uni_pi} (the mean coefficient of the micromoment)",
                             options=options_pi,
                             format_func=partial(format_f,
                                                 list_s=options_pi,
                                                 list_labels=labels_pi))

st.subheader("Here are your plots")
for plot_type in plot_types:
    for scenario in scenarii:
        for J in J_vals:
            for model in models:
                if "demog" in model:
                    for pi_num in pi_vals:
                        plot_i = load_plot(plot_type, J, scenario, model,
                                           pi_num=pi_num)
                        st.image(plot_i)
                else:
                    plot_i = load_plot(plot_type, J, scenario, model)
                    st.image(plot_i)
