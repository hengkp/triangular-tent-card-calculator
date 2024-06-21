import streamlit as st
import math
import matplotlib.pyplot as plt

st.title('Triangular Tent Card Calculator')

st.write('## Input Parameters')

# Inputs
paper_type = st.selectbox('Paper Type', ['A4', 'Custom'])
width = st.number_input('Width (cm)', min_value=1, value=210)  # cm
length = st.number_input('Length (cm)', min_value=1, value=297)  # cm

# Get base, front, back, and angles inputs from the user
base = st.number_input('Base (cm)', min_value=1, value=50)  # cm
base_x2 = base * 2  # cm

# Default front and back to base to start
front = base 
back = base

# Calculate angles
A = st.number_input('Angle A (degree)', min_value=0, max_value=180, value=45)
B = st.number_input('Angle B (degree)', min_value=0, max_value=180, value=90)

# Calculate angle C
C = 180 - A - B

# Check if the provided angles form a valid triangle
if A + B + C != 180 or A <= 0 or B <= 0 or C <= 0:
    st.error("Invalid angles: Angles A, B, and C must sum to 180 degrees.")
else:
    # Calculate lengths using the law of sines
    front = base_x2 * math.sin(math.radians(A)) / math.sin(math.radians(C))
    back = base_x2 * math.sin(math.radians(B)) / math.sin(math.radians(C))

# Displaying the inputs and calculated values
st.write(f"### Paper Type: {paper_type}")
st.write(f"### Width: {width} cm")
st.write(f"### Length: {length} cm")

st.write('## Calculated Dimensions')
st.write(f"### Base x2: {base_x2:.2f} cm")
st.write(f"### Front: {front:.2f} cm")
st.write(f"### Back: {back:.2f} cm")

st.write('## Calculated Angles')
st.write(f"### Angle A: {A:.2f}°")
st.write(f"### Angle B: {B:.2f}°")
st.write(f"### Angle C: {C:.2f}°")

# Plotting the triangle
fig, ax = plt.subplots()
x = [0, base_x2/2, base_x2, 0]
y = [0, front, 0, 0]
ax.plot(x, y, 'b-')
ax.text(0, 0, 'A', fontsize=12, ha='right')
ax.text(base_x2, 0, 'C', fontsize=12, ha='left')
ax.text(base_x2/2, front, 'B', fontsize=12, ha='center')
ax.set_xlim(-10, base_x2 + 10)
ax.set_ylim(-10, front + 10)
ax.set_aspect('equal')
ax.grid(True)

st.pyplot(fig)

st.write('## Coordinate System')
st.write('### X: 1, 2, 3, 4, 5...')
st.write('### Y: 1, 1, 1, 1...')

# Placeholder for coordinates
coordinate_x = [i for i in range(1, 6)]
coordinate_y = [1 for _ in range(5)]

st.write(f"### Coordinate X: {coordinate_x}")
st.write(f"### Coordinate Y: {coordinate_y}")
