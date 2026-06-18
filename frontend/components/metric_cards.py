import streamlit as st


# Style 01
def metric_card(title, value):
    st.markdown(
        f"""
        <div style="
            background-color:#1e293b;
            padding:20px;
            border-radius:12px;
            text-align:center;
            box-shadow:0 4px 10px rgba(0,0,0,0.3);   
            min-height:120px;                
            display:flex;                 
            flex-direction:column;
            justify-content:center;
            gap:6px;
        ">
            <div style="font-size:14px; color:#94a3b8;">{title}</div>
            <div style="font-size:26px; font-weight:bold; color:#38bdf8;">
                {value}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_data_metrics(dict_datametrics):
    num_cols = len(dict_datametrics)
    cols = st.columns(num_cols)

    for col, (title, value) in zip(cols, dict_datametrics.items()):
        with col:
            metric_card(title, value)


# Style-2
def render_data_metrics_style2(dict_datametrics):
    def _kpi_card(title, value):
        return f"""
            <div class="kpi-card">
                <div class="kpi-title">{title}</div>
                <div class="kpi-value">{value}</div>
            </div>
        """

    num_cols = len(dict_datametrics)
    cols = st.columns(num_cols)

    for col, (title, value) in zip(cols, dict_datametrics.items()):
        with col:
            st.markdown(_kpi_card(title, value), unsafe_allow_html=True)


# Style-3
def render_data_metrics_style3(dict_datametrics):
    num_cols = len(dict_datametrics)

    with st.container(border=True):
        cols = st.columns(num_cols)

        for col, (title, value) in zip(cols, dict_datametrics.items()):
            with col:
                st.metric(title, value)
