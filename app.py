import streamlit as st
from PIL import Image
from run_experiment import run_simulation
import base64

# Sidebar appearance
st.set_page_config(
    page_title="Federated Learning Simulator",
    layout="centered",
    initial_sidebar_state="expanded"
)


#CSS for profile pics
st.markdown("""
<style>
.circle-img {
    border-radius: 50%;
    border: 3px solid transparent;
    transition: 0.3s;
}
.circle-img:hover {
    cursor: pointer;
    transform: scale(1.05);
}
.selected {
    border: 3px solid #4A90E2;
}
</style>
""", unsafe_allow_html=True)

#Pic selection
selected_user = st.radio("👥 Users:", ["Ö", "K", "Ç"], horizontal=True)

#Users
user_data = {
    "Ö": {"img": "user1.png", "name": "Öznur Özkasap", "role": "Advisor"},
    "K": {"img": "user2.png", "name": "Kaan Erdoğan", "role": "Researcher"},
    "Ç": {"img": "user3.png", "name": "Çınar Arslan", "role": "Researcher"}
}

#Profile display
user_cols = st.columns(3)
for i, key in enumerate(["Ö", "K", "Ç"]):
    img_path = user_data[key]["img"]
    selected_class = "selected" if key == selected_user else ""

    with open(img_path, "rb") as f:
        img_data = f.read()
        img_base64 = base64.b64encode(img_data).decode()

    with user_cols[i]:
        st.markdown(f"""
        <img src="data:image/png;base64,{img_base64}" 
             class="circle-img {selected_class}" width="80">
        """, unsafe_allow_html=True)

# Profile info
profile = user_data[selected_user]
with st.expander("👤 Profile", expanded=True):
    st.markdown(f"**Name:** {profile['name']}")
    st.markdown(f"**Role:** {profile['role']}")


#Profile section end

#Titl
st.title("Federated Learning Client Selection Simulator")
st.markdown("""
Welcome to the interactive simulator for top FL client selection algorithms.  
You can configure the experiment below and visualize the global model parameters after training.
""")

# Sidebar simulation settings
st.sidebar.header("Simulation Settings")

dataset_type = st.sidebar.selectbox("Select Dataset Type", [
    "homo_low_dev",
    "homo_high_dev",
    "semi_homo_low_dev",
    "semi_homo_high_dev",
    "hetero_low_dev",
    "hetero_high_dev"
])

selection_algo = st.sidebar.selectbox("Select Client Selection Algorithm", [
    "loss",
    "threshold",
    "reputation",
    "multi"
])

num_clients = st.sidebar.slider("Number of Clients Per Round", 1, 15, 10)
rounds = st.sidebar.slider("Number of Training Rounds", 1, 50, 10)

# Run Simulation button
if st.sidebar.button("🚀 Run Simulation"):
    with st.spinner("Running your simulation..."):
        try:
            results = run_simulation(dataset_type, selection_algo, num_clients, rounds)
            st.success("Simulation completed successfully!")

            # Show result
            st.subheader("Global Model Parameters")
            st.metric(label="Slope", value=f"{results['global_slope']:.3f}")
            st.metric(label="Intercept", value=f"{results['global_constant']:.3f}")

            # Logs
            st.subheader("Simulation Logs")
            st.text_area("Experiment Log Output", value=results["logs"], height=400)

        except Exception as e:
            st.error(f"Simulation failed: {str(e)}")
else:
    st.info("Adjust parameters on the left and click **Run Simulation** to begin.")

# Sidebar visual references
st.sidebar.markdown("Client Selection Visual")
st.sidebar.image("cs_fig.jpg", caption="Client Selection Visual", use_container_width=True)

# Main page image at the bottom
st.markdown("---")
st.image("fl_fig.jpg", caption="Federated Learning Visual", use_container_width=True)
