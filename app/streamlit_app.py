import streamlit as st
import requests

# Make sure the docker is running first
API_URL = "http://localhost:5000/api/v1/scheduler"

headers = {
    'Content-Type': 'application/json'
}

# Streamlit app title
st.title("Shift Scheduler: REST API Version")

# Input fields for the scheduling parameters
# num_employees = st.number_input("Enter the number of employees", min_value=1, value=3)
# shifts_per_day = st.number_input("Enter the number of shifts per day", min_value=1, value=2)
# total_days = st.number_input("Enter the total number of days to schedule", min_value=1, value=5)
num_employees = st.number_input("Enter the number of employees", min_value=1, value=3)
shifts_per_day = st.number_input("Enter the number of shifts per day", min_value=1, value=2)
total_days = st.number_input("Enter the total number of days to schedule", min_value=1, value=5)

st.subheader("Employee Types")

# Input for each employee type
employee_types = []
for i in range(num_employees):
    employee_type = st.selectbox(
        f"Select type for Employee {i + 1}",
        options=["full_time", "part_time"],
        index=0
    )
    employee_types.append(employee_type)

# When the user clicks the "Generate Schedule" button
if st.button("Generate Schedule"):
    # Prepare the data to be sent to the API
    data = {
        "num_employees": num_employees,
        "shifts_per_day": shifts_per_day,
        "total_days": total_days,
        "employee_types": employee_types
    }

    # Display a loading spinner while processing
    with st.spinner("Generating schedule..."):
        # Send a POST request to the API
        response = requests.post(API_URL, headers=headers, json=data)

        # Check if the response is successful
        if response.status_code == 200:
            # Parse the response JSON and display the output
            output = response.json()
            st.success("Schedule generated successfully!")
            st.write(output)
        else:
            st.error(f"Failed to generate schedule. Error: {response.status_code}")
            st.write(response.text)
