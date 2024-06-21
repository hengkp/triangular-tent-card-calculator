import streamlit as st
import math
import matplotlib.pyplot as plt

st.title('Triangular Tent Card Calculator')

# Sidebar inputs
st.sidebar.write('## Input Parameters')
paper_type = st.sidebar.selectbox('Paper Type', ['A4', 'Custom'])
width = st.sidebar.number_input('Width (mm)', min_value=1, value=210)  # cm
length = st.sidebar.number_input('Length (mm)', min_value=1, value=297)  # cm

# Use st.session_state to handle the interdependent changes between base, front, and angle A
if 'base' not in st.session_state:
    st.session_state.base = 74.0
if 'front' not in st.session_state:
    st.session_state.front = 74.0
if 'A' not in st.session_state:
    st.session_state.A = 60.0

def update_A():
    C = math.degrees(math.asin(st.session_state.front * math.sin(math.radians(st.session_state.A)) / st.session_state.base))
    B = 180 - st.session_state.A - C
    if B > 0:
        st.session_state.base = st.session_state.front * math.sin(math.radians(C)) / math.sin(math.radians(st.session_state.A))
    else:
        # this should change the back length first, then change the base length, and finally the front length by loop decreasing the back length until 1 then decrease the base length until 1 until the B is more than zero
        while B <= 0:
            st.session_state.front -= 1
            if st.session_state.front < 1:
                st.session_state.front = 1
                st.session_state.base = (length - st.session_state.front - 2) / 2
                while B <= 0:
                    st.session_state.base -= 1
                    if st.session_state.base < 1:
                        st.session_state.base = 1
                        st.session_state.front = length - st.session_state.base - 2
                        while B <= 0:
                            st.session_state.front -= 1
                            if st.session_state.front < 1:
                                st.session_state.front = 1
                                st.session_state.base = (length - st.session_state.front - 2) / 2
                                break
                        break
            C = math.degrees(math.asin(st.session_state.front * math.sin(math.radians(st.session_state.A)) / st.session_state.base))
            B = 180 - st.session_state.A - C

def update_front():
    back = length - st.session_state.front - 2 * st.session_state.base
    if back < 0:
        back = 1
        st.session_state.base = (length - st.session_state.front - back) / 2
        if st.session_state.base < 0:
            st.session_state.base = 1
            st.session_state.front = length - back - 2 * st.session_state.base
    C = math.degrees(math.acos((st.session_state.front**2 + st.session_state.base**2 - back**2) / (2 * st.session_state.front * st.session_state.base)))
    B = math.degrees(math.acos((back**2 + st.session_state.base**2 - st.session_state.front**2) / (2 * back * st.session_state.base)))
    st.session_state.A = 180 - B - C

def update_base():
    back = length - st.session_state.front - 2 * st.session_state.base
    if back < 0:
        back = 1
        st.session_state.front = length - back - 2 * st.session_state.base
        if st.session_state.front < 0:
            st.session_state.front = 1
            st.session_state.base = (length - st.session_state.front - back) / 2
    C = math.degrees(math.acos((st.session_state.front**2 + st.session_state.base**2 - back**2) / (2 * st.session_state.front * st.session_state.base)))
    B = math.degrees(math.acos((back**2 + st.session_state.base**2 - st.session_state.front**2) / (2 * back * st.session_state.base)))
    st.session_state.A = 180 - B - C

st.sidebar.number_input('Base (mm)', min_value=1.0, step=1.0, value=st.session_state.base, key='base', on_change=update_base)
st.sidebar.number_input('Front (mm)', min_value=1.0, step=1.0, value=st.session_state.front, key='front', on_change=update_front)
st.sidebar.number_input('Angle A (degree)', min_value=0.0, max_value=180.0, step=1.0, value=st.session_state.A, key='A', on_change=update_A)

# Button to reset to defaut values
if st.sidebar.button('Reset'):
    st.session_state.pop('base', None)
    st.session_state.pop('front', None)
    st.session_state.pop('A', None)
    st.session_state.base = 74.0
    st.session_state.front = 74.0
    st.session_state.A = 60.0

# Initialize variables
back = B = C = None
base_x2 = st.session_state.base * 2

try:
    # Calculate angle C and angle B
    C = math.degrees(math.asin(st.session_state.front * math.sin(math.radians(st.session_state.A)) / st.session_state.base))
    B = 180 - st.session_state.A - C

    if st.session_state.A <= 0 or B <= 0 or C <= 0:
        st.error("Invalid angles: Angles A, B, and C must be greater than 0 degrees.")
    else:
        # Calculate back length using the law of sines
        back = st.session_state.base * math.sin(math.radians(B)) / math.sin(math.radians(C))
except ValueError:
    st.error("Invalid values leading to math domain error.")

# Layout with columns
col1, col2 = st.columns(2)

with col1:
    st.write(f"### Paper Type: {paper_type}")
    st.write(f"### Width: {width} mm")
    st.write(f"### Length: {length} mm")
    st.write('## Calculated Dimensions')
    st.write(f"### Base x2: {base_x2:.2f} mm")
    if st.session_state.front is not None:
        st.write(f"### Front: {st.session_state.front:.2f} mm")
    if back is not None:
        st.write(f"### Back: {back:.2f} mm")
        st.write(f"### Totals: {st.session_state.front + back + base_x2:.2f} mm")
    st.write('## Calculated Angles')
    st.write(f"### Angle A: {st.session_state.A:.2f}°")
    if B is not None:
        st.write(f"### Angle B: {B:.2f}°")
    if C is not None:
        st.write(f"### Angle C: {C:.2f}°")

with col2:
    if st.session_state.front is not None and back is not None:
        # Plotting the triangle
        fig, ax = plt.subplots()
        x = [0, st.session_state.front * math.cos(math.radians(st.session_state.A)), base_x2 / 2, 0]
        y = [0, st.session_state.front * math.sin(math.radians(st.session_state.A)), 0, 0]
        ax.plot(x, y, 'b-')
        ax.text(0, 0, 'A', fontsize=16, ha='right')
        ax.text(st.session_state.base, 0, 'C', fontsize=16, ha='left')
        ax.text(st.session_state.front * math.cos(math.radians(st.session_state.A)), st.session_state.front * math.sin(math.radians(st.session_state.A)), 'B', fontsize=16, ha='center')
        # for i, txt in enumerate(zip(x, y)):
        #     ax.annotate(f'({txt[0]:.2f}, {txt[1]:.2f})', (x[i], y[i]), textcoords="offset points", xytext=(0,10), ha='center')
        ax.set_xlim(-10, length / 2)
        ax.set_ylim(-10, length / 2)
        ax.set_aspect('equal')
        ax.grid(True)
        st.pyplot(fig)
        st.write('## Coordinate System')
        st.write(f"### Coordinate X: {int(x[0]):.0f}, {int(x[1]):.0f}, {int(x[2]):.0f}, {int(x[3]):.0f}")
        st.write(f"### Coordinate X: {int(y[0]):.0f}, {int(y[1]):.0f}, {int(y[2]):.0f}, {int(y[3]):.0f}")
